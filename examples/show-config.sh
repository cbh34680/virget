#!/bin/bash

: ${1?"Usage: $0 vmname"}

virget --pretty dumpjson $1

exit 0
