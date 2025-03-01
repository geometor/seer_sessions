"""
1.  **Identify Unique Colors:** Examine the input grid and determine the number of *unique* colors present, *excluding* white (0).
2.  **Count:** If there is one unique color, output that color; if there are two unique colors, output grey (5).
3.  **Output Grid:** Create a 1x1 output grid.
4.  **Set Pixel Color:** Set the value of the output grid's single pixel based on the number of unique colors found in the input.
"""

import numpy as np

def count_unique_colors(grid):
    # Flatten the grid and convert it to a set to get unique colors
    unique_colors = set(grid.flatten())
    # Remove white (0) from the set if it exists
    unique_colors.discard(0)
    return len(unique_colors), unique_colors

def transform(input_grid):
    # Convert input to numpy array
    grid = np.array(input_grid)

    # Count the unique colors (excluding white)
    num_unique_colors, unique_colors_set = count_unique_colors(grid)
    first_color = next(iter(unique_colors_set)) if unique_colors_set else 0

    # Create a 1x1 output grid
    output_grid = np.zeros((1, 1), dtype=int)

    # Set the output pixel color based on the number of unique colors
    if num_unique_colors == 1:
        output_grid[0, 0] = first_color
    elif num_unique_colors == 2:
        output_grid[0, 0] = 5  # Grey
    # else the output remains 0 (white), which is the default

    return output_grid.tolist()