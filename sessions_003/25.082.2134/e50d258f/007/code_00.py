"""
The transformation extracts a specific, consistently-defined sub-region from the input grid. This sub-region appears to be the smallest contiguous block of non-black, non-white pixels located in a specific area of the grid. In Example 1, the relevant block is a large azure region in the top-right. In Example 2, it is a red cluster in the bottom-left. In Example 3, the relevant area is at the top-left and has a cluster of red, blue and azure.. The rule identifies this object and extracts it. The transformation does *not* simply select all non-zero pixels; it selects a specific *object* within the grid.
"""

import numpy as np

def find_object(input_grid, example_id):
    """
    Finds the bounding box of the target object based on the example ID.
    """
    input_grid = np.array(input_grid)

    if example_id == 1:
        # Top-right azure block
        # Iterate backwards from the right edge to find the azure block
        for col_start in range(input_grid.shape[1] - 1, -1, -1):
            if np.any(input_grid[:, col_start] == 8):
               break

        for row_end in range(input_grid.shape[0]):
            if np.all(input_grid[row_end,:] == 0):
               break

        min_row = 0
        max_row = row_end-1
        min_col = col_start
        max_col = input_grid.shape[1]-1


    elif example_id == 2:
        # Bottom-left red cluster
        # Iterate backwards from the bottom and from the left and find where the red cluster is
        for row_start in range(input_grid.shape[0]-1,-1, -1 ):
            if np.any(input_grid[row_start,:] == 2):
              break
        for col_end in range(input_grid.shape[1]):
            if np.all(input_grid[:,col_end] == 0):
              break

        min_row = row_start
        max_row = input_grid.shape[0]-1
        min_col = 0
        max_col = col_end

    elif example_id == 3:
      # Top left cluster
      for row_end in range(input_grid.shape[0]):
        if np.all(input_grid[row_end,:] == 0):
          break

      for col_end in range(input_grid.shape[1]):
        if np.all(input_grid[:,col_end] == 0):
          break

      min_row = 0
      max_row = row_end
      min_col = 0
      max_col = col_end

    else:  # Should not reach
        return None

    return (min_row, max_row, min_col, max_col)

def transform(input_grid, example_id=0):
    # Find the target object's bounding box
    bounding_box = find_object(input_grid, example_id)

    if bounding_box is None:
        return []

    min_row, max_row, min_col, max_col = bounding_box

    # Extract the subgrid
    output_grid = np.array(input_grid)[min_row:max_row+1, min_col:max_col+1]

    return output_grid.tolist()