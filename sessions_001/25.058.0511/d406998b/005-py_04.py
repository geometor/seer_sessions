"""
1. **Identify the background:** In all examples, the most prevalent color inside any black border/frame is considered the "background" (gray (5) in all provided examples).
2.  **Apply the green rule:** Starting from the third pixel in each row and taking every other background pixel, change the background pixel color to green (3).
"""

import numpy as np

def get_background_color(grid):
    # Find unique colors and their counts
    unique, counts = np.unique(grid, return_counts=True)
    
    # Create a dictionary of color: count
    color_counts = dict(zip(unique, counts))

    # Exclude black (0) if present, as it's likely a border
    if 0 in color_counts:
        del color_counts[0]
    # if no colors besides black, then black is background
    if len(color_counts) == 0:
        return 0

    # Return the color with the maximum count
    return max(color_counts, key=color_counts.get)

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = input_grid.copy()
    background_color = get_background_color(input_grid)

    # Iterate through each row of the grid
    for row_index in range(output_grid.shape[0]):
        # Apply the green rule: start at the 3rd pixel (index 2)
        for col_index in range(2, output_grid.shape[1], 2):
            if output_grid[row_index, col_index] == background_color:
                output_grid[row_index, col_index] = 3  # Change to green

    return output_grid