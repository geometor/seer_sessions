"""
The transformation rule extracts all non-zero pixels from the input grid, counts them, and creates a 1 x n output grid where n is the number of non-zero pixels. The output grid is filled with the non-zero pixel values, each repeated as many times as it occurs.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to a NumPy array for easier processing.
    input_array = np.array(input_grid)

    # Find all non-zero pixels.
    non_zero_pixels = input_array[input_array != 0]
    
    # Count the number of non-zero pixels.
    count = len(non_zero_pixels)

    #Create output based on count
    if count > 0:
      output_grid = np.array(non_zero_pixels).reshape(1,count)
    else:
        output_grid = np.array([])
    
    return output_grid.tolist()