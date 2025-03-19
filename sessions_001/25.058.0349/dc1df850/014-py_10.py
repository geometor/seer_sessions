"""
1. Locate the Red Pixel: Find the single pixel in the input grid that has a value of 2 (red).
2. Preserve Red: Copy the red pixel from the input grid to the same location in the output grid.
3. Check Neighbors: For the red pixel, examine its four immediate neighbors (up, down, left, and right).
4. Transform Adjacent Pixels:
    *   If a neighboring pixel in the input grid has a value of 0 (white) and is directly adjacent to the red pixel, change its value to 1 (blue) in the output grid.
    *   If a pixel is not directly adjacent to the red one, keep the output value same as input.
"""

import numpy as np

def find_pixel_by_value(grid, value):
    # Find the coordinates of a pixel with a specific value.
    rows, cols = np.where(grid == value)
    if len(rows) > 0:
        return rows[0], cols[0]  # return first if multiple
    return None

def is_valid(row, col, grid_shape):
    #check that a coordinate is within bounds
    return 0 <= row < grid_shape[0] and 0 <= col < grid_shape[1]

def get_adjacent_pixels(row, col, grid_shape):
    # Get the coordinates of adjacent pixels (up, down, left, right)

    adjacent = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_row, new_col = row + dr, col + dc
        if is_valid(new_row, new_col, grid_shape):
            adjacent.append((new_row, new_col))
    return adjacent

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    grid_shape = input_grid.shape

    # Find the red pixel
    red_pixel_coords = find_pixel_by_value(input_grid, 2)

    if red_pixel_coords:
        # Preserve red pixel (already done by copying)

        # Check neighbors
        adjacent_pixels = get_adjacent_pixels(red_pixel_coords[0], red_pixel_coords[1], grid_shape)

        # Transform adjacent white pixels to blue
        for r, c in adjacent_pixels:
            if input_grid[r, c] == 0:
                output_grid[r, c] = 1

    return output_grid