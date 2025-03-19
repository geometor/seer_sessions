# 23b5c85d • 024 • refine_coder

---
```python
"""
1.  **Identify Orange Region:** Locate the rectangular region of orange (color 7) pixels in the input grid.
2.  **Extract, if present**: If an orange region exists, extract it. The output grid will be the same dimensions and contain only the pixels within the bounding box of the orange region in the input.
3.  **Handle No Orange:** If there are no orange pixels in the input grid, the output grid is empty (0x0).
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
    Extracts the rectangular region of orange pixels, or returns an empty grid if no orange is present.
    """
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # Find the bounding box of the orange region
    orange_color = 7
    bounding_box = find_object_by_color(input_grid, orange_color)

    # Handle the case where no orange is found.
    if bounding_box is None:
        return np.array([]).tolist()  # Return an empty list (0x0 grid)

    top_left, bottom_right = bounding_box
    
    # Extract the orange region using array slicing.  Add 1 to bottom_right to include last element.
    output_grid = input_grid[top_left[0]:bottom_right[0]+1, top_left[1]:bottom_right[1]+1]

    return output_grid.tolist()
```
