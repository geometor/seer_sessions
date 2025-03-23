"""
1.  **Identify the Non-Zero Color:** Scan the input 3x3 grid and identify the single non-zero color value.
2.  **Count Non-Zero Color Occurrences:** count total number of times the non-zero color occurs.
3.  **Construct Output Grid:** Create a 1 x N grid where `N` equals count from step 2, with each cell in the grid being the identified non-zero color.
"""

import numpy as np

def get_nonzero_color(grid):
    # Flatten the grid and remove zeros
    unique_colors = np.unique(grid[grid != 0])
    if len(unique_colors) == 1:
        return unique_colors[0]
    else:
        return None  # Handle cases with no or multiple non-zero colors

def transform(input_grid):
    # Find the non-zero color
    non_zero_color = get_nonzero_color(input_grid)

    if non_zero_color is None:
        return []

    # count occurrences
    count = np.count_nonzero(input_grid == non_zero_color)
    
    # Construct output
    output_grid = np.full((1, count), non_zero_color)

    return output_grid