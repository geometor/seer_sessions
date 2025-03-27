"""
Transforms an input grid by removing rows starting with 2, processing rows starting with 6, 
and reordering them based on digit frequency and lexicographical order.
"""

import numpy as np

def get_counts(row):
    """Counts occurrences of each digit in a row."""
    counts = {}
    for x in row:
        counts[x] = counts.get(x, 0) + 1
    return counts

def get_max_count_digit(counts):
  """Find digit that appears most."""
  max_count = 0
  max_digit = -1

  for digit, count in counts.items():
    if count > max_count:
      max_count = count
      max_digit = digit
  return max_digit


def transform(input_grid):
    # Convert input_grid to a list of lists for easier manipulation.
    rows = [list(row) for row in input_grid]
    
    # 1. Identify and Remove: Remove any row that starts with the number 2.
    rows_to_process = [row for row in rows if row[0] != 2]
    
    # Find elements only appearing in rows that start with 2
    elements_in_removed = []
    if len(rows_to_process) < len(rows): #rows were removed
      for row in rows:
        if row[0] == 2:
          elements_in_removed.extend(row)
    
    # 2. Identify Target Rows: Identify rows that start with the number 6.
    six_rows = [row for row in rows_to_process if row[0] == 6]
    other_rows = [row for row in rows_to_process if row[0] != 6]

    # 3. Transform '6' Rows, Phase 1: For rows starting with 6, remove that first '6'.
    transformed_six_rows = [row[1:] for row in six_rows]

    # 4. Group and Sort (Modified):
    groups = {}
    for row in transformed_six_rows:
        counts = get_counts(row)
        max_digit = get_max_count_digit(counts)

        if max_digit not in groups:
            groups[max_digit] = []
        groups[max_digit].append(row)

    # Sort groups based on max_digit (higher digits first), then sort rows within each group lexicographically.
    sorted_groups = []

    for max_digit in sorted(groups.keys(), reverse=True):
        sorted_groups.extend(sorted(groups[max_digit]))

    #5. Shorten rows
    shortened_rows = [row[-6:] for row in sorted_groups]

    #6. Leftover input handling.
    reconstructed_row = []
    if elements_in_removed:
      
      present_values = set()
      for row in shortened_rows:
        present_values.update(row)

      missing = [val for val in elements_in_removed if val not in present_values]
      reconstructed_row = sorted(list(set(missing)))

      if len(reconstructed_row) > 6:
        reconstructed_row = reconstructed_row[-6:]
      elif len(reconstructed_row) < 6: #need to pick up some more values, borrow from existing rows
        borrowed = []
        for row in shortened_rows:
          for item in row:
            if len(reconstructed_row) + len(borrowed) < 6:
              borrowed.append(item)
            else:
              break
          if len(reconstructed_row) + len(borrowed) >= 6:
            break

        reconstructed_row.extend(borrowed)
        reconstructed_row = sorted(reconstructed_row)
        reconstructed_row = reconstructed_row[-6:]
    # 7. Output Construction

    output_rows = []

    if reconstructed_row:
      output_rows.append(reconstructed_row)
    
    output_rows.extend(shortened_rows)
  

    # Convert back to numpy array
    output_grid = np.array(output_rows)

    return output_grid