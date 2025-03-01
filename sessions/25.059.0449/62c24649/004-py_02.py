"""
The input grid is expanded to double its original dimensions. The original grid is then copied
into the center of the expanded grid. A border, one pixel wide, is created around the copied
grid. The color of this border is the same as the color of the top-left pixel of the original input grid.
"""

import numpy as np

def transform(input_grid):
    # Get dimensions of input grid
    input_height, input_width = input_grid.shape

    # Create output grid with double the dimensions
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Determine border color (top-left pixel of input)
    border_color = input_grid[0, 0]

    # Fill border
    output_grid[0, :] = border_color  # Top row
    output_grid[-1, :] = border_color # Bottom row
    output_grid[:, 0] = border_color  # Left column
    output_grid[:, -1] = border_color # Right column

    # Copy input grid to the center of output grid
    output_grid[1:input_height+1, 1:input_width+1] = input_grid

    return output_grid