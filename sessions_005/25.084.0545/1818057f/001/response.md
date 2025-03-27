```python
"""
Iterate through each pixel in the input grid.
Identify yellow (4) pixels.
For each yellow (4) pixel, check for adjacent red (2) pixels (horizontally or vertically).
If a yellow (4) pixel has one or more adjacent red(2) pixels, then that yellow pixel will be changed to azure(8).
Output the modified grid.
"""

import numpy as np

def get_adjacent_pixels(grid, row, col):
    # helper to get adjacent pixel coords
    rows, cols = grid.shape
    adjacent_pixels = []
    if row > 0:
        adjacent_pixels.append((row - 1, col))  # Up
    if row < rows - 1:
        adjacent_pixels.append((row + 1, col))  # Down
    if col > 0:
        adjacent_pixels.append((row, col - 1))  # Left
    if col < cols - 1:
        adjacent_pixels.append((row, col + 1))  # Right
    return adjacent_pixels

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Check if the current pixel is yellow (4)
            if output_grid[row, col] == 4:
                # Get adjacent pixel coordinates
                adjacent_coords = get_adjacent_pixels(output_grid, row, col)
                # Check for adjacent red (2) pixels
                for r, c in adjacent_coords:
                    if output_grid[r, c] == 2:
                        # Replace yellow with azure (8)
                        output_grid[row, col] = 8
                        break  # Only need one adjacent red to trigger change

    return output_grid
```