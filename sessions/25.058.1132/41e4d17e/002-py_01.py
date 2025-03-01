"""
1.  **Identify Blue Crosses:** Locate all contiguous blue (1) shapes that form a "cross" or "+" shape.
2.  **Draw Magenta Line:**
    - the blue cross is enclosed by a vertical and horizontal magenta line of 1 pixel width
    - the magenta line fills the entire row and column that are not occupied by any blue cross.
3. **Background Remains:** The remaining azure (8) background pixels remain unchanged.

In the examples shown, in case there are more than one crosses, they form a pattern where one cross and a corresponding intersecting magenta line forms a quadrant.
"""

import numpy as np

def find_blue_crosses(grid):
    # Find contiguous blue (1) regions and identify those that form a cross shape
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