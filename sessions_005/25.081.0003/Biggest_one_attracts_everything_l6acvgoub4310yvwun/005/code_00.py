"""
The transformation rule works as follows:

1.  **Identify Objects:** Treat contiguous blocks of non-zero pixels of the same color within each row as individual objects.
2.  **Rearrange within Rows:** Within each row, move all zero pixels ('0') to the left, and non-zero pixels shift to fill the remaining spaces to the right.
3.   **Move Empty Rows:** Move all rows that contained any non-zero pixels to the top and fill the remaining rows with zero.
"""

import numpy as np

def rearrange_row(row):
    """Rearranges a single row by moving zeros to the left."""
    non_zeros = [pixel for pixel in row if pixel != 0]
    zeros = [pixel for pixel in row if pixel == 0]
    return zeros + non_zeros

def transform(input_grid):
    """Transforms the input grid according to the rule."""
    input_grid_np = np.array(input_grid)
    rows, cols = input_grid_np.shape
    output_grid = []
    non_empty_rows = []

    # Rearrange within each row and collect non-empty rows.
    for row in input_grid_np:
        rearranged_row = rearrange_row(list(row))
        if any(pixel != 0 for pixel in rearranged_row):  #Check if it is a non zero row
          non_empty_rows.append(rearranged_row)
        
    
    # construct output grid with modified non empty rows at top
    for row in non_empty_rows:
      output_grid.append(row)
      
    # Pad the remaining rows with zeros.
    while len(output_grid) < rows:
        output_grid.append([0] * cols)

    return output_grid