```python
"""
The transformation rule is to find the smallest rectangular region (bounding box)
that contains all non-zero pixels in the input grid and extract that region as
the output grid.
"""

import numpy as np

def get_bounding_box(grid):
    """
    Finds the bounding box of non-zero elements in a grid.

    Args:
        grid: A 2D numpy array.

    Returns:
        A tuple (min_row, max_row, min_col, max_col) representing the bounding box.
    """
    rows = np.any(grid != 0, axis=1)
    cols = np.any(grid != 0, axis=0)
    min_row, max_row = np.where(rows)[0][[0, -1]] if np.any(rows) else (0, 0)
    min_col, max_col = np.where(cols)[0][[0, -1]] if np.any(cols) else (0, 0)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Transforms the input grid by extracting the smallest rectangular region
    containing all non-zero pixels.

    Args:
        input_grid: A 2D list representing the input grid.

    Returns:
        A 2D list representing the output grid.
    """
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # Find the bounding box
    min_row, max_row, min_col, max_col = get_bounding_box(input_grid)

    # Extract the subgrid defined by the bounding box
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]

    return output_grid.tolist()
```