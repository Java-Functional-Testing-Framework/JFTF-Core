#!/bin/bash
# ©2023 JFTF
# JFTF-Core development memcached cache stats script
# Prerequisites
# Ubuntu 22.04+
# memcached service installed/active
# Version 1.0

/usr/share/memcached/scripts/memcached-tool localhost:11211 stats
