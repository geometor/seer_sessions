"""
1.  **Identify Blue Crosses:** Locate all contiguous blue (1) pixels that form a "+" shape (cross). A cross consists of exactly 5 blue pixels, arranged as a center pixel with four adjacent pixels (up, down, left, right).

2.  **Draw Magenta Lines:**
    -   For each detected blue cross, draw a *horizontal* and a *vertical* magenta (6) line, each 1 pixel wide, passing through the center row and center column.

3.  **Non-intersecting magenta line**:
    - Draw a magenta line that cover the whole rows and cols of the centers of the blue crosses, but not any position occupied by a blue cross.

4.  **Background:** All other pixels remain unchanged.
"""

import numpy as np
from scipy import ndimage

def find_blue_crosses(grid):
    """
    Finds and returns the coordinates of blue crosses in the grid.
    """
    blue_pixels = (grid == 1)
    labeled_grid, num_features = ndimage.label(blue_pixels)
    crosses = []
    for i in range(1, num_features + 1):
        cross_pixels = (labeled_grid == i)
        coords = np.array(np.where(cross_pixels)).T
        # Check if it's a cross (simple heuristic: min_row, max_row, min_col, max_col)
        min_row, min_col = np.min(coords, axis=0)
        max_row, max_col = np.max(coords, axis=0)

        # check the number of element
        if np.sum(cross_pixels) != 5:
            continue

        is_cross = True
        center_row = (min_row+max_row)//2
        center_col = (min_col + max_col) // 2

        if not(grid[center_row,min_col] == 1 and \
               grid[center_row,max_col] == 1 and \
               grid[min_row, center_col] == 1 and \
               grid[max_row, center_col] == 1 and\
               grid[center_row, center_col] == 1):

            is_cross = False
        
        if is_cross:
            crosses.append(((min_row, max_row, min_col, max_col), (center_row,center_col)))
            
    return crosses

def transform(input_grid):
    """
    Transforms the input grid according to the defined rules.
    """
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Find blue crosses
    crosses = find_blue_crosses(input_grid)

    rows, cols = input_grid.shape
    # init magenta lines
    magenta_rows = set()
    magenta_cols = set()

    for cross_info, cross_center in crosses:
        min_row, max_row, min_col, max_col = cross_info
        center_row, center_col = cross_center

        magenta_rows.add(center_row)
        magenta_cols.add(center_col)

    for r in range(rows):
        for c in range(cols):

            if r in magenta_rows or c in magenta_cols:
                 if input_grid[r,c] != 1:
                    output_grid[r,c] = 6
    

    return output_grid