#!/bin/bash

sudo -E virget --pretty --query 'data[].name' list --all

exit 0
