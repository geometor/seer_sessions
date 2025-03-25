"""
Transforms a 5x5 input grid into a 10x10 output grid. The transformation
replicates the input grid in the top-left corner and constructs the rest of
the output grid based on the border, inner, and center colors of the input
grid. The top half consists of the replicated input and columns of the
border, inner, and center colors in a specific pattern. The bottom half has
a more intricate pattern based on those three colors.
"""

import numpy as np

def get_colors(input_grid):
    border_color = input_grid[0, 0]
    center_color = input_grid[2, 2]
    for i in range(5):
        for j in range(5):
            if input_grid[i,j] != border_color and input_grid[i, j] != center_color:
                inner_color = input_grid[i,j]
                return border_color, inner_color, center_color
    return border_color, None, center_color

def transform(input_grid):
    # Initialize output_grid
    output_grid = np.zeros((10, 10), dtype=int)

    # Identify Colors
    border_color, inner_color, center_color = get_colors(input_grid)

    # Create Building Blocks (Planes)
    plane1 = np.copy(input_grid)  # Plane 1: Original input grid
    plane2 = np.full((5, 1), border_color, dtype=int)  # Plane 2: Border color column
    plane3 = np.full((5, 1), inner_color, dtype=int)  # Plane 3: Inner color column
    plane4 = np.full((5, 1), center_color, dtype=int)  # Plane 4: Center color column

    # Construct Top Half (Rows 0-4)
    output_grid[0:5, 0:5] = plane1  # Place Plane 1
    output_grid[0:5, 5:6] = plane2  # Place Plane 2
    output_grid[0:5, 6:7] = plane4  # Place Plane 4
    output_grid[0:5, 7:8] = plane3  # Place Plane 3
    output_grid[0:5, 8:9] = plane2  # Place Plane 2
    output_grid[0:5, 9:10] = plane4 # Place Plane 4

   # Construct Bottom Half (rows 5-9)
    sequence = [border_color, center_color, inner_color, border_color, center_color]
    for i in range(5):
        for j in range(5):
            output_grid[5 + i, j] = sequence[i]

    output_grid[5:9, 5] = inner_color
    output_grid[7:9, 6] = inner_color
    output_grid[8, 7] = inner_color

    output_grid[9,5] = center_color
    output_grid[9,6] = border_color
    output_grid[9,7] = border_color
    output_grid[9,8] = border_color
    output_grid[9,9] = center_color

    return output_grid