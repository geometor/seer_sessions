```python
"""
Extracts a 2x2 subgrid from the input grid. 
If the input grid's width is even, the top-right 2x2 subgrid is extracted.
If the input grid's width is odd, the top-left 2x2 subgrid is extracted.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the 2x2 extracted subgrid.
    """
    # Convert input list of lists to numpy array if it's not already
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid, dtype=int)

    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Initialize output_grid (will be assigned the slice)
    output_grid = None

    # Check if the width is even or odd
    if width % 2 == 0:
        # If width is even, extract the top-right 2x2 subgrid
        # Rows 0 and 1, columns width-2 and width-1
        output_grid = input_grid[0:2, width-2:width]
    else:
        # If width is odd, extract the top-left 2x2 subgrid
        # Rows 0 and 1, columns 0 and 1
        output_grid = input_grid[0:2, 0:2]

    return output_grid

```