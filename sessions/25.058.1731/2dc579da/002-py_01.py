"""
The transformation identifies the most frequent color in each row and column, treating it as the background color.
It then removes any rows and columns composed entirely of this background color,
resulting in a smaller grid containing only the non-background elements.
"""

import numpy as np

def get_background_color(grid):
    # Flatten the grid to a 1D array
    flat_grid = grid.flatten()

    # Find unique colors and their counts
    unique_colors, counts = np.unique(flat_grid, return_counts=True)

    # Find the color with the maximum count (most frequent)
    background_color = unique_colors[np.argmax(counts)]
    return background_color

def transform(input_grid):
    # Convert input grid to a NumPy array for easier manipulation.
    grid = np.array(input_grid)
    
    # Get the background color.
    background_color = get_background_color(grid)

    # Remove background rows.
    rows_to_keep = []
    for i, row in enumerate(grid):
        if not np.all(row == background_color):
            rows_to_keep.append(i)
    grid = grid[rows_to_keep]
    
    # Remove background columns
    cols_to_keep = []
    for j in range(grid.shape[1]):
      if not np.all(grid[:, j] == background_color):
        cols_to_keep.append(j)
    
    output_grid = grid[:, cols_to_keep]

    return output_grid.tolist()