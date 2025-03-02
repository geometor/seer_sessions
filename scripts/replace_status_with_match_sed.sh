#!/bin/bash

# scripts/replace_status_with_match_sed.sh

find ../sessions -name "*.json" -type f -print0 | xargs -0 sed -i 's/"status"/"match"/g'

# Optional: Add some error checking
if [ $? -eq 0 ]; then
  echo "Successfully replaced 'status' with 'match' in JSON files."
else
  echo "An error occurred during the replacement."
fi
