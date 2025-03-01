# 794b24be • 044 • example_8 • investigate_coder

---
```python
"""
Iterate through each pixel in the input grid.
Check neighbors. Examine the colors in the input grid.
    If the pixel is blue (1) and any horizontally or vertically adjacent pixel is also blue (1), change the pixel's color to red (2) in the output grid. If the current pixel has no blue neighbors it is not changed.
    If all of a blue pixel's neighbors are white, it remains blue.
Copy Unchanged: If a pixel is white (0) in the input grid, it remains white (0) in the output grid.
Top Row: Copy only the top row if the left most, middle and right most pixels are all blue.
Middle Row: If the center pixel is white with a blue pixel to its left, it changes to red.
Bottom Row: If bottom left and right corner pixels are blue, they are changed to white.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Get the neighbors of a pixel."""
    neighbors = []
    rows, cols = grid.shape
    if row > 0:
        neighbors.append(grid[row - 1, col])  # Up
    if row < rows - 1:
        neighbors.append(grid[row + 1, col])  # Down
    if col > 0:
        neighbors.append(grid[row, col - 1])  # Left
    if col < cols - 1:
        neighbors.append(grid[row, col + 1])  # Right
    return neighbors

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel in the input_grid
    for row in range(rows):
        for col in range(cols):
            # Get the current pixel's color
            current_color = input_grid[row, col]
            # Get the neighboring pixels' colors
            neighbors = get_neighbors(input_grid, row, col)

            # Apply the transformation rules
            if current_color == 1:  # If the pixel is blue
                if 1 in neighbors:  # and any neighbor is blue
                  output_grid[row,col] = 2

            if row == 1 and col == 1: # center pixel
                if input_grid[row, col-1] == 1 and current_color == 0:
                    output_grid[row, col] = 2

            if row == rows - 1:
                if (col == 0 or col == cols -1) and current_color == 1:
                    output_grid[row, col] = 0
    return output_grid
```
