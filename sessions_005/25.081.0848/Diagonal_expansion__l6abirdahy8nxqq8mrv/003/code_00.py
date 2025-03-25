"""
For each non-white pixel in the input grid, draw a cross of that color in the output grid, centered at the same row and column. The arms of the cross extend outwards until they encounter a white pixel or the edge of the grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.zeros_like(input_grid)

    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r, c] != 0:
                color = input_grid[r, c]
                output_grid[r, c] = color  # Set center pixel

                # Horizontal Expansion
                # Rightward
                for i in range(c + 1, input_grid.shape[1]):
                    if input_grid[r, i] == 0:
                        break
                    output_grid[r, i] = color
                # Leftward
                for i in range(c - 1, -1, -1):
                    if input_grid[r, i] == 0:
                        break
                    output_grid[r, i] = color

                # Vertical Expansion
                # Downward
                for i in range(r + 1, input_grid.shape[0]):
                    if input_grid[i, c] == 0:
                        break
                    output_grid[i, c] = color
                # Upward
                for i in range(r - 1, -1, -1):
                    if input_grid[i, c] == 0:
                        break
                    output_grid[i, c] = color

    return output_grid