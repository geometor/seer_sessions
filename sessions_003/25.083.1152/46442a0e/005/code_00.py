"""
The input grid is expanded into a 2x2 tiled output grid. The top-left quadrant of the output grid is a direct copy of the input grid. The top-right quadrant is a horizontal flip of the input grid. The bottom-left quadrant is a vertical flip of the input grid. The bottom-right quadrant is a 180-degree rotation of the input grid.
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

    # 2. Top-Right Quadrant: Horizontal flip of the input grid
    output_grid[:rows, cols:] = np.fliplr(input_grid)

    # 3. Bottom-Left Quadrant: Vertical flip of the input grid
    output_grid[rows:, :cols] = np.flipud(input_grid)

    # 4. Bottom-Right Quadrant: 180-degree rotation of the input grid
    output_grid[rows:, cols:] = np.rot90(input_grid, 2)  # Rotate by 180 degrees (k=2)
    
    return output_grid.tolist()