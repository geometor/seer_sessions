```python
"""
Embeds the input grid within a larger grid, adding one row and one column, and fills the new cells with maroon (9). The input grid is placed at the top-left corner of the output grid.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to numpy array for easier manipulation
    input_grid = np.array(input_grid)
    input_rows, input_cols = input_grid.shape

    # Determine output grid dimensions.
    output_rows = input_rows + 1
    output_cols = input_cols + 1

    # Initialize output_grid with maroon (9)
    output_grid = np.full((output_rows, output_cols), 9)

    # Embed the input_grid into the output_grid at top-left (0,0)
    output_grid[:input_rows, :input_cols] = input_grid

    return output_grid.tolist()
```