# JFTF-Core

JFTF-Core is a powerful backend for the Java Functional Testing Framework (JFTF) that provides a RESTful API for handling the test automation logic of JFTF. Built on top of Django, JFTF-Core is a flexible and customizable solution that can be easily integrated into your existing testing workflows.

With JFTF-Core, you can create and manage test suites, define test case parameters, and schedule test runs. The API is designed to be easy-to-use, providing a seamless integration with JFTF-App. You can use the API to create and manage test cases, as well as to schedule test runs and monitor results. 

One of the main benefits of JFTF-Core is its advanced reporting capabilities. You can generate detailed reports that give you valuable insights into the performance and stability of your applications. The reports include information on test cases, test runs, and test suite results. This information can be used to identify performance bottlenecks and stability issues, helping you to optimize your applications.

JFTF-Core is highly customizable, and can be easily integrated into your existing testing workflows. You can use the API to build custom solutions that fit your specific testing needs. For example, you can use the API to schedule test runs at specific times, or to integrate JFTF-Core with other testing tools.

JFTF-Core is designed to work seamlessly with JFTF-App, but it can also be used as a standalone solution. If you're looking for a powerful backend for your testing workflows, JFTF-Core is the perfect solution.

## Key Features

- RESTful API for handling the test automation logic of JFTF
- Easy-to-use interface for managing and executing functional test cases
- Advanced reporting capabilities for gaining insights into application performance and stability
- Highly customizable to fit your specific testing needs
- Seamlessly integrates with JFTF-App

## Getting Started (**WIP**)

To get started with JFTF-Core, check out the documentation on our [website](https://www.javafunctionaltestingframework.com/docs/core).

## Configuration and Startup Steps

To deploy JFTF-Core and start it locally, follow these steps:

1. Execute the script found in `deploy_dev_local.sh`. First, navigate to the `scripts/deploy` directory in your terminal.
2. Before executing the script, make sure to follow the instructions specified in the script header.
3. To start the Python virtual environment, execute the script `source activate_dev_venv.sh`. Navigate to the `scripts/deploy` directory in your terminal before running the command.
4. Change the directory to `jftf_core` by running `cd jftf_core`.
5. Start the JFTF-Core server by running `python3 manage.py runserver 8000`.
6. To start the Celery worker, execute the script `run_celery_worker.sh` located in the `scripts/celery` directory. Navigate to the `scripts/celery` directory in your terminal.

Please note that the provided instructions assume a Unix-based environment. Adjustments may be needed if you are using a different operating system.

## License

JFTF-Core is open source software, released under the [MIT License](./LICENSE).
