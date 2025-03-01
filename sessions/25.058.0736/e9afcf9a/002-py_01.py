"""
The transformation rule is to create a checkerboard-like pattern. The output grid retains the same dimensions as the input grid (2x6).  The colors, green (3) and maroon (9) from the input, alternate in the output grid. The top-left cell of the output grid has the same color as the top-left cell of the input grid (green/3).  Within each row, adjacent cells have different colors. Within each column, adjacent cells have different colors.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid with the same dimensions as the input grid
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.zeros((rows, cols), dtype=int)

    # get the colors from the input grid
    colors = [input_grid[0][0], input_grid[1][0]]

    # change output pixels to create an alternating pattern
    for i in range(rows):
        for j in range(cols):
            # alternate colors based on row and column index
            output_grid[i][j] = colors[(i + j) % 2]

    return output_grid