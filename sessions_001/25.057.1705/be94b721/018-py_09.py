"""
1.  **Identify Objects:** Find all contiguous regions of the same color in the input grid. These are the objects.
2.  **Border Rule:** If there is an object that forms a complete border around other objects, remove the border and output the inner region.
3. **Color 8 Rule:** If there is a single color 8 object, and no other rule applies, the color 8 object is removed and the grid is empty.
4.  **Top-Left Rule:** If there are multiple objects of color 8, extract the top-leftmost object of color 8.
5.  **No Azure Rule:** If there are no objects of color 8, examine objects of other colors and their relationships, especially border/inner.
6. Color 7 Rule: If there is a single color 7 object, output an empty grid
"""

import numpy as np
import scipy.ndimage

def find_objects(grid):
    """
    Finds all contiguous regions of the same color in the grid.
    Returns a list of bounding box coordinates (top_left_row, top_left_col, bottom_right_row, bottom_right_col)
    and their corresponding masks.
    """
    objects = []
    for color in np.unique(grid):
        mask = (grid == color).astype(int)
        if np.sum(mask) == 0:
            continue

        labeled_mask, num_labels = scipy.ndimage.label(mask)

        for label in range(1, num_labels + 1):
            rows, cols = np.where(labeled_mask == label)
            top_left_row, top_left_col = np.min(rows), np.min(cols)
            bottom_right_row, bottom_right_col = np.max(rows), np.max(cols)
            objects.append(((top_left_row, top_left_col, bottom_right_row, bottom_right_col), (labeled_mask == label), color))

    return objects

def remove_border(grid):
    """
    Removes the outer layer of a grid if it forms a complete border of the same color
    """
    if grid.size == 0:  # Handle empty grids
      return grid
    
    rows, cols = grid.shape
    
    if rows < 3 or cols < 3:
        return grid

    top_row = grid[0, :]
    bottom_row = grid[-1, :]
    left_col = grid[:, 0]
    right_col = grid[:, -1]
    
    if (np.all(top_row == top_row[0]) and np.all(bottom_row == top_row[0]) and
        np.all(left_col == top_row[0]) and np.all(right_col == top_row[0])):
      return grid[1:-1, 1:-1]
    
    return grid

def check_border(grid, object_info):
    """
    Checks if given object is a complete border around entire grid.
    """
    bounding_box, _, _ = object_info
    top_left_row, top_left_col, bottom_right_row, bottom_right_col = bounding_box
    rows, cols = grid.shape

    return top_left_row == 0 and top_left_col == 0 and bottom_right_row == rows - 1 and bottom_right_col == cols - 1

def transform(input_grid):
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)

    # Find all objects
    objects = find_objects(input_grid)

    # sort objects by color
    objects.sort(key=lambda x: x[2])

    # Border Rule
    for obj_info in objects:
      if check_border(input_grid, obj_info):
          bounding_box, _, _ = obj_info
          top, left, bottom, right = bounding_box
          return input_grid[top+1:bottom, left+1:right].tolist()
    
    # Find azure objects
    azure_objects = [obj for obj in objects if obj[2] == 8]
    
    # Color 8 Rule (single object)
    if len(azure_objects) == 1:
        return []

    # Top-Left Rule (multiple azure objects)
    if len(azure_objects) > 1:
        azure_objects.sort(key=lambda x: (x[0][0], x[0][1]))  # Sort by top-left corner
        bounding_box, _, _ = azure_objects[0]
        top_left_row, top_left_col, bottom_right_row, bottom_right_col = bounding_box
        return input_grid[top_left_row:bottom_right_row+1, top_left_col:bottom_right_col+1].tolist()

    # Find orange objects
    orange_objects = [obj for obj in objects if obj[2] == 7]
    
    #Color 7 rule (single object)
    if len(orange_objects) == 1:
        return []

    return []