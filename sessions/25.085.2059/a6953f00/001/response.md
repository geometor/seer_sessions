```python
"""
Extracts a 2x2 subgrid from the input grid based on the parity of the input grid's width.
If the width is even, the top-right 2x2 subgrid is extracted.
If the width is odd, the top-left 2x2 subgrid is extracted.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on its width parity.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The 2x2 extracted output grid.
    """
    # Convert input_grid to a numpy array for easier slicing
    grid = np.array(input_grid, dtype=int)

    # Get the dimensions of the input grid
    height, width = grid.shape

    # Check if the width is even or odd
    if width % 2 == 0:
        # If width is even, extract the top-right 2x2 subgrid
        # Rows 0 and 1 (index 0 to 2), Columns W-2 and W-1 (index W-2 to W)
        output_grid = grid[0:2, width-2:width]
    else:
        # If width is odd, extract the top-left 2x2 subgrid
        # Rows 0 and 1 (index 0 to 2), Columns 0 and 1 (index 0 to 2)
        output_grid = grid[0:2, 0:2]

    return output_grid.tolist() # Return as list of lists to match ARC format if needed
```