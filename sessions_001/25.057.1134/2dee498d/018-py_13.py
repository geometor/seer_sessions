"""
The transformation identifies and extracts a repeating vertical pattern from the input grid. In each output example this repeating pattern is two pixels wide:

1.  Examine the input grid.
2.  Identify the smallest repeating vertical pattern, two pixels wide, starting from the top left corner.
3.  Extract this pattern to create the output grid. The output has same number of rows.
"""

import numpy as np

def transform(input_grid):
    # Get the dimensions of the input grid.
    rows, cols = input_grid.shape

    # Initialize the output grid with the same number of rows and a width of 2 (for the repeating pattern).
    output_grid = np.zeros((rows, 2), dtype=int)

    # Extract the first two columns as the repeating pattern.
    output_grid[:, 0] = input_grid[:, 0]
    output_grid[:, 1] = input_grid[:, 1]
    
    return output_grid