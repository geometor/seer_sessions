# aedd82e4 • 020 • example_4 • investigate_coder

---
```python
"""
Identify red pixels in the input grid. Then, find white pixels that are diagonally adjacent to any red pixels (or below). Change the color of these white pixels to blue. All other pixels remain unchanged.
"""

import numpy as np

def get_diagonally_adjacent_and_down_pixels(grid, row, col):
    """
    Gets the coordinates of pixels that are diagonally adjacent (or directly below) to a given pixel.
    """
    rows, cols = grid.shape
    adjacent_coords = []

    # Diagonal neighbors (and below).
    for dr in [-1, 1]:
        for dc in [-1, 1]:
            if 0 <= row + dr < rows and 0 <= col + dc < cols:
                adjacent_coords.append((row + dr, col + dc))
    # one directly below
    if 0 <= row+1 < rows and 0 <= col < cols:
        adjacent_coords.append((row + 1, col))

    return adjacent_coords

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through all pixels.
    for row in range(rows):
        for col in range(cols):
            # Identify red pixels.
            if input_grid[row, col] == 2:
                # Get diagonally adjacent (and directly below) pixel coordinates.
                adjacent_coords = get_diagonally_adjacent_and_down_pixels(input_grid, row, col)
                # Change color of adjacent white pixels to blue.
                for adj_row, adj_col in adjacent_coords:
                    if input_grid[adj_row, adj_col] == 0:
                        output_grid[adj_row, adj_col] = 1

    return output_grid
```
