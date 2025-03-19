# c909285e • 010 • example_2 • investigate_coder

---
```python
"""
The transformation extracts a significant, patterned subgrid from the center of the full image.
"""

import numpy as np

def find_central_object(grid, object_color=2):
    """
    Finds the bounding box of a central object of a specified color.

    Args:
        grid: A 2D numpy array representing the input grid.
        object_color: The color of the object to find.

    Returns:
        A tuple (min_row, max_row, min_col, max_col) representing the bounding box,
        or None if no object of the specified color is found.
    """
    rows, cols = np.where(grid == object_color)
    if rows.size == 0 or cols.size == 0:
        return None

    # find the largest contiguous block
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    
    return (min_row, max_row, min_col, max_col)


def transform(input_grid):
    """
    Extracts a 7x7 subgrid from the center of the input, based on
    the central pattern defined by red pixels.
    """
    # Convert input to numpy array
    input_grid = np.array(input_grid)
    
    # Find the central red object
    bounding_box = find_central_object(input_grid, object_color=2)
    if bounding_box is None:
        return None  # Or handle the case where no red object is found

    min_row, max_row, min_col, max_col = bounding_box
    
    #find object inside of the red frame
    rows, cols = np.where(input_grid[min_row:max_row+1, min_col:max_col+1] != 2)
    
    
    center_row = min_row+rows.mean()
    center_col = min_col+cols.mean()

    # Calculate the starting row and column for the 7x7 subgrid
    start_row = int(center_row - 3)
    start_col = int(center_col - 3)

    # Extract the 7x7 subgrid
    output_grid = input_grid[start_row:start_row + 7, start_col:start_col + 7]

    return output_grid.tolist()
```
