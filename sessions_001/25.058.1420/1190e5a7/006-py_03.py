"""
1.  **Identify the Border:** Locate the '7's (orange pixels) in the input grid, forming a large, thick-lined square open at the top.
2.  **Find the Inner Region:**  Determine the bounding box of the area enclosed by the orange border. This excludes the border itself.
3.  **Locate the Target Object:** Find the 2x2 block of '3' (green) pixels within this inner region.
4.  **Extract:**  Extract the 2x2 green block.
5.  **Output:** The extracted 2x2 block becomes the output grid.
"""

import numpy as np

def find_border(grid, border_color):
    """Finds coordinates of all border pixels."""
    border_coords = np.argwhere(grid == border_color)
    return border_coords

def find_inner_region(grid, border_coords):
    """Determines the bounding box of the area enclosed by the border."""
    if len(border_coords) == 0:
        return None
    min_row = np.min(border_coords[:, 0]) + 1
    max_row = np.max(border_coords[:, 0]) - 1
    min_col = np.min(border_coords[:, 1]) + 1
    max_col = np.max(border_coords[:, 1]) - 1

    # Check for valid inner region
    if min_row > max_row or min_col > max_col:
        return None
    
    return min_row, max_row, min_col, max_col

def find_object(grid, object_value, inner_region):
    """Finds a 2x2 block of the specified object value within the inner region"""
    if inner_region is None:
      return None

    min_row, max_row, min_col, max_col = inner_region
    for row in range(min_row, max_row):
        for col in range(min_col, max_col):
            if (grid[row:row+2, col:col+2] == object_value).all():
                return row, col #return top left corner
    return None
    

def transform(input_grid):
    """Extracts the 2x2 block of '3's inside the orange border."""
    # Find the border coordinates
    border_coords = find_border(input_grid, 7)

    # Find the inner region
    inner_region = find_inner_region(input_grid, border_coords)

    # Find top left of 2 x 2 block of value '3'
    object_top_left = find_object(input_grid, 3, inner_region)
    
    if object_top_left is not None:
      row, col = object_top_left
      output_grid = input_grid[row:row+2, col:col+2].copy()
    else:
      output_grid = np.zeros((2,2)) # should not happen based on problem statement

    return output_grid