```python
"""
Embeds the input grid within a larger grid and fills the surrounding area with the color maroon (9).
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to numpy array for easier manipulation
    input_grid = np.array(input_grid)
    input_rows, input_cols = input_grid.shape

    # Determine output grid dimensions and offset based on input dimensions.
    # add one row above and one row below
    output_rows = input_rows + 2
    # if the input grid has only one column, add one on right
    # if > 1 col, and 1 to left and right
    output_cols = input_cols + (1 if input_cols == 1 else 2)
    

    # Initialize output_grid with maroon (9)
    output_grid = np.full((output_rows, output_cols), 9)

    # Embed the input_grid into the output_grid.
    # Calculate row and column start positions for embedding
    row_start = 0 if input_cols == 1 else 1
    col_start = 1 if input_cols > 1 else 0

    output_grid[row_start:row_start + input_rows, col_start:col_start + input_cols] = input_grid

    return output_grid.tolist()
```