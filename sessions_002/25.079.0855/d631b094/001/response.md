```python
"""
Find the non-zero color present in the input grid, examine which edge has that color, count it, and create an output grid filled with that color of that size.
"""

import numpy as np

def get_non_zero_color(grid):
    # find unique colors, exclude 0 (white), and return the first one.
    unique_colors = np.unique(grid)
    non_zero_colors = unique_colors[unique_colors != 0]
    if non_zero_colors.size > 0:
        return non_zero_colors[0]
    else:
        return 0

def count_color_along_edge(grid, color):
    rows, cols = grid.shape
    row_count = 0
    col_count = 0

    # Check rows
    for r in range(rows):
        if color in grid[r, :]:
            row_count += np.count_nonzero(grid[r,:] == color)

    # Check columns
    for c in range(cols):
        if color in grid[:, c]:
             col_count += np.count_nonzero(grid[:,c] == color)
    
    return row_count, col_count
    

def transform(input_grid):
    # initialize output_grid

    # Find the non-zero color
    non_zero_color = get_non_zero_color(input_grid)
    
    if non_zero_color == 0:
        return np.array([])  # Return empty if no non-zero color.

    # Count the color on edge
    row_count, col_count = count_color_along_edge(input_grid, non_zero_color)
    
    
    # create output
    if row_count > 0 and col_count > 0:
      # both, take sum
        output_grid = np.full((row_count + col_count), non_zero_color)
    elif row_count > 0:
      # only rows
        output_grid = np.full((row_count), non_zero_color)
    elif col_count > 0:
        # only cols
        output_grid = np.full((col_count), non_zero_color)
    else:
        return np.array([])

    return output_grid
```