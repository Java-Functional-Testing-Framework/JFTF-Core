#!/bin/bash
# ©2023 JFTF
# JFTF-Core MariaDB timezone definitions fix
# Prerequisites
# Ubuntu 22.04+
# MariaDB deployed with the "deploy_dev_local.sh" script
# Version 1.0

echo "Will be prompted to input root password, you can safely enter no value!"
mysql_tzinfo_to_sql /usr/share/zoneinfo | sudo mysql -u root -p mysql
