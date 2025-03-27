```python
import numpy as np

"""
Extracts a 2x2 subgrid from the input grid based on the parity of the input grid's width.
If the width is odd, the top-left 2x2 subgrid is extracted.
If the width is even, the top-right 2x2 subgrid is extracted.
"""

def transform(input_grid):
    """
    Extracts a 2x2 subgrid from the input grid.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The extracted 2x2 output grid.
    """
    # Convert input_grid to a numpy array for easier slicing
    grid = np.array(input_grid, dtype=int)

    # Get the dimensions (height and width) of the input grid
    height, width = grid.shape

    # Check if the width is odd or even
    if width % 2 != 0:
        # If width is odd, extract the top-left 2x2 subgrid
        # Rows 0 and 1, Columns 0 and 1
        output_grid = grid[0:2, 0:2]
    else:
        # If width is even, extract the top-right 2x2 subgrid
        # Rows 0 and 1, Columns width-2 and width-1
        output_grid = grid[0:2, width-2:width]

    # Return the extracted 2x2 subgrid
    return output_grid.tolist() # Convert back to list of lists if needed by the framework

```