#!/bin/bash
set -euo pipefail
#
# Scritpt to sweep project for shell-scripts and, if found,
# use `shellchecker` to lint them
############################################################

# Create empty-array
declare -a FOUND_FILES

# Populate array
readarray -t FOUND_FILES < <(
  find . -type f  \( -name "*.sh" \
    -o -name "*.bash" \
    -o -name "*.csh" \
    -o -name "*.ksh" \
    -o -name "*.zsh" \
    -o -name "*.SH" \
    -o -name "*.BASH" \
    -o -name "*.CSH" \
    -o -name "*.KSH" \
    -o -name "*.ZSH" \
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
      shellcheck "${VAR}"
   done
fi
