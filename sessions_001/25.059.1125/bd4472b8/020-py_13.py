"""
The transformation rule replicates each row of the input grid three times in the output grid. The output grid's height is three times the input grid's height, while the width remains the same.
"""

import numpy as np

def transform(input_grid):
    # Get dimensions of the input grid.
    input_height, input_width = input_grid.shape
    
    # Calculate dimensions of the output grid.
    output_height = input_height * 3
    output_width = input_width

    # Initialize the output grid with the calculated dimensions.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through the input rows and replicate each three times.
    for i in range(input_height):
        for j in range(3):
            output_grid[i * 3 + j] = input_grid[i]

    return output_grid