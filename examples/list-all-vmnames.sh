#!/bin/bash

virget --pretty --query 'data[].name' list --all

exit 0
