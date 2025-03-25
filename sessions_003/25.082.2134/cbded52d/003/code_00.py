"""
The transformation copies the input grid and then modifies it. It identifies non-all-zero rows. For every other of these rows, starting with the first, it copies the values in the 2nd and 5th columns from the input grid to the corresponding locations in the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Identify target rows (every other non-all-zero row, starting with first)
    target_rows = []
    non_zero_row_count = 0
    for i in range(rows):
        if np.any(input_grid[i] != 0):  # Check if the row is not all zeros
            non_zero_row_count += 1
            if non_zero_row_count % 2 != 0: #check if odd numbered non-zero row
                target_rows.append(i)

    # Apply modification to target columns in target rows
    for row_index in target_rows:
        # Target columns are 2nd (index 1) and 5th (index 4)
      if cols > 1:
        output_grid[row_index, 1] = input_grid[row_index, 1]
      if cols > 4:
        output_grid[row_index, 4] = input_grid[row_index, 4]

    return output_grid.tolist()