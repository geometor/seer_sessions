"""
The input grid is expanded into a larger grid where each dimension (rows and columns) is doubled. The output grid is composed of four quadrants:

1.  **Top-Left Quadrant:** This quadrant is identical to the original input grid.
2.  **Top-Right Quadrant:** This quadrant is a horizontally mirrored copy of the *input grid* (flipped left-to-right).
3.  **Bottom-Left Quadrant:** This quadrant is a vertically mirrored copy of the *input grid* (flipped top-to-bottom).
4.  **Bottom-Right Quadrant:** This quadrant is a horizontally mirrored copy of the *bottom-left quadrant*, which is also a vertically mirrored copy of the *top-right quadrant*. Equivalently, the bottom-right quadrant is constructed by mirroring the *top-left quadrant* on *both* the x and y axes.
"""

import numpy as np

def mirror_horizontal(grid):
    return np.fliplr(grid)

def mirror_vertical(grid):
    return np.flipud(grid)

def transform(input_grid):
    # Convert input grid to numpy array
    input_grid = np.array(input_grid)

    # Get dimensions of input grid
    rows, cols = input_grid.shape

    # Create output grid with doubled dimensions
    output_grid = np.zeros((rows * 2, cols * 2), dtype=int)

    # Fill the quadrants of the output grid
    # Top-left: original input grid
    output_grid[:rows, :cols] = input_grid
    # Top-right: horizontally mirrored input grid
    top_right = mirror_horizontal(input_grid)
    output_grid[:rows, cols:] = top_right
    # Bottom-left: vertically mirrored input grid
    bottom_left = mirror_vertical(input_grid)
    output_grid[rows:, :cols] = bottom_left
    # Bottom-right: horizontally mirrored bottom-left
    output_grid[rows:, cols:] = mirror_horizontal(bottom_left)

    return output_grid.tolist()