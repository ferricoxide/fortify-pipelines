#!/bin/bash
#
# Script to install and activate custom yum repos
#################################################################

# Install custom yum repo-def if defined
if [[ -n ${CUSTOM_YUM_REPO} ]]
then
   declare -a ACTIVATABLE_REPOS
   declare LOOP
   declare REPO_FILE

   LOOP=0
   REPO_FILE="/etc/yum.repos.d/ci-custom.repo"

   printf "Installing ci-custom repo... "
   cp "${CUSTOM_YUM_REPO}" "${REPO_FILE}" || ( echo FAILED ; exit 1)
   echo Succeeded.

   mapfile -t ACTIVATABLE_REPOS < <( grep '^\[' "${REPO_FILE}" | sed -e 's/\[//' -e 's/]//' )

   while [[ ${LOOP} -lt ${#ACTIVATABLE_REPOS[*]} ]]
   do
      yum-config-manager --enable "${ACTIVATABLE_REPOS[${LOOP}]}"
      LOOP=$(( LOOP += 1 ))
   done
else
   echo "No custom yum repositories declared for project"
fi
