#!/bin/bash

: ${1?"Usage: $0 vmname"}

sudo -E virget --pretty --query 'data[].source' domblklist $1

exit 0
