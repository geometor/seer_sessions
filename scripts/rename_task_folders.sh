#!/usr/bin/env bash
cd ..
find sessions -mindepth 2 -maxdepth 2 -type d -name "[0-9]-*" | while read -r dir; do
  echo $dir
  new_dir=$(echo "$dir" | sed 's/\/[0-9]-/\//')
  if [ "$dir" != "$new_dir" ]; then
    echo "Renaming '$dir' to '$new_dir'"
    mv "$dir" "$new_dir"
  fi
done
