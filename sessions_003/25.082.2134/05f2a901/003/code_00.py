"""
The transformation removes empty (white) rows *between* objects, preserving leading and trailing empty rows.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by removing empty rows between objects,
    preserving leading and trailing empty rows.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # 1. Find the indices of non-empty rows.
    non_empty_row_indices = []
    for r in range(rows):
        if not all(input_grid[r] == 0):
            non_empty_row_indices.append(r)

    # 2. Copy leading empty rows.
    current_output_row = 0
    for r in range(rows):
        if r < (non_empty_row_indices[0] if non_empty_row_indices else rows) :
          output_grid[current_output_row] = input_grid[r]
          current_output_row += 1
        else:
          break

    # 3. Copy non-empty rows and trailing, removing rows between objects.
    
    for r in non_empty_row_indices:
        output_grid[current_output_row] = input_grid[r]
        current_output_row += 1


    return output_grid.tolist()