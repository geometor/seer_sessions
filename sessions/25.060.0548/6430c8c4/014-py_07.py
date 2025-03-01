"""
1. **Extract Subgrid:** Identify the dimensions of the upper-left colored object composed by same-colored contiguous cells. From the input grid, extract the 4x4 subgrid from the top-left corner of input.
2.  **Transform Colors:**
    *   If an orange (7) pixel is present in the original input, set the cells with relative coordinates to green(3), else it's a white cell(0).
"""

import numpy as np

def get_object_dimensions(grid):
    """Find the dimensions of top-left colored object."""
    rows, cols = grid.shape
    first_color = grid[0,0]
    height = 0
    width = 0

    for r in range(rows):
        if grid[r,0] == first_color:
            height+=1
        else:
            break

    for c in range(cols):
        if grid[0,c] == first_color:
            width +=1
        else:
            break
    return height, width

def transform(input_grid):
    # Initialize numpy arrays for input grid
    input_grid = np.array(input_grid)

    #get object_dimensions
    height, width = get_object_dimensions(input_grid)
    # Initialize output_grid
    output_grid = np.zeros((height, width), dtype=int)

    # Find orange color
    orange_coords = np.argwhere(input_grid == 7)

    if len(orange_coords) >0:
      #transform orange to green, rest to white.
        for r in range(height):
            for c in range(width):
                output_grid[r,c] = 3


    return output_grid.tolist()