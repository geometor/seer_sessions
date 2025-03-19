# f25fbde4 • 014 • refine_coder

---
```python
"""
1.  **Identify the Object:** Find the connected component of yellow (4) pixels in the input grid. This forms an "L" shape, potentially with one extended arm.

2.  **Determine Orientation:** Analyze the "L" shape to determine its orientation based on which corner pixel would complete a 2x2 square, or which side is extended. The possible orientations are "top-left", "top-right", "bottom-left", and "bottom-right", with extended variants.

3.  **Create, Rotate, and Flip:**
    *   Create a copy of the identified "L" shape.
    *   Rotate the copy 90 degrees counter-clockwise.
    *   Flip the rotated object over the x axis.
    *  Flip the rotated object over the y axis.

4.  **Combine and Position:**
    *   Create a new grid large enough to accommodate both the original and transformed "L" shapes.
    *   Place the original "L" shape in the grid.
    *   Place the flipped and rotated copy adjacent to the original "L".
        - If the original is bottom-right oriented: Place the copy above and to the left.
        - If the original is top-right oriented:  Place the copy below and to the left.
        - If the original is bottom-left oriented: Place the copy above and to the right.
        - If the original is top-left oriented:   Place the copy below and to the right.

5.  **Trim:** Remove any empty rows and columns from the combined grid to produce the final output.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels with the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, None, None
    # find the bounding box
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    return coords, (min_row, min_col), (max_row, max_col)

def extract_object(grid, min_coords, max_coords):
    # slice the grid with the bounding box
    return grid[min_coords[0]:max_coords[0]+1, min_coords[1]:max_coords[1]+1]

def rotate_object(object_grid):
      # rotate counter clockwise
    return np.rot90(object_grid)

def determine_orientation(object_grid):
    # Check for the missing corner in the 2x2 bounding box.
    if object_grid.shape == (2,2):
      if object_grid[0, 0] == 0:
        return "top-left"
      elif object_grid[0, 1] == 0:
        return "top-right"
      elif object_grid[1, 0] == 0:
          return "bottom-left"
      elif object_grid[1, 1] == 0:
          return "bottom-right"
    elif object_grid.shape == (3,2):
      if np.array_equal(object_grid[0:2,0:2], np.array([[4,4],[0,4]])):
        return "top-left extended"
      elif np.array_equal(object_grid[0:2,0:2], np.array([[4,4],[4,0]])):
        return "top-right extended"
      elif np.array_equal(object_grid[1:3,0:2], np.array([[0,4],[4,4]])):
        return "bottom-left extended"
      else: #if np.array_equal(object_grid[1:3,0:2], np.array([[4,0],[4,4]])):
        return "bottom-right extended"
    elif object_grid.shape == (2,3):
      if np.array_equal(object_grid[0:2,0:2], np.array([[4,0],[4,4]])):
        return "top-left extended"
      elif np.array_equal(object_grid[0:2,1:3], np.array([[0,4],[4,4]])):
        return "top-right extended"
      elif np.array_equal(object_grid[0:2,0:2], np.array([[4,4],[0,4]])):
        return "bottom-left extended"
      else:
        return "bottom-right extended"

def transform(input_grid):
    # Convert input grid to a NumPy array.
    input_grid = np.array(input_grid)

    # Find the yellow object and its bounding box.
    coords, min_coords, max_coords = find_object(input_grid, 4)
    if coords is None:
        return input_grid.tolist()  # Return original if no object is found

    # extract the object
    object_grid = extract_object(input_grid, min_coords, max_coords)

    # determine the orientation
    orientation = determine_orientation(object_grid)

    # rotate the object
    rotated_object = rotate_object(object_grid)

    # flip the rotated object over the x and y axis
    rotated_object = np.flip(rotated_object,0)
    rotated_object = np.flip(rotated_object,1)

    # initialize the output, size of the original object + rotated and flipped object
    out_height = object_grid.shape[0] + rotated_object.shape[0]
    out_width = object_grid.shape[1] + rotated_object.shape[1]
    output_grid = np.zeros((out_height, out_width), dtype=int)

   # place the original object
    og_height, og_width = object_grid.shape
    output_grid[0:og_height, 0:og_width] = object_grid

    # place the rotated object based on orientation
    rotated_height, rotated_width = rotated_object.shape

    if orientation == "top-left" or orientation == "top-left extended":
        output_grid[rotated_height-1:rotated_height-1+rotated_height, rotated_width-1: rotated_width-1+rotated_width] = rotated_object
    elif orientation == "top-right" or orientation == "top-right extended":
        output_grid[rotated_height-1:rotated_height -1 + rotated_height, 0:rotated_width] = rotated_object
    elif orientation == "bottom-left" or orientation == "bottom-left extended":
        output_grid[0:rotated_height, rotated_width-1:rotated_width-1 + rotated_width] = rotated_object
    elif orientation == "bottom-right" or orientation == "bottom-right extended":
        output_grid[0:rotated_height, 0:rotated_width] = rotated_object


    # remove blank columns and rows
    # find the first and last row with yellow pixel
    rows_with_yellow = np.any(output_grid == 4, axis = 1)
    cols_with_yellow = np.any(output_grid == 4, axis = 0)

    first_row_with_yellow = np.argmax(rows_with_yellow)
    last_row_with_yellow = len(rows_with_yellow) - np.argmax(rows_with_yellow[::-1])

    first_col_with_yellow = np.argmax(cols_with_yellow)
    last_col_with_yellow = len(cols_with_yellow) - np.argmax(cols_with_yellow[::-1])

    output_grid = output_grid[first_row_with_yellow:last_row_with_yellow,first_col_with_yellow:last_col_with_yellow]

    return output_grid.tolist()
```
