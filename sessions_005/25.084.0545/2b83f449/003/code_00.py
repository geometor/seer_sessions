"""
1.  **Identify Objects:** The scene consists of three primary objects: a border object formed by connected pixels of colors 3 and 8, an irregular object with color 7, and the background with color 0.

2.  **Border State Change:** Within the border object, pixels of color 8 change to color 3, and pixels of color 3 change to color 8.

3.  **Color Replacement:** All pixels of color 7 (the irregular object) change to color 6.

4.  **Adjacent Propagation:** Any pixel of color 8 that is adjacent to a pixel of color 6 changes to color 6. This propagation continues until no more color 8 pixels are adjacent to color 6 pixels. The propagation should check *all* newly changed 6s, not just the original ones.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    # Use numpy to find coordinates of all pixels matching the given color.
    return np.argwhere(grid == color)

def get_adjacent_pixels(grid, row, col):
    # returns the adjacent pixels to (row, col) but NOT including (row, col)
    height, width = grid.shape
    adjacent_pixels = []
    for i in range(max(0, row - 1), min(height, row + 2)):
        for j in range(max(0, col - 1), min(width, col + 2)):
            if (i, j) != (row, col):
                adjacent_pixels.append((i, j))
    return adjacent_pixels

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Border State Change (3 <-> 8)
    border_8_pixels = find_pixels_by_color(input_grid, 8)
    for row, col in border_8_pixels:
        # check if part of the border by checking for 3 and 8 neighbors
        adj_pix = get_adjacent_pixels(input_grid,row,col)
        is_border = False
        for r, c in adj_pix:
            if input_grid[r,c] == 3:
                is_border = True
                break
        if is_border:
          output_grid[row, col] = 3

    border_3_pixels = find_pixels_by_color(input_grid, 3)
    for row, col in border_3_pixels:
        # check if part of the border by checking for 3 and 8 neighbors
        adj_pix = get_adjacent_pixels(input_grid,row,col)
        is_border = False
        for r, c in adj_pix:
            if input_grid[r,c] == 8:
                is_border = True
                break
        if is_border:
          output_grid[row,col] = 8

    # Color Replacement (7 -> 6)
    orange_pixels = find_pixels_by_color(input_grid, 7)
    for row, col in orange_pixels:
        output_grid[row, col] = 6

    # Adjacent Propagation (8 -> 6 near 6)
    while True:
        magenta_pixels = find_pixels_by_color(output_grid, 6)
        new_magenta_pixels = []
        for row, col in magenta_pixels:
            adjacent_pixels = get_adjacent_pixels(output_grid, row, col)
            for adj_row, adj_col in adjacent_pixels:
                if output_grid[adj_row, adj_col] == 8:
                    new_magenta_pixels.append((adj_row, adj_col))

        if not new_magenta_pixels:
            break  # Exit loop if no new magenta pixels were found

        for row, col in new_magenta_pixels:
            output_grid[row, col] = 6

    return output_grid