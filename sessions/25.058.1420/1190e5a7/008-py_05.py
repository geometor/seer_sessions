"""
1.  **Identify the Border:** Locate the orange (7) pixels in the input grid.  These form an incomplete rectangle, open at the top.
2.  **Define Inner Region:** Determine the rectangular region enclosed by the orange border. This excludes the border itself.
3.  **Identify Inner Object:** Within the inner region, identify the single-colored contiguous object that contrasts with the black(0) background and orange(7) border.
4. **Extract Inner Object**: Create an output grid with just the inner object. The output grid must only contain the inner object.
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

def find_inner_object(grid, inner_region):
    """
    Finds the single-colored contiguous object within the inner region.
    Returns the object's color and its bounding box coordinates.
    """
    if inner_region is None:
        return None, None

    min_row, max_row, min_col, max_col = inner_region
    inner_grid = grid[min_row:max_row+1, min_col:max_col+1]

    # Find colors other than 0 (background)
    unique_colors = np.unique(inner_grid)
    object_colors = unique_colors[unique_colors != 0]

    if len(object_colors) == 0:
      return None, None
    
    # Assume first non-background is target
    object_color = object_colors[0]
    object_coords = np.argwhere(grid == object_color)

    min_obj_row = np.min(object_coords[:, 0])
    max_obj_row = np.max(object_coords[:, 0])
    min_obj_col = np.min(object_coords[:, 1])
    max_obj_col = np.max(object_coords[:, 1])

    return object_color, (min_obj_row, max_obj_row, min_obj_col, max_obj_col)


def transform(input_grid):
    """Extracts the single-colored object inside the orange border."""
    # Find the border coordinates
    border_coords = find_border(input_grid, 7)

    # Find the inner region
    inner_region = find_inner_region(input_grid, border_coords)

    # Find the inner object and its bounding box
    object_color, object_bbox = find_inner_object(input_grid, inner_region)
    
    if object_bbox is not None:
      min_row, max_row, min_col, max_col = object_bbox
      output_grid = input_grid[min_row:max_row+1, min_col:max_col+1].copy()
    else:
      output_grid = np.array([[]]) # return empty if none found

    return output_grid