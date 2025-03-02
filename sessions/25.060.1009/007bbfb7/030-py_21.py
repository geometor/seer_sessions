"""
Expands the input grid by a factor of 3, replicating the input pattern and filling the remaining cells with zeros.
"""

import numpy as np

def transform(input_grid):
    # Get input grid dimensions
    input_height, input_width = input_grid.shape

    # Calculate output grid dimensions
    output_height = input_height * 3
    output_width = input_width * 3

    # Initialize output grid with zeros
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Iterate through the input grid and replicate the pattern in the output grid
    for i in range(input_height):
      for j in range(input_width):
        for x in range(3):
          for y in range(3):
            output_grid[i*3 + x, j * 3 + y] = input_grid[i,j]

    return output_grid