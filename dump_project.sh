#!/bin/bash

output_file="project_dump.txt"
touch "$output_file"
echo "Project Dump" > "$output_file"

# Create an array of patterns to ignore from the .gitignore file
ignore_patterns=()
while IFS= read -r line; do
    if [[ ! "$line" =~ ^\# ]] && [[ ! -z "$line" ]]; then
        ignore_patterns+=("$line")
    fi
done < ".gitignore"

# Add patterns to ignore JPEG image files
ignore_patterns+=(".*\.jpg$")
ignore_patterns+=(".*\.jpeg$")

should_ignore() {
    for pattern in "${ignore_patterns[@]}"; do
        if [[ $1 =~ $pattern ]]; then
            return 0
        fi
    done
    return 1
}

traverse() {
  for file in "$1"/*; do
    if ! should_ignore "$file"; then
      if [ -d "$file" ]; then
        traverse "$file"
      elif [ -f "$file" ]; then
        echo -e "\n# File: $file\n" >> "$output_file"
        cat "$file" >> "$output_file"
      fi
    fi
  done
}

traverse "$(pwd)/app"
traverse "$(pwd)/tests"

echo "Project dump complete. Check project_dump.txt in the project root directory."
