#!/bin/bash

: ${1?"Usage: $0 vmname"}

virget --pretty --query 'data[].addrs[].addr' domifaddr --source arp $1

exit 0
