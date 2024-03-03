#!/bin/bash

: ${1?"Usage: $0 vmname"}

sudo -E virget --pretty domifaddr --source arp $1 | jq -r '.data[].addrs | map(.addr)'

exit 0
