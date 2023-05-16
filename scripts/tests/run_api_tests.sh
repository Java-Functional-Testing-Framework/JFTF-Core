#!/bin/bash
# ©2023 JFTF
# JFTF-Core API tests run script
# Prerequisites
# Ubuntu 22.04+
# Virtual environment activated with the "activate_dev_venv.sh" script

# Usage: ./run_api_tests.sh

python3 ../../jftf_core/manage.py test jftf_core_api --keepdb
