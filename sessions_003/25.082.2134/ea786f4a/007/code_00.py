"""
1.  **Copy:** Create a copy of the input grid to serve as the output grid.
2.  **Border:** Identify all pixels along the outer edge (first row, last row, first column, last column) of the grid.
3.  **Blank Border:** Set the color value of all identified border pixels in the *output* grid to 0 (white).
4.  **Center:** Locate the center pixel of the *input* grid (at row = `rows // 2`, column = `cols // 2`).
5.  **Cross:** Identify the pixels directly above, below, left, and right of the center pixel in the *input* grid. These, along with the center pixel, form the "inner cross".
6.  **Blank Cross:** Set the color value of all identified inner cross pixels in the *output* grid to 0 (white).
7.  **Preserve:** All other pixels in the *output* grid retain their original color values from the *input* grid. This step is implicitly handled because we started with a copy.
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

def get_inner_cross_indices(grid):
    rows, cols = grid.shape
    center_row, center_col = get_center_index(grid)
    inner_cross_indices = []
    if center_row > 0:
        inner_cross_indices.append((center_row - 1, center_col))  # Above
    if center_row < rows - 1:
        inner_cross_indices.append((center_row + 1, center_col))  # Below
    if center_col > 0:
        inner_cross_indices.append((center_row, center_col - 1))  # Left
    if center_col < cols - 1:
        inner_cross_indices.append((center_row, center_col + 1))  # Right
    return inner_cross_indices

def transform(input_grid):
    # initialize output_grid: Create a copy of the input grid.
    output_grid = np.copy(np.array(input_grid))
    rows, cols = output_grid.shape

    # Blank Border: Set border pixels to 0.
    border_indices = get_border_indices(output_grid)
    for r, c in border_indices:
        output_grid[r, c] = 0

    # Blank Cross: Set inner cross pixels to 0.
    inner_cross_indices = get_inner_cross_indices(output_grid)
    for r, c in inner_cross_indices:
        output_grid[r, c] = 0

    # Preserve: Other pixels are implicitly preserved due to the copy.
    return output_grid.tolist()