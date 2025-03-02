# d406998b • 004 • example_1 • investigate_coder

---
```python
"""
Transforms the input grid by changing some gray (5) pixels to green (3) based on their adjacency to other gray and white pixels.
Specifically, a gray pixel is changed to green if it's directly adjacent to exactly two other gray and one white pixels.
"""

import numpy as np

def get_adjacent_pixels(grid, row, col):
    """Gets the values of the adjacent pixels, handling edge cases."""
    rows, cols = grid.shape
    adjacent = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):  # Exclude the pixel itself
                adjacent.append(grid[i, j])
    return adjacent

def transform(input_grid):
    """
    Applies the color change to pixels based on their color and adjacency.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 5:  # Check if the pixel is gray
                adjacent_pixels = get_adjacent_pixels(input_grid, row, col)
                gray_count = adjacent_pixels.count(5)
                white_count = adjacent_pixels.count(0)

                # adjacent pixels are either diagonal or side by side
                side_by_side_or_diagonal = 0
                if gray_count + white_count >=1:
                  side_by_side_or_diagonal = 1
                
                # if input_grid[row, col] == 5 is adjacent to exactly two 5 and one 0:
                if gray_count == 2 and white_count == 1 and side_by_side_or_diagonal == 1:
                  output_grid[row, col] = 3  # Change to green
                elif gray_count == 1 and white_count == 2 and side_by_side_or_diagonal == 1:
                  output_grid[row, col] = 3

    return output_grid
```
