#!/bin/bash
set -euo pipefail
REPO_NAME="custom-co7-rpms"

if [[ -z ${CUSTOM_YUM_REPO:-} ]]
then
   echo "Yum repository URL not set in environment"
   yum install -y python3
else
   echo "Setting up custom yum repo-def"
   (
     echo "[${REPO_NAME}]"
     echo "name=Custom Yum repo - OS"
     echo "baseurl=${CUSTOM_YUM_REPO}"
     echo "enabled=1"
     echo "gpgcheck=0"
   ) > /etc/yum.repos.d/private.repo
   yum --disablerepo=* --enablerepo="${REPO_NAME}" install -y python3
fi
