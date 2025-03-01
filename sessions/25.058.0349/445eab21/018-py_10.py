"""
1.  Identify all objects: Find all contiguous regions of the same color in the input grid, and determine their bounding boxes.
2.  Find Output Size: Identify the object in the input made by a single color. The size of its bounding box defines output grid size.
3.  Find extraction object: Identify the biggest object containing other colors in the input.
4.  Extract Subgrid: Extract a subgrid from the input. The size of the subgrid is determined in step 2. The subgrid top-left corner is the same of extraction object found in step 3.
5.  Output: The extracted subgrid is the output.
"""

import numpy as np

def find_object_bounding_box(grid, color):
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None
    top_left = (min(rows), min(cols))
    bottom_right = (max(rows), max(cols))
    return top_left, bottom_right

def get_object_details(grid):
  objects = {}
  grid_array = np.array(grid)
  for color in np.unique(grid_array):
    bounding_box = find_object_bounding_box(grid_array, color)
    if bounding_box:
      top_left, bottom_right = bounding_box
      objects[color] = {
          'top_left': top_left,
          'bottom_right': bottom_right,
          'width': bottom_right[1] - top_left[1] + 1,
          'height': bottom_right[0] - top_left[0] + 1
      }
  return objects

def find_first_single_color_object(grid):
    """Finds the first object in the grid that consists of only one color."""
    grid_np = np.array(grid)
    for color in np.unique(grid_np):
        rows, cols = np.where(grid_np == color)
        if len(rows) > 0:  # Ensure the color exists in the grid
            # Check if all cells within the bounding box are of the same color
            top_left, bottom_right = find_object_bounding_box(grid_np, color)
            object_pixels = grid_np[top_left[0]:bottom_right[0]+1, top_left[1]:bottom_right[1]+1]
            if np.all(object_pixels == color):
                return color, top_left, bottom_right
    return None, None, None

def find_largest_multicolor_object(grid):
    """Finds the largest object in the grid that contains multiple colors."""
    grid_np = np.array(grid)
    largest_object = None
    max_area = 0

    objects = get_object_details(grid_np)
    for color, details in objects.items():
        top_left = details['top_left']
        bottom_right = details['bottom_right']
        object_pixels = grid_np[top_left[0]:bottom_right[0]+1, top_left[1]:bottom_right[1]+1]

        if np.unique(object_pixels).size > 1:
            area = details['width'] * details['height']
            if area > max_area:
                max_area = area
                largest_object = details

    return largest_object


def transform(input_grid):
    # Find the first single-color object and its bounding box.
    color, top_left, bottom_right = find_first_single_color_object(input_grid)
    
    if color is None:
        return [[]]  # Return an empty grid if no single-color object is found

    object_width = bottom_right[1] - top_left[1] + 1
    object_height = bottom_right[0] - top_left[0] + 1

    # Find largest multicolor object
    extraction_object = find_largest_multicolor_object(input_grid)

    if not extraction_object:
        return [[]]

    # Extract a subgrid of the determined size, starting from the top-left of largest multicolor object.
    row_start, col_start = extraction_object['top_left']
    output_grid = []
    for i in range(object_height):
        row = []
        for j in range(object_width):
            if row_start + i < len(input_grid) and col_start + j < len(input_grid[0]):
                row.append(input_grid[row_start + i][col_start + j])
            else:
                row.append(0) # fill with 0 if out of bounds
        output_grid.append(row)

    return output_grid