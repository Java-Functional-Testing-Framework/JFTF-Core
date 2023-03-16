#!/bin/bash
# ©2023 JFTF
# JFTF-Core development memcached cache reset script
# Prerequisites
# Ubuntu 22.04+
# memcached service active
# Version 1.0

echo 'flush_all' | nc localhost 11211 | exit
