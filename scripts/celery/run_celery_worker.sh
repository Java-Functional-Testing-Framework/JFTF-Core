#!/bin/bash
# ©2023 JFTF
# Celery worker bootstrapper script
# Prerequisites
# Ubuntu 22.04+
# Version 1.0
# Environment deployed using "deploy/deploy_dev_local.sh" script
# Usage
# ./run_celery_worker.sh
# WARNING!!!
# Script only works if executing from the same directory, do not run from relative path
# WARNING!!!

echo "Sourcing Python virtual environment"

source ../deploy/activate_dev_venv.sh

echo "Changing directory to Django project root"

cd ../../jftf_core || exit 1

echo "Bootstrapping celery worker"

celery -A jftf_core worker --loglevel=info
