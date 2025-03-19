"""
1.  **Identify Azure Region:** Locate all azure (8) colored pixels in the input grid.
2.  **Bounding Box:** Create a bounding box (the `azure_region`) around the outermost azure pixels. This defines a rectangular region.
3.  **Extract Subgrid:** Extract the portion of the input grid (`subgrid`) that falls within the bounding box.
4.  **Resample to 3x3:** Resample the subgrid to a 3x3 output grid. The exact center pixel is determined: ((min_row + max_row)//2, (min_col + max_col) // 2 ).
5.  Set all the values of the output grid to 8.
6.  Set output_grid[1,1] = the value of the `center_pixel`.
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
    output_grid = np.full((3, 3), 8, dtype=int) # Initialize with all 8s

    # Get bounding box of the input azure pixels
    min_row, min_col, max_row, max_col = get_azure_bounding_box(input_grid)

    # Extract the subgrid
    subgrid = input_grid[min_row:max_row+1, min_col:max_col+1]
    
    # compute center pixel of the sub grid
    center_row = (max_row + min_row) // 2
    center_col = (max_col + min_col) // 2

    # Place center pixel in the output
    output_grid[1, 1] = input_grid[center_row, center_col]

    return output_grid