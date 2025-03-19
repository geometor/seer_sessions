# ef135b50 • 020 • refine_coder

---
```python
"""
1.  **Identify** all white pixels (value 0) in the input grid.
2.  **Identify** all red pixels (value 2) in the input grid.
3.  **Check** the edges of the grid for any white pixels adjacent (horizontally or vertically, but *not* diagonally) to a red pixel.
4.  **If** a white pixel is at the edge and adjacent to a red pixel, change its color to maroon (value 9).
5.  **Check** for any white pixels located *between* two red pixels either horizontally or vertically.
6.  **If** a white pixel is located between two red pixels, change its color to maroon (value 9)
7.  **If** a white pixel doesn't meet the above conditions, leave as original color(0).
8.  **Output** the modified grid.
"""

import numpy as np

def get_adjacent_pixels(grid, row, col):
    """Gets the adjacent pixels of a given cell (horizontally and vertically)."""
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

def is_on_edge(grid, row, col):
    """Checks if a pixel is on the edge of the grid."""
    rows, cols = grid.shape
    return row == 0 or row == rows - 1 or col == 0 or col == cols - 1

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel in the input grid
    for row in range(rows):
        for col in range(cols):
            # Identify white pixels (value 0)
            if input_grid[row, col] == 0:
                adjacent = get_adjacent_pixels(input_grid, row, col)
                is_adjacent_to_red = False
                for r, c in adjacent:
                    if input_grid[r, c] == 2:
                        is_adjacent_to_red = True
                        break

                # Check if it's on an edge and adjacent to red
                if is_on_edge(input_grid, row, col) and is_adjacent_to_red:
                    output_grid[row, col] = 9
                elif is_adjacent_to_red: #check if it's between two reds
                    #check horizontal
                    red_count = 0
                    for c in range(cols):
                        if input_grid[row, c] == 2:
                            red_count = red_count + 1
                    if red_count >= 2:
                        output_grid[row,col] = 9
                    #check vertical
                    red_count = 0
                    for r in range(rows):
                        if input_grid[r, col] == 2:
                            red_count = red_count + 1
                    if red_count >= 2:
                        output_grid[row,col] = 9

    return output_grid
```
