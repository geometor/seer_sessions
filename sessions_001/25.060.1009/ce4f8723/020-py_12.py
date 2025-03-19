"""
1. **Locate 4x4 Region:** Find the largest contiguous 4x4 region of a single non-zero color in the input grid.
2. **Recolor:** Create a 4x4 output grid. If a 4x4 region was found in step 1, fill the output grid with green (3).  If no such region was found, the output should be all zeros (which is how it's initialized, so no action is needed).
"""

import numpy as np

def find_4x4_region(input_grid):
    """
    Searches for a 4x4 region of a single, non-zero color.
    Returns the color and top-left coordinates if found, otherwise None.
    """
    rows, cols = input_grid.shape
    for r in range(rows - 3):
        for c in range(cols - 3):
            color = input_grid[r, c]
            if color != 0:
                # Check if all cells in the 4x4 region have the same color
                is_uniform = True
                for i in range(4):
                    for j in range(4):
                        if input_grid[r + i, c + j] != color:
                            is_uniform = False
                            break
                    if not is_uniform:
                        break
                if is_uniform:
                    return color, (r, c)
    return None, None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((4, 4), dtype=int)

    # find 4x4 region
    color, top_left = find_4x4_region(input_grid)

    # change output pixels 
    if top_left:
        for i in range(4):
          for j in range(4):
            output_grid[i,j] = 3

    return output_grid