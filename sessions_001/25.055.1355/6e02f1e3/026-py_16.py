"""
Identify distinct colors in the input grid. Replace one instance of each color, specifically those lying on the main diagonal (top-left to bottom-right), with gray (5). Fill the remaining cells with white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid according to the described rule.
    """
    # Initialize output grid with the same dimensions, filled with white (0)
    output_grid = np.zeros_like(input_grid)

    # Find unique colors in the input grid
    unique_colors = np.unique(input_grid)

    # Iterate through the grid's main diagonal
    for i in range(input_grid.shape[0]):
        for color in unique_colors:
          if input_grid[i,i] == color:
            output_grid[i,i] = 5 # set to grey
    
    return output_grid