"""
The input grid is divided into three vertical rectangular regions: red (left), grey (middle), and yellow (right).
White pixels in the grey region are propagated to the red region in the same row. White pixels in the yellow region remain unchanged.
"""

import numpy as np

def get_regions(grid):
    """
    Divides the grid into three vertical regions based on color.
    """
    rows, cols = grid.shape
    red_region = []
    grey_region = []
    yellow_region = []
    for r in range(rows):
      for c in range(cols):
        if grid[r,c] == 2:
          red_region.append((r,c))
        if grid[r,c] == 5:
          grey_region.append((r,c))
        if grid[r,c] == 4:
            yellow_region.append((r,c))
    return red_region, grey_region, yellow_region
    

def transform(input_grid):
    """
    Transforms the input grid according to the rule: white pixels in the grey region are 
    propagated to the red region in the same row, while white pixels in the yellow region stay.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Get regions coordinates
    red_region, grey_region, yellow_region = get_regions(input_grid)

    # Find white pixels and apply transformation
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 0:  # Found a white pixel
                if (r,c) in yellow_region:
                    # Keep white pixel in the same position
                    output_grid[r, c] = 0
                if (r,c) in grey_region:
                    # find the column that starts the red region, for the current row
                    c_red = -1
                    for c_scan in range(cols):
                      if (r,c_scan) in red_region:
                        c_red = c_scan
                        break
                    if c_red>=0:
                      output_grid[r,c_red] = 0


    return output_grid