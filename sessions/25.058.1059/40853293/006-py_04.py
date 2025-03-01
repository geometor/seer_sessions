"""
1.  **Identify Seed Pixels:** Find all *single* pixels of colors red, azure, magenta, gray, green, and white. A single pixel is defined as a pixel that does *not* have an adjacent neighbor (up, down, left, or right) of the same color.

2.  **Red Extension:** If a single red pixel is found, extend it vertically upwards to the top edge of the grid, changing those pixels to red.

3.  **Azure Extension:** If a single azure pixel is found, extend it vertically downwards to the bottom edge of the grid, changing those pixels to azure.

4.  **Magenta Extension:** If a single magenta pixel exists, extend it by *one* pixel horizontally in *both* directions (left and right).

5.  **Gray Extension:** If a single gray pixel is found, *and* if that pixel is on row index 3 or greater, extend it downwards to the bottom.

6.  **Green Extension:** If a single green pixel if found, extend it to the right until it makes the green object to 4 pixels long in total.

7.  **White Extension:** If a single white pixel if found, extend it to the right until it makes the white object to 7 pixels long in total.
"""

import numpy as np

def find_single_pixels(grid):
    """Finds single pixels of specified colors (not directly adjacent to same color)."""
    single_pixels = {}
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0:  # Non-background
                is_single = True
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == color:
                        is_single = False
                        break
                if is_single:
                    if color not in single_pixels:
                      single_pixels[color] = (r, c)
    return single_pixels

def transform(input_grid):
    # Initialize output grid as a copy
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find single pixels
    single_pixels = find_single_pixels(input_grid)

    # Red Extension
    if 2 in single_pixels:
        r, c = single_pixels[2]
        for i in range(r):
            output_grid[i, c] = 2

    # Azure Extension
    if 8 in single_pixels:
        r, c = single_pixels[8]
        for i in range(r + 1, rows):
            output_grid[i, c] = 8

    # Magenta Extension
    if 6 in single_pixels:
        r, c = single_pixels[6]
        if c - 1 >= 0:
            output_grid[r, c - 1] = 6
        if c + 1 < cols:
            output_grid[r, c + 1] = 6

    # Gray Extension
    if 5 in single_pixels:
        r, c = single_pixels[5]
        if r >= 3:
            for i in range(r + 1, rows):
                output_grid[i, c] = 5
    
    # Green Extension
    if 3 in single_pixels:
        r, c = single_pixels[3]
        for i in range(1,4):
            if c+i < cols:
                output_grid[r,c+i] = 3
    
    # White Extension
    if 0 in single_pixels:
        r,c = single_pixels[0]
        for i in range(1,7):
            if c + i < cols:
                output_grid[r, c + i] = 0


    return output_grid