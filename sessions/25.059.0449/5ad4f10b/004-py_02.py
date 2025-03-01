"""
1.  **Identify Azure Pixels:** Examine the input grid and locate all pixels with the value "8" (azure).

2.  **Bounding Box (Hypothesis):** It is possible that a bounding box around the azure colored pixels is a key idea. I will need more example pairs to test the bounding box idea. If true, create a bounding box around the outter most azure colored pixels.

3.  **Resize to Output:** Resample/Resize the Bounding box contents, into a 3x3 output grid. The method is not clear at this time.

4.  **Eliminate other colors** Set all non-azure (8) pixels to be white (0).
"""

import numpy as np

def get_azure_bounding_box(grid):
    # Find coordinates of all azure pixels
    azure_coords = np.argwhere(grid == 8)
    
    if azure_coords.size == 0:  # Handle the case with no azure pixels
        #default
        min_row, min_col = 0,0
        max_row, max_col = 2,2
        return min_row, min_col, max_row, max_col

    # Find minimum and maximum row and column
    min_row = np.min(azure_coords[:, 0])
    max_row = np.max(azure_coords[:, 0])
    min_col = np.min(azure_coords[:, 1])
    max_col = np.max(azure_coords[:, 1])

    return min_row, min_col, max_row, max_col


def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)  # Convert to NumPy array
    output_grid = np.zeros((3, 3), dtype=int)

    # Get bounding box of the input azure pixels
    min_row, min_col, max_row, max_col = get_azure_bounding_box(input_grid)
    
    # compute the height and width
    height = max_row - min_row + 1
    width = max_col - min_col + 1

    if height < 3 and width < 3:
      # place into the output grid
      for row_add in range(height):
        for col_add in range(width):
          output_grid[row_add, col_add] = 8

    else:
        # place azure pixels in the corners and center of the output grid
        output_grid[0, 0] = 8
        output_grid[0, 2] = 8
        output_grid[2, 0] = 8
        output_grid[2, 2] = 8
        output_grid[1,1] = 8 if input_grid[ (min_row + max_row)//2,  (min_col+max_col)//2] == 8 else 0

    return output_grid