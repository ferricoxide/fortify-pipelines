#!/bin/bash
set -euo pipefail
#
# Scritpt to sweep project for shell-scripts and, if found,
# use `pylint` to lint them
############################################################

# Create empty-array
declare -a FOUND_FILES

# Populate array
readarray -t FOUND_FILES < <(
  find . -type f  \( -name "*.py" \
    -o -name "*.PY" \
  \)
)

# Check whether array has lintable content
if [[ ${#FOUND_FILES[*]} -eq 0 ]]
then
   echo "Found no YAML files to lint"
else
   for VAR in "${FOUND_FILES[@]}"
   do
      echo "Checking ${VAR}..."
      pylint "${VAR}"
   done
fi
