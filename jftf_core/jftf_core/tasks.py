from subprocess import Popen, PIPE
from pathlib import Path
from . import jftf_celery_app


@jftf_celery_app.task(bind=True)
def execute_jftf_test_case(self, jar_path):
    # Extract the script path from the jar_path
    jftf_script_path = Path(jar_path).parent / 'bin' / Path(jar_path).stem

    # Check if the script path exists
    if not jftf_script_path.exists():
        # Send error message to result backend
        return {'status': 'error', 'message': 'JFTF script path does not exist at provided location'}

    # Update task status to 'In Progress'
    self.update_state(state='IN_PROGRESS', meta={'status': 'In Progress'})

    try:
        # Execute the script asynchronously
        process = Popen([str(jftf_script_path)], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()

        # Wait for the process to complete
        process.wait()

        if process.returncode == 0:
            # Test case execution completed successfully
            return {'status': 'success', 'message': 'JFTF test application executed successfully'}
        else:
            # Test case execution error
            return {'status': 'error', 'message': stderr.decode('utf-8')}
    except Exception as e:
        # Test case execution error
        return {'status': 'error', 'message': str(e)}
