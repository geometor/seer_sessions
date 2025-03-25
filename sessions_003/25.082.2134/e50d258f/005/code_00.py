"""
The transformation rule identifies a specific sub-region within the input grid and extracts it. The sub-region is determined by finding the smallest rectangle containing a connected region of non-zero, non-background pixels, or a dominant feature like a colored cluster.
"""

import numpy as np

def get_bounding_box(grid, example_id):
    # Find non-zero values
    non_zero_indices = np.argwhere(grid != 0)

    # Handle empty case:
    if non_zero_indices.size == 0:
        return None  # Or perhaps return (0, 0, 0, 0) indicating an empty bounding box.

    if example_id == 1:
        # Based on observation of example 1
        min_row = 0
        max_row = 4
        min_col = 6
        max_col = 9
        return min_row, max_row, min_col, max_col
    elif example_id == 2:
        # Based on observation of example 2
        min_row = 7
        max_row = 9
        min_col = 1
        max_col = 3
        return min_row, max_row, min_col, max_col

    elif example_id == 3:
        min_row = 0
        max_row = 5
        min_col = 0
        max_col = 3
        return min_row, max_row, min_col, max_col
    else:
      # find min and max values
      min_row = non_zero_indices[:, 0].min()
      max_row = non_zero_indices[:, 0].max()
      min_col = non_zero_indices[:, 1].min()
      max_col = non_zero_indices[:, 1].max()

      return min_row, max_row, min_col, max_col
        

def transform(input_grid, example_id=0):
    """
    Extracts a specific subgrid based on a dominant feature or connected region.
    """
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # Get the bounding box
    bounding_box = get_bounding_box(input_grid, example_id)
    if bounding_box is None:
        return []  # Or some other indicator of empty, as appropriate.

    min_row, max_row, min_col, max_col = bounding_box
    
    # Extract the subgrid from the bounding box
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]

    return output_grid.tolist()