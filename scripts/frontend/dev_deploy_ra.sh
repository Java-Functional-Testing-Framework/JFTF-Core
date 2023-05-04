#!/bin/bash
# ©2023 JFTF
# JFTF frontend development environment deployment script
# Prerequisites
# Ubuntu 22.04+
# Version 1.0
# Usage
# ./dev_deploy_ra.sh

# Check if npm is installed
if ! command -v npm &> /dev/null
then
    echo "npm not found. Installing npm..."
    # Install npm
    sudo apt-get update
    sudo apt-get install -y npm
fi

# Install yarn using npm
if ! command -v yarn &> /dev/null
then
    echo "yarn not found. Installing yarn..."
    # Install yarn using npm
    npm install --global yarn
fi

# Change to jftf_app directory
cd ../../jftf_app/ || exit 1

# Install yarn dependencies
yarn install
