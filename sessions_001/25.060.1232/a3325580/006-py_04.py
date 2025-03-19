"""
The transformation identifies the unique non-zero colors in the input grid.  The output grid's width and height are equal to the number of unique colors. Each column in the output grid represents a unique color, and the column is filled entirely with that color.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)

    # find distinct non zero colors
    colors = sorted(list(set(input_grid.flatten())))
    colors = [c for c in colors if c!= 0]

    num_colors = len(colors)
    output_grid = np.zeros((num_colors, num_colors), dtype=int)

    # change output pixels
    for j, color in enumerate(colors):
        for i in range(num_colors):
            output_grid[i, j] = color

    return output_grid.tolist()