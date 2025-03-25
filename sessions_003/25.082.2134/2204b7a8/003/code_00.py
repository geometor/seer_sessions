"""
1.  **Preserve Top and Bottom Rows:** Copy the top and bottom rows of the input grid directly to the output grid without modification.
2.  **Determine the Dividing Line:**
    *   If the grid has an odd number of rows, the "middle row" is the row exactly in the center. No changes occur to this row.
    *   If the grid has an even number of rows, the dividing line is conceptually between the two central rows.
3. **Iterate through inner rows** Iterate through rows between top and dividing line, and dividing line and bottom row.
4.  **Conditional Pixel Replacement (Top Half):**
    *   For each pixel in rows *above* the middle row (or dividing line), check its color.
    *   If the pixel's color is *not* 0, *and* it's different from *both* the top row's color *and* the bottom row's color, change the pixel's color to match the top row's color.
5.  **Conditional Pixel Replacement (Bottom Half):**
    *   For each pixel in rows *below* the middle row (or at/below the dividing line), check its color.
    *    If the pixel's color is *not* 0, *and* it is different from the top and the bottom row color then change it to match the bottom row color.
6. **Middle Row:** If the grid has odd number of rows, do not modify the middle row.
"""

import numpy as np

def get_top_bottom_colors(grid):
    """Gets the colors of the top and bottom rows."""
    top_color = grid[0, 0]  # Assume uniform color in the top row
    bottom_color = grid[-1, 0]  # Assume uniform color in the bottom row
    return top_color, bottom_color

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # get top and bottom row colors
    top_color, bottom_color = get_top_bottom_colors(input_grid)

    # determine dividing line
    if rows % 2 == 0:
        middle_row = rows // 2
    else:
        middle_row = rows // 2

    # iterate and conditionally replace (top half)
    for r in range(1, middle_row):
        for c in range(cols):
            if input_grid[r, c] != 0 and input_grid[r, c] != top_color and input_grid[r, c] != bottom_color:
                output_grid[r, c] = top_color

    # iterate and conditionally replace (bottom half)
    for r in range(middle_row if rows %2 == 0 else middle_row + 1, rows - 1):
        for c in range(cols):
            if input_grid[r, c] != 0 and input_grid[r, c] != top_color and input_grid[r, c] != bottom_color:
                output_grid[r, c] = bottom_color
    
    return output_grid