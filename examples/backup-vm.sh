#!/bin/bash

set -eux

: ${2?"Usage: $0 vmname output-dir"}

test -d "$2" || { echo $2 not exist; exit 1; }

vmname="$1"
outdir="$2"

vmstate=$(virget --pretty --query 'data.state' --raw-output dominfo ${vmname})
#echo ${vmname} ${vmstate}

test ${vmstate} = 'running' || { echo ${vmname} is not running; exit 1; }

bkxml="${outdir}/${vmname}-backup.xml"

virget backup-newxml ${vmname} "${outdir}" > "${bkxml}"
virsh backup-begin ${vmname} --backupxml "${bkxml}"

echo + phase 1/2
while :
do
  jobtype=$(virget --query 'data.type' --raw-output domjobinfo $vmname)
  echo current jobtype is ${jobtype}

  test ${jobtype} = 'none' && break

  sleep 3
done

echo
echo + phase 2/2
while :
do
  jobtype=$(virget --query 'data.type' --raw-output domjobinfo $vmname --completed)
  echo current jobtype is ${jobtype}

  test ${jobtype} = 'none' && break

  sleep 3
done

echo
echo + result
echo
ls -l "${outdir}"
echo

echo all done.

exit 0
