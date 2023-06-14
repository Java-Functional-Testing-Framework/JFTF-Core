from celery import states
from subprocess import Popen, PIPE
from pathlib import Path
from . import jftf_celery_app


class TestCaseApplicationScriptPathNotFound(Exception):
    def __init__(self, script_path: Path):
        self.script_path = script_path
        super().__init__(f"JFTF script path does not exist at provided location: '{script_path}'")


class TestCaseApplicationExecutionError(Exception):
    def __init__(self, script_path: Path, stderr: str):
        self.script_path = script_path
        super().__init__(f"JFTF test application from: '{script_path}' failed to execute, STDERR is '{stderr}'")


@jftf_celery_app.task(bind=True)
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
