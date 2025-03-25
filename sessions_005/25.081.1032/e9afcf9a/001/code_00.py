"""
The transformation takes two rows of numbers and interleaves them in an alternating pattern, row by row. The first row of the output grid is created by taking alternating values from the first and second input rows, beginning with the first input row. The second row is created by alternating values from the first and second input rows, starting with the second input row.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)
    
    # Get dimensions of the input grid
    rows, cols = input_grid.shape
    
    # Initialize output_grid with the same dimensions
    output_grid = np.zeros((rows, cols), dtype=int)

    # Fill the first row of the output grid by alternating values
    for i in range(cols):
        output_grid[0, i] = input_grid[i % 2, i]

    # Fill the second row of the output grid by alternating values, starting from the second row
    for i in range(cols):
        output_grid[1, i] = input_grid[(i + 1) % 2, i]

    return output_grid.tolist()