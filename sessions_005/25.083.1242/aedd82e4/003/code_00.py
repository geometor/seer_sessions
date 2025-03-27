"""
1. Find all red pixels (value 2).
2. Find all white pixels (value 0).
3. Identify Red Pixels Adjacent to White: From the list of red pixels, identify those that are adjacent (horizontally, vertically, or diagonally) to at least one white pixel.
4. Select Target: If multiple such red pixels exist, select the "lower-right most".  This is the red pixel with the largest row index, and among those, the largest column index. The selection is limited to those that have white neighbors.
5. Transform: Change the color of the selected red pixel to blue (value 1).
6. Output: Return the modified grid.
"""

import numpy as np

def get_adjacent_pixels(grid, row, col):
    """Gets the values of adjacent pixels (including diagonals)."""
    rows, cols = grid.shape
    adjacent = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                adjacent.append((i, j, grid[i, j]))
    return adjacent

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    red_pixels = []
    white_pixels = []

    # Find all red and white pixels
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 2:
                red_pixels.append((r, c))
            elif output_grid[r, c] == 0:
                white_pixels.append((r,c))

    # Find red pixels adjacent to white pixels
    red_adjacent_to_white = []
    for r, c in red_pixels:
        adjacent_pixels = get_adjacent_pixels(output_grid, r, c)
        for ar, ac, val in adjacent_pixels:
            if val == 0:
                red_adjacent_to_white.append((r, c))
                break  # Move to the next red pixel if one white neighbor is found

    # Select the lower-right most red pixel among those adjacent to white
    target_pixel = None
    if red_adjacent_to_white:
        max_row = -1
        for r, c in red_adjacent_to_white:
            if r > max_row:
                max_row = r
                target_pixel = (r, c)
            elif r == max_row:
                if c > target_pixel[1]:
                    target_pixel = (r, c)

    # change output pixels
    if target_pixel:
        output_grid[target_pixel[0], target_pixel[1]] = 1

    return output_grid