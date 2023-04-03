#!/bin/bash
# ©2023 JFTF
# JFTF legacy DBDriver database views initializer
# Prerequisites
# (MariaDB DBMS)
# WARNING
# Don't run this script by itself, script is executed as part of deploy_dev_local.sh
# Version 1.0

jftf_user_password=$1
jftf_user_ip=$2

function init_jftf_cmdb_db_views(){
  echo "Creating JFTF cmdb legacy database views";
  sudo mariadb < create_views.sql
  if [ $? == 0 ]
    then
      echo "Created database views schema!";
    else
      echo "Failed to create database views schema!";
      exit 1;
  fi
  echo "Successfully created JFTF cmdb legacy database views!";
  exit 0;
}

if [ "$EUID" -ne 0 ]
  then echo "Please run the script as root!";
  exit
fi

if [ -z "$jftf_user_password" ] || [ -z "$jftf_user_ip" ]
then
  echo "Script usage is: database_init.sh <jftf_user_password> <jftf_user_ip>";
  exit 1;
fi

init_jftf_cmdb_db_views;
