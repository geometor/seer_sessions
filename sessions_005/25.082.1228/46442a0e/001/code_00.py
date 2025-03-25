"""
The input grid is expanded into a larger grid where both dimensions (rows and columns) are doubled. 
The output grid is composed of four quadrants. The top-left quadrant is the original input grid.
The top-right quadrant is a horizontally mirrored copy of the input grid.
The bottom-left quadrant is a vertically mirrored copy of the input grid.
The bottom-right quadrant is a diagonally mirrored copy of the input grid (mirrored both horizontally and vertically).
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
    output_grid[:rows, cols:] = mirror_horizontal(input_grid)
    # Bottom-left: vertically mirrored input grid
    output_grid[rows:, :cols] = mirror_vertical(input_grid)
    # Bottom-right: diagonally mirrored input grid
    output_grid[rows:, cols:] = mirror_horizontal(mirror_vertical(input_grid))

    return output_grid.tolist()