#!/bin/bash
set -euo pipefail
#
# Script to install desired python module from an appropriate
# repository
#
#################################################################
PKG="${1:-}"

# Check if package was requested
if [[ -z ${PKG:-} ]]
then
   echo "No package requested. Aborting"
   exit 1
fi

# Whether to install from private repository
if [[ -n ${NEXUS3_FQDN:-} ]]
then
   # Install a netrc file to be used by curl and pip
   printf 'Writing ~/.netrc for pip to use... '
   install -bDm 0600 <(
     echo "machine ${NEXUS3_FQDN}"
     echo "login ${NEXUS3_CRED_USER}"
     echo "password ${NEXUS3_CRED_PASS}"
   ) -o root -g root ~/.netrc || ( echo -e "\e[31mFailed writing ~/.netrc\e[0m" ; exit 1 )
   echo -e "\e[32mSucceeded!\e[0m"

   # Install desired module
   echo "Attempting to install ${PKG} from ${NEXUS3_FQDN}"
   python3 -m pip install -i "${PYPI_INDEX_URL}" --trusted-host "${NEXUS3_FQDN}" "${PKG}"
else
   python3 -m pip install "${PKG}"
fi
