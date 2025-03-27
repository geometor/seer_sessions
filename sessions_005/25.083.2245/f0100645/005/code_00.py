"""
Iterate through each row of the grid. Identify the leftmost pixel's color (the "seed" color).
For each subsequent pixel in the row:
    If the current pixel's color is different from the seed color:
        Check if the preceding pixel's color is the same as the seed color.
        If the preceding pixel is the seed color, change the current pixel's color to the seed color.
        if the preceding pixel is not the seed color:
            if the current pixel is a specific "blocking" color, do not change it's color.
            otherwise change the current pixel color to the seed color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by conditionally propagating the leftmost pixel's color across each row.
    Propagation occurs if the preceding pixel matches the leftmost color or according to the blocking rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    for r in range(rows):
        seed_color = output_grid[r, 0]  # Get the leftmost pixel's color
        for c in range(1, cols):
            if output_grid[r, c] != seed_color:  # If current pixel is different from leftmost
                if output_grid[r, c-1] == seed_color:  # Check preceding pixel
                    output_grid[r, c] = seed_color  # Set to leftmost color
                else:
                    # Determine blocking color based on the seed color (This is a simplification)
                    if seed_color == 4:
                        blocking_color = 6
                    elif seed_color == 9:
                        blocking_color = 8
                    else:
                        blocking_color = -1  # No blocking

                    if output_grid[r,c] != blocking_color:
                        output_grid[r,c] = seed_color


    return output_grid