"""
Transforms an input grid by expanding non-zero pixels horizontally and vertically, inserting rows of zeros.

1. Iterate through rows of the input grid.
2. For each row, expand horizontally:
   - If a non-zero pixel is found, fill the rest of the row with that pixel's value.
3. Replicate Vertically:
    - Place the expanded row in the output.
    - For each subsequent row: insert a row of all zeros, then another copy of the expanded row.
"""

import numpy as np

def expand_row_horizontally(row):
    """Expands a single row by filling to the right after a non-zero pixel."""
    expanded_row = np.copy(row)
    found_non_zero = False
    for i in range(len(row)):
        if row[i] != 0:
            expanded_row[i:] = row[i]
            found_non_zero = True
            break  # Stop after the first non-zero value
    return expanded_row

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = []

    for row_index in range(rows):
        # Horizontal Expansion
        expanded_row = expand_row_horizontally(input_grid[row_index])

        # Vertical Replication
        output_grid.append(expanded_row)
        for _ in range(row_index + 1, rows):
           output_grid.append(np.zeros(cols, dtype=int))
           output_grid.append(expanded_row)
    return np.array(output_grid)