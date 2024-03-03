#!/bin/bash

: ${1?"Usage: $0 vmname"}

sudo -E virget --pretty dumpjson $1

exit 0
