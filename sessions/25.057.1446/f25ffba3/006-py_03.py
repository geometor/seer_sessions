"""
1.  **Identify Target Columns:** Find the columns containing the color pairs [9, 3] (maroon, green) and [2, 4] (red, yellow). We'll refer to these as `column_9_3` and `column_2_4`, respectively.

2.  **Vertical Flip within Target Columns:** Within `column_9_3` and `column_2_4`, *only* vertically flip the order of the pixels that are part of the target color pairs (9, 3 and 2, 4). Other colored pixels within these columns should remain in their original positions.

3.  **Column Swap:** Swap the entire contents of `column_9_3` with `column_2_4`.
"""

import numpy as np

def find_colored_columns(grid, colors):
    rows, cols = grid.shape
    found_cols = []
    for c in range(cols):
        for r in range(rows):
            if grid[r, c] in colors:
                found_cols.append(c)
                break  # Move to the next column once a color is found
    return sorted(list(set(found_cols)))

def vertical_flip_target_colors(grid, col, colors):
    """Flips the target colors vertically within a single column, leaving others unchanged."""
    rows = grid.shape[0]
    target_pixels = []
    other_pixels = []

    # Separate target and other colored pixels
    for r in range(rows):
        if grid[r, col] in colors:
            target_pixels.append((r, grid[r, col]))
        elif grid[r,col] != 0:
            other_pixels.append((r,grid[r,col]))

    # Reverse target pixels and update the column
    if target_pixels:
        target_pixels.reverse()
        for i, (r, color) in enumerate(target_pixels):
            grid[r, col] = color

    return grid

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Identify Target Columns
    cols_9_3 = find_colored_columns(input_grid, [9, 3])
    cols_2_4 = find_colored_columns(input_grid, [2, 4])
  

    # Vertical Flip within Target Columns
    for col in cols_9_3:
        output_grid = vertical_flip_target_colors(output_grid, col, [9, 3])
    for col in cols_2_4:
        output_grid = vertical_flip_target_colors(output_grid, col, [2, 4])
        
    #column swap
    if (len(cols_2_4) > 0) and (len(cols_9_3) > 0):
        #get the values for the columns
        temp_c24 = output_grid[:,cols_2_4[0]].copy()
        temp_c93 = output_grid[:,cols_9_3[0]].copy()
      
        #copy to the swapped columns
        output_grid[:,cols_2_4[0]] = temp_c93
        output_grid[:,cols_9_3[0]] = temp_c24

    return output_grid