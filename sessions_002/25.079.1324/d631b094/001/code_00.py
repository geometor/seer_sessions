"""
Extracts the non-zero colored pixels from the input grid and forms a contiguous block of those pixels in the output grid.
The output grid's dimensions are determined by the number of non-zero pixels, creating a shape as close to a square as possible.
"""

import numpy as np

def get_nonzero_color(grid):
    # find the non zero color
    for row in grid:
        for cell in row:
            if cell != 0:
                return cell
    return 0

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_grid = np.array(input_grid)

    # Identify the non-zero color
    non_zero_color = get_nonzero_color(input_grid)


    # Count the number of non-zero pixels
    count = np.count_nonzero(input_grid)

    # Determine output grid dimensions
    if count == 0:
      return []
    
    if count == 1:
        width = 1
        height = 1
    elif count == 2:
        width = 2
        height = 1
    elif count == 3:
        width = 3
        height = 1
    elif count == 4:
        width = 2
        height = 2
    elif count == 5:  # special handling since a perfect square isn't possible
      width = 5
      height = 1 # default to a row
    elif count == 6:
      width = 3
      height = 2
    elif count == 7:
      width = 7
      height = 1 # default to row
    elif count == 8:
      width = 4
      height = 2 # keep closest to a square
    elif count == 9:
        width = 3
        height = 3
    else:
        width = int(count**0.5) # will it ever get here? not with 3 x 3
        height = (count + width - 1) // width

    # Create output grid and fill with the non-zero color
    output_grid = np.full((height, width), non_zero_color, dtype=int)

    return output_grid.tolist()