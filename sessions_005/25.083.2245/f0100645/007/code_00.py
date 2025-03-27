"""
For each row in the input grid, identify the leftmost pixel's color (the "seed" color).
Iterate through the remaining pixels in the row, from left to right.
If the current pixel's color is different from the seed color, count the length of the consecutive pixels that match the current color, starting from the current pixel.
If the count is greater than or equal to 2, do not change the current pixel.
If the count is less than 2, change the current pixel to the seed color.
The modified grid is the output. The end of a row also blocks propagation.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by propagating the leftmost pixel's color across each row,
    stopping when a run of different colors of length 2 or more is encountered.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    for r in range(rows):
        seed_color = output_grid[r, 0]  # Get the leftmost pixel's color

        for c in range(1, cols):
            if output_grid[r, c] != seed_color:
                # Count consecutive pixels of the same color
                run_length = 0
                for k in range(c, cols):
                    if output_grid[r,k] == output_grid[r,c]:
                        run_length +=1
                    else:
                        break

                if run_length < 2:
                    if c < cols: # end of line
                       output_grid[r,c] = seed_color
            # else current pixel is seed_color, continue

    return output_grid