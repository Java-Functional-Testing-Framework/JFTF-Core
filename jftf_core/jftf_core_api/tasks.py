import os
import subprocess
from ..jftf_core import jftf_celery_app


@jftf_celery_app.task(bind=True)
def execute_jftf_test_case(self, script_path):
    # Check if the script path exists
    if not os.path.exists(script_path):
        # Send error message to result backend
        return {'status': 'error', 'message': 'Script path does not exist'}

    # Update task status to 'In Progress'
    self.update_state(state='IN_PROGRESS', meta={'status': 'In Progress'})

    try:
        # Execute the script asynchronously
        process = subprocess.Popen([script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Wait for the process to complete
        process.wait()

        if process.returncode == 0:
            # Test case execution completed successfully
            return {'status': 'success', 'message': 'Test case executed successfully'}
        else:
            # Test case execution error
            return {'status': 'error', 'message': stderr.decode('utf-8')}
    except Exception as e:
        # Test case execution error
        return {'status': 'error', 'message': str(e)}
