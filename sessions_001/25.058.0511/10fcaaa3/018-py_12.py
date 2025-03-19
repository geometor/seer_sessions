"""
Identifies yellow pixels in the input grid, mirrors them horizontally across a central vertical axis in an output grid of doubled width, and fills the remaining space with azure.
"""

import numpy as np

def transform(input_grid):
    # Get input grid dimensions
    input_height, input_width = input_grid.shape

    # 1. Initialize Output Grid: Double the width, same height.
    output_height = input_height
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 2. Horizontal Mirroring of Yellow Pixels
    for i in range(input_height):
        for j in range(input_width):
            if input_grid[i, j] == 4:  # Yellow pixel
                # Original position
                output_grid[i, j] = 4
                # Mirrored position (across the central vertical axis of the output grid)
                output_grid[i, output_width - 1 - j] = 4

    # 3. Background Fill with Azure
    for i in range(output_height):
        for j in range(output_width):
            if output_grid[i, j] == 0:  # Empty cell
                output_grid[i, j] = 8  # Fill with azure

    return output_grid