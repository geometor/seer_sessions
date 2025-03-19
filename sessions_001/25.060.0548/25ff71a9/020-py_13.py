"""
The input grid contains a connected shape formed by blue pixels. This shape is rotated 90 degrees clockwise to produce the output grid. The white pixels simply fill the remaining spaces.
"""

import numpy as np

def rotate_clockwise(grid):
    """Rotates a square grid 90 degrees clockwise."""
    return np.rot90(grid, k=-1)

def transform(input_grid):
    # initialize output_grid as a copy of the input grid, ensures that output grid gets correct data type like unit8
    output_grid = np.copy(input_grid)

    # Find the bounding box of the blue pixels
    blue_pixels = np.argwhere(input_grid == 1)
    if blue_pixels.size == 0: # Handle the case where there are no blue pixels
      return output_grid
    
    min_row = np.min(blue_pixels[:, 0])
    max_row = np.max(blue_pixels[:, 0])
    min_col = np.min(blue_pixels[:, 1])
    max_col = np.max(blue_pixels[:, 1])

    # Extract the blue region as a subgrid
    blue_subgrid = input_grid[min_row:max_row+1, min_col:max_col+1]
    
    # determine how much padding is needed based on the shape of the subgrid
    rows, cols = blue_subgrid.shape
    if rows > cols:
        pad_width = ((0,0), (0, rows-cols)) #pad cols
    elif cols > rows:
        pad_width = ((0, cols-rows),(0,0) ) #pad rows
    else:
        pad_width = ((0,0),(0,0))
        
    padded_subgrid = np.pad(blue_subgrid, pad_width=pad_width, mode='constant', constant_values=0 )

    # Rotate the subgrid
    rotated_subgrid = rotate_clockwise(padded_subgrid)

    #remove the padding that was added
    rotated_subgrid = rotated_subgrid[0:rows, 0:cols]
        
    # Create a new output grid filled with white (0)
    output_grid[:] = 0
    # Place the rotated subgrid back into the output grid
    output_grid[min_row:max_row+1, min_col:max_col+1] = rotated_subgrid

    return output_grid