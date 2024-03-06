#!/bin/bash

for vmname in $(virget --query 'data[].name' --raw-output list)
do
  virsh shutdown ${vmname}

  while :
  do
    state=$(virget --query 'data.state.stateText' --raw-output domstats ${vmname})
    echo ${vmname}: current [${state}]

    if test "$state" = 'shutoff';
    then
      break
    fi

    echo ${vmname}: wait for shutoff ...
    sleep 3
  done
done

exit 0
