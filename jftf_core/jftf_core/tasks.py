from celery import states, group
from subprocess import Popen, PIPE
from pathlib import Path
from celery.signals import task_failure
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from django.utils import timezone
from django_celery_results.models import TaskResult
from . import jftf_celery_app


class TestCaseApplicationScriptPathNotFound(Exception):
    def __init__(self, script_path: Path):
        self.script_path = script_path
        super().__init__(f"JFTF script path does not exist at provided location: '{script_path}'")


class TestCaseApplicationExecutionError(Exception):
    def __init__(self, script_path: Path, stderr: str):
        self.script_path = script_path
        super().__init__(f"JFTF test application from: '{script_path}' failed to execute, STDERR is '{stderr}'")


class TestCaseApplicationGroupExecutionError(Exception):
    def __init__(self, task_id):
        self.task_id = task_id
        super().__init__(
            f"JFTF test application execution failed for task ID: '{task_id}'")


@jftf_celery_app.task(bind=True, trail=True)
def execute_jftf_test_case(self, jar_path, testrunner):
    # Extract the script path from the jar_path
    jftf_script_path = Path(jar_path).parent.parent / 'bin' / Path(jar_path).stem

    # Check if the script path exists
    if not jftf_script_path.exists():
        # Send error message to result backend
        self.update_state(state=states.FAILURE,
                          meta={'status': 'ERROR', 'message': 'JFTF script path does not exist at provided location'})
        raise TestCaseApplicationScriptPathNotFound(script_path=jftf_script_path)

    # Update task status to 'In Progress'
    self.update_state(state=states.PENDING,
                      meta={'status': states.PENDING, 'message': 'JFTF test application execution in progress'})

    try:
        # Execute the script asynchronously
        process = Popen([str(jftf_script_path), '-d', testrunner], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()

        # Wait for the process to complete
        process.wait()

        if process.returncode == 0:
            # Test case execution completed successfully
            return {'status': states.SUCCESS, 'message': 'JFTF test application executed successfully',
                    'stdout': stdout.decode('utf-8')}
        else:
            # Test case execution error
            self.update_state(state=states.FAILURE,
                              meta={'status': 'ERROR', 'message': 'JFTF test application failed to execute',
                                    'stderr': stderr.decode('utf-8')})
            raise TestCaseApplicationExecutionError(script_path=jftf_script_path, stderr=stderr.decode('utf-8'))
    except Exception as e:
        # Test case execution error
        self.update_state(state=states.FAILURE, meta={'status': 'ERROR', 'message': str(e)})
        raise ValueError(str(e))


@jftf_celery_app.task(bind=True, trail=True)
def send_failure_email(self, task_id, error_message, recipient_emails):
    subject = 'JFTF Test Application Execution Task Failed'
    template = 'email/test_execution_task_failure_email.html'

    # Get the TaskResult object for the task_id
    try:
        task_result = TaskResult.objects.get(task_id=task_id)
    except TaskResult.DoesNotExist:
        return {'success': False, 'error_message': 'TaskResult not found'}

    # Extract additional information from the task_result
    worker_name = task_result.worker
    task_args = task_result.task_args
    created_at = task_result.date_created
    completed_at = task_result.date_done
    timezone_setting = timezone.get_current_timezone_name()

    # Render the email template with the error message and additional information
    email_body = render_to_string(
        template,
        {
            'error_message': error_message,
            'task_id': task_id,
            'worker_name': worker_name,
            'task_args': task_args,
            'created_at': created_at,
            'completed_at': completed_at,
            'timezone_setting': timezone_setting,
        }
    )

    # Strip HTML tags from the message for the plain text version
    plain_message = strip_tags(email_body)

    # Send the email
    send_mail(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        recipient_emails,
        html_message=email_body,
        fail_silently=False,
    )

    # Create a success JSON response with the recipient list
    response_data = {
        'success': True,
        'recipients': recipient_emails,
        'error_message': error_message,
        'test_execution_task_id': task_id,
        'worker_name': worker_name
    }

    return response_data


@jftf_celery_app.task(bind=True, trail=True)
def execute_jftf_test_case_group(self, jar_paths, testrunner):
    # Create a group of individual tasks
    task_group = group(
        execute_jftf_test_case.s(jar_path, testrunner) for jar_path in jar_paths
    )

    # Update task status to 'In Progress'
    self.update_state(state=states.PENDING,
                      meta={'status': states.PENDING, 'message': 'JFTF test application group execution in progress'})

    # Execute the group of tasks and get the group result
    group_result = task_group.delay()

    # Check the status of individual tasks in the group
    while True:
        try:
            if all(result.ready() for result in group_result.results):
                break
        except Exception:
            # Suppress exception thrown from group task (at ready() call), for some reason this cannot be stopped,
            # so instead it has to be suppressed
            pass

    # Check if any task in the group has failed
    for result in group_result.results:
        if result.failed():
            # Update the task state to 'FAILURE' and raise the custom exception
            self.update_state(state=states.FAILURE,
                              meta={'status': states.FAILURE,
                                    'message': 'JFTF test application group execution failed'})
            raise TestCaseApplicationGroupExecutionError(result.id)

    # Retrieve relevant information from individual results
    result_info = []
    for result in group_result.results:
        result_info.append({
            'task_id': result.id,
            'status': result.status,
            'result': result.result,
            'traceback': result.traceback,
        })

    # Return the group result and relevant information
    return {'status': states.SUCCESS, 'individual_test_execution_results': result_info}


@task_failure.connect(sender=execute_jftf_test_case)
def handle_task_failure(sender=None, task_id=None, exception=None, traceback=None, einfo=None, **kwargs):
    # Extract the relevant information from the failure signal
    error_message = str(exception)

    # Get all user emails from the User model
    recipient_emails = list(User.objects.values_list('email', flat=True))

    # Execute the Celery task to send the failure email asynchronously
    send_failure_email.delay(task_id, error_message, recipient_emails)
