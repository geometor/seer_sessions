# 67a423a3 • 020 • refine_coder

---
```python
"""
1.  **Identify** the blue (1) square object in the input grid.
2.  **Locate** all pixels directly adjacent (up, down, left, right - not diagonally) to the blue square.
3.  **Change** the color of those adjacent pixels that are white (0) to yellow (4).
4.  **Propagate** the yellow color: For every yellow pixel, check its directly adjacent neighbors. If any of them are white (0), change them to yellow (4) as well.  Repeat this step until no more white pixels can be changed to yellow.
5. **Preserve** the color of the blue pixels.
6.  **Output** the modified grid.
"""

import numpy as np

def get_adjacent_pixels(grid, row, col):
    """
    Gets the coordinates of directly adjacent pixels (up, down, left, right).
    """
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

def propagate_color(grid, start_pixels, initial_color, target_color):
    """
    Propagates the target color from the starting pixels to connected pixels of the initial color.
    """
    rows, cols = grid.shape
    output_grid = np.copy(grid)
    pixels_to_check = start_pixels.copy()

    while pixels_to_check:
        current_pixel = pixels_to_check.pop()
        row, col = current_pixel

        if output_grid[row, col] == initial_color:
            output_grid[row, col] = target_color
            neighbors = get_adjacent_pixels(grid, row, col)
            for neighbor in neighbors:
                if output_grid[neighbor[0],neighbor[1]] == initial_color:
                  pixels_to_check.append(neighbor)


    return output_grid

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find blue pixels and their adjacent pixels
    blue_pixels = []
    adjacent_to_blue = []
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 1:
                blue_pixels.append((row, col))
                adjacent_pixels = get_adjacent_pixels(input_grid, row, col)
                for adj_row, adj_col in adjacent_pixels:
                    if input_grid[adj_row,adj_col] == 0:
                      adjacent_to_blue.append((adj_row, adj_col))

    # Propagate yellow color from adjacent_to_blue
    output_grid = propagate_color(output_grid, adjacent_to_blue, 0, 4)
    

    return output_grid
```
