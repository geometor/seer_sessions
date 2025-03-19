"""
1. Identify the Central Object: Locate the contiguous block of non-white pixels (azure and red) in the center of the input grid.
2. Crop: Extract a rectangular region around the central object. The dimensions of the extraction are not immediately obvious from the single example. It removes all of the white background.
3. Rearrange: The cropped section is then potentially re-arranged. In this specific example, the 2x2 red block is moved from the left to the top right part of the output, and other smaller shifts happen, so that all of the red squares are together.
"""

import numpy as np

def find_object(grid):
    # Find non-white pixels
    non_white_pixels = np.argwhere(grid != 0)

    # Get bounding box
    if len(non_white_pixels) > 0:
      min_row = np.min(non_white_pixels[:, 0])
      max_row = np.max(non_white_pixels[:, 0])
      min_col = np.min(non_white_pixels[:, 1])
      max_col = np.max(non_white_pixels[:, 1])
      return (min_row, max_row, min_col, max_col)
    else:
       return None

def transform(input_grid):
    # Find the central object bounding box
    object_bbox = find_object(input_grid)
    
    if object_bbox is None:
      return np.array([])

    min_row, max_row, min_col, max_col = object_bbox

    # Crop the grid
    cropped_grid = input_grid[min_row:max_row+1, min_col:max_col+1]

    # Separate azure and red pixels
    red_pixels = np.argwhere(cropped_grid == 2)
    azure_pixels = np.argwhere(cropped_grid == 8)
    
    # Calculate output dimensions based on cropped size
    output_height = cropped_grid.shape[0]
    output_width = cropped_grid.shape[1]

    # Initialize output grid
    output_grid = np.full((output_height, output_width), 8, dtype=int) # Fill with azure
    
    # Place red pixels at top right
    num_red = len(red_pixels)

    red_placed = 0
    for r in range(output_height):
      for c in range(output_width -1 ,-1,-1):
          if red_placed < num_red:
            output_grid[r,c] = 2
            red_placed+=1
          
    return output_grid