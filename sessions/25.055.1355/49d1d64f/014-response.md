# 49d1d64f • 014 • example_3 • investigate_coder

---
```python
"""
The transformation takes the input grid, expands it by creating mirrored copies around a central vertical and horizontal axis, and fills in any leftover space with zeros.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 3x3 input grid into a 5x5 output grid by mirroring
    the input grid horizontally and vertically, and padding the
    remaining cells with 0.
    """
    # Initialize the output grid with zeros.
    output_grid = np.zeros((5, 5), dtype=int)

    # Get the dimensions of the input grid.
    input_height, input_width = input_grid.shape

    # Calculate the center indices for both input and output grids.
    input_center_row = input_height // 2
    input_center_col = input_width // 2
    output_center_row = 2
    output_center_col = 2

    # Place the center element of the input grid at the center of the output grid.
    output_grid[output_center_row, output_center_col] = input_grid[input_center_row, input_center_col]

    # Iterate through the input grid and mirror the elements.
    for i in range(input_height):
        for j in range(input_width):
            # Calculate the corresponding output indices.
            output_row = i + (output_center_row - input_center_row)
            output_col = j + (output_center_col - input_center_col)

            # Place the element in the output grid.
            output_grid[output_row, output_col] = input_grid[i, j]

            # Mirror horizontally.
            mirrored_col = output_grid.shape[1] - 1 - output_col
            output_grid[output_row, mirrored_col] = input_grid[i, j]
            
            # Mirror vertically.
            mirrored_row = output_grid.shape[0] -1 - output_row
            output_grid[mirrored_row, output_col] = input_grid[i,j]

            # mirror diagonally
            output_grid[mirrored_row, mirrored_col] = input_grid[i,j]

    return output_grid
```
