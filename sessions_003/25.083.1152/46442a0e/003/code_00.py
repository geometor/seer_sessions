"""
The input grid is expanded into a 2x2 tiled output grid. The top-left quadrant of the output grid is a direct copy of the input grid. The top-right, bottom-left, and bottom-right quadrants are filled with the color of the top-left pixel of the input grid.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Initialize output_grid with double the dimensions of the input
    output_grid = np.zeros((rows * 2, cols * 2), dtype=int)

    # 1. Top-Left Quadrant: Copy the input grid
    output_grid[:rows, :cols] = input_grid

    # Get the fill color from the top-left pixel of the input grid
    fill_color = input_grid[0, 0]

    # 2. Top-Right Quadrant: Fill with the top-left pixel's color
    output_grid[:rows, cols:] = fill_color

    # 3. Bottom-Left Quadrant: Fill with the top-left pixel's color
    output_grid[rows:, :cols] = fill_color

    # 4. Bottom-Right Quadrant: Fill with the top-left pixel's color
    output_grid[rows:, cols:] = fill_color
    
    return output_grid.tolist()