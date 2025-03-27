"""
The transformation extracts the outer border of a shape within a 6x6 input grid,
removes diagonally connected pixels, and presents it within a 5x5 output grid.
The center 3x3 region of the output grid is filled with color 0.
"""

import numpy as np

def transform(input_grid):
    # Initialize a 5x5 output grid filled with 0s.
    output_grid = np.zeros((5, 5), dtype=int)

    # Create a border from the input, excluding corner elements.
    for i in range(6):
        for j in range(6):
            if input_grid[i, j] == 8:  #consider only '8' colored parts
                # Map 6x6 coordinates to 5x5, adjusting for border removal
                # Top and Bottom borders
                if i == 0 and j > 0 and j < 5:
                    output_grid[0, j-1] = 8
                elif i == 1 and (j == 0 or j == 5):
                    output_grid[0,j] = input_grid[i,j]
                elif i == 5 and j > 0 and j < 5:
                    output_grid[4, j - 1] = 8
                elif i == 4 and (j == 0 or j==5):
                    output_grid[4,j] = input_grid[i,j]
                #left and right

                elif j == 0 and i > 0 and i < 5:
                    output_grid[i-1, 0] = 8
                elif j == 1 and (i == 0 or i == 5):
                    output_grid[i,0] = input_grid[i,j]
                elif j == 5 and i > 0 and i < 5:
                    output_grid[i - 1, 4] = 8
                elif j == 4 and (i == 0 or i ==5):
                    output_grid[i,4] = input_grid[i,j]

    return output_grid