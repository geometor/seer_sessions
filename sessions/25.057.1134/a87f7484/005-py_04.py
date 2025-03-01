"""
1.  **Find the Marker:** Locate the azure (color 8) pixel in the input grid.
2.  **Check for 3x3 Block Below:** Check if there's a 3x3 block of identically colored pixels one row below the azure pixel. It does not matter how many rows below, as long as no other pixels are in the way.
3.  **Extract and Output:** If the 3x3 block exists, extract it. This 3x3 block is the output. If there is no block, the output is an empty grid.
"""

import numpy as np

def find_azure_pixel(grid):
    # Find coordinates of azure pixels (color 8)
    azure_coords = np.argwhere(grid == 8)
    if azure_coords.size > 0:
        return azure_coords[0]  # Return the first occurrence
    else:
        return None

def check_3x3_block(grid, start_row, start_col, color):
    # Check if a 3x3 block of the given color exists at the specified location
    if start_row + 3 > grid.shape[0] or start_col + 3 > grid.shape[1]:
        return False  # Out of bounds

    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i, j] != color:
                return False  # Not a uniform 3x3 block
    return True

def extract_3x3_block(grid, row, col):
  # extracts a 3 x 3 block, checking bounds
    if row + 3 > grid.shape[0] or col + 3 > grid.shape[1]:
      return None
    return grid[row:row+3, col:col+3]


def transform(input_grid):
    # initialize output_grid as empty
    input_grid = np.array(input_grid)
    output_grid = np.array([[]])


    # Find the azure marker pixel
    azure_coord = find_azure_pixel(input_grid)

    if azure_coord is not None:
        # Check for 3x3 block below the azure pixel
        azure_row, azure_col = azure_coord
        for row in range(azure_row + 1, input_grid.shape[0] - 2):  # Iterate rows below azure
           for col in range(0, input_grid.shape[1]-2):
              if input_grid[row,col] != 0: # check if non-background
                if check_3x3_block(input_grid, row, col, input_grid[row, col]):
                      output_grid = extract_3x3_block(input_grid, row, col)
                      return output_grid

    return output_grid