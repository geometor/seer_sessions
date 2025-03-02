# 23b5c85d • 022 • example_4 • investigate_coder

---
```python
"""
Extracts the rectangular region of orange (7) pixels from the input grid.
"""

import numpy as np

def find_object_by_color(grid, color):
    """
    Finds the bounding box of a contiguous region of a specific color in a grid.

    Args:
      grid: A 2D numpy array representing the grid.
      color: The color to search for.

    Returns:
      A tuple (top_left, bottom_right) representing the bounding box coordinates
      of the object, or None if the color is not found.
    """
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None
    top_left = (min(rows), min(cols))
    bottom_right = (max(rows), max(cols))
    return top_left, bottom_right

def transform(input_grid):
    """
    Extracts the rectangular region of orange pixels.
    """
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # Find the bounding box of the orange region
    orange_color = 7
    bounding_box = find_object_by_color(input_grid, orange_color)

    if bounding_box is None:
        return [] # Or some other default value indicating no orange found.

    top_left, bottom_right = bounding_box
    
    # Extract the orange region using array slicing.  Add 1 to bottom_right to include last element
    output_grid = input_grid[top_left[0]:bottom_right[0]+1, top_left[1]:bottom_right[1]+1]

    return output_grid.tolist()
```
