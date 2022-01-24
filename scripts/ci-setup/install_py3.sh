#!/bin/bash
#
# set -euo pipefail
#
# Script to ensure that Python3 RPM is installed
#
#################################################################

if [[ -x $( readlink -f /bin/yum ) ]] && \
   [[ $( rpm --quiet -q python3 )$? -ne 0 ]]
then
   printf "Checking availability of python3 package..."
   if [[ $( yum list available python3 > /dev/null 2>&1 )$? -eq 0 ]]
   then
      printf "Installing python3... "
      yum install -y python3 || ( echo "Failed!" ; exit 1 )
      echo "Success"
   else
      echo "No python3 RPM available for install"
      exit 1
   fi
fi
