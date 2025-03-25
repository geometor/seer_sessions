"""
1.  **Identify the Border:** Determine the pixels constituting the outer perimeter (first and last rows and columns) of the input grid.
2.  **Identify the Center:** Locate the pixel at the center of the grid (at row = rows // 2, column = cols // 2).
3.  **Transform Border Pixels:** Set the color of all border pixels to 0 (white) in the output grid.
4.  **Retain Inner, Non-Center Pixels**: Copy the color of all inner pixels that *aren't* the center pixel to the same position in the output grid.
5. **Retain Center Pixel**: Copy the color of the center pixel to the same position in the output grid.
"""

import numpy as np

def get_border_indices(grid):
    rows, cols = grid.shape
    border_indices = []
    for r in range(rows):
        for c in range(cols):
            if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                border_indices.append((r, c))
    return border_indices

def get_center_index(grid):
    rows, cols = grid.shape
    center_row = rows // 2
    center_col = cols // 2
    return (center_row, center_col)

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # change border pixels to 0
    border_indices = get_border_indices(input_grid)
    for r, c in border_indices:
        output_grid[r, c] = 0

    # get center index
    center_row, center_col = get_center_index(input_grid)
    
    # retain inner, non-center and center pixels   
    for r in range(rows):
        for c in range(cols):
            if (r,c) not in border_indices:
                output_grid[r,c] = input_grid[r,c]

    return output_grid.tolist()