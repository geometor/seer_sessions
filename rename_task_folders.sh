#!/bin/bash

# Iterate through all session timestamp folders
find sessions -mindepth 1 -maxdepth 1 -type d | while read session_timestamp; do
  # Iterate through all task_id folders within each session
  find "$session_timestamp" -mindepth 1 -maxdepth 1 -type d | while read task_folder; do
    # Extract the task folder name
    task_name=$(basename "$task_folder")

    # Remove the "N-" prefix if present
    new_task_name=$(echo "$task_name" | sed 's/^[0-9]\+-//')

    # If the name changed, rename the folder
    if [ "$task_name" != "$new_task_name" ]; then
      new_task_folder=$(dirname "$task_folder")/"$new_task_name"
      echo "Renaming '$task_folder' to '$new_task_folder'"
      mv "$task_folder" "$new_task_folder"
    fi
  done
done

