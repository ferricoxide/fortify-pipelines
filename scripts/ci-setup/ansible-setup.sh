#!/bin/bash
#
# Script to install the components necessary to lint and execute 
# Ansible playbooks
#
#################################################################
set -euo pipefail

# Install Ansible tools from RPM
yum install -y ansible ansible-lint

# Install warning-squelching config if none present in projec
if [[ ! -e ansible.cfg ]]
then
  printf "Creating basic Ansible config file... "
  (
    echo "[defaults]"
    echo "deprecation_warnings=False"
  ) > ~/ansible.cfg || ( echo "FAILED!" ; exit 1 )
  echo Success
fi

# Make sure the posix Ansible modules are available
echo "Installing Ansible's POSIX-modules collection... "
ansible-galaxy collection install ansible.posix || \
  ( echo "Failed" ; exit 1 )
echo "Success"
