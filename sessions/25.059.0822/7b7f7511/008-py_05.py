"""
The transformation rule is to remove the right-most column from the input grid to produce the output grid. The removed column appears to contain pixels of the same color, although that is an observation and may or may not be relevant. The height of the grid remains unchanged, and the width decreases by one.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_array = np.array(input_grid)
    
    # Get the dimensions of the input grid
    rows, cols = input_array.shape
    
    # Create the output array by slicing the input array, excluding the last column
    output_array = input_array[:, :cols-1]
    
    # Convert the NumPy array back to a list of lists
    output_grid = output_array.tolist()
    
    return output_grid