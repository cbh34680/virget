#!/bin/bash

: ${1?"Usage: $0 vmname"}

virget --pretty --query 'data[].source' domblklist $1

exit 0
