#!/bin/bash
set -euo pipefail
#
# Scritpt to sweep project for YAML files and, if found,
# use `yamllint` to lint them
############################################################

# Create empty-array
declare -a FOUND_FILES

# Populate array
readarray -t FOUND_FILES < <(
  find . -type f  \( -name "*.yml" \
    -o -name "*.yaml" \
    -o -name "*.YML" \
    -o -name "*.YAML" \)
)

# Check whether array has lintable content
if [[ ${#FOUND_FILES[*]} -eq 0 ]]
then
   echo "Found no YAML files to lint"
else
   for VAR in "${FOUND_FILES[@]}"
   do
      echo "Checking ${VAR}..."
      yamllint "${VAR}"
   done
fi
