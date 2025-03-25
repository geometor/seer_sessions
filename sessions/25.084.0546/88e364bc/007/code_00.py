"""
The transformation rule swaps 0 and 4 based on adjacent colors.

1.  **Initialization:** Create an output grid that is an exact copy of the input grid.
2.  **Iteration:** Examine each pixel in the input grid.
3. **Conditional Swap**
    - if a pixel is 0 and any of the directly adjacent pixels (up, down, left, right) is 4 or 5, change the pixel to 4 in the output grid.
    - if a pixel is 4 and any of the directly adjacent pixels (up, down, left, right) is 0 or 5, change the pixel to 0 in the output grid.
4. All other pixels are copied to the output grid unchanged.
"""

import numpy as np

def get_adjacent_pixels(grid, row, col):
    """Gets the values of directly adjacent pixels (up, down, left, right)."""
    rows, cols = grid.shape
    adjacent = []
    if row > 0:
        adjacent.append(grid[row - 1, col])  # Up
    if row < rows - 1:
        adjacent.append(grid[row + 1, col])  # Down
    if col > 0:
        adjacent.append(grid[row, col - 1])  # Left
    if col < cols - 1:
        adjacent.append(grid[row, col + 1])  # Right
    return adjacent

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            pixel_value = input_grid[row, col]
            adjacent_values = get_adjacent_pixels(input_grid, row, col)

            # Conditional Swap Logic
            if pixel_value == 0 and (4 in adjacent_values or 5 in adjacent_values):
                output_grid[row, col] = 4
            elif pixel_value == 4 and (0 in adjacent_values or 5 in adjacent_values):
                output_grid[row, col] = 0

    return output_grid