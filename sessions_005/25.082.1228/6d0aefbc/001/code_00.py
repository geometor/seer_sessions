"""
The input grid is mirrored in all directions to produce an output grid of double
minus the original size.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_array = np.array(input_grid)

    # Get dimensions of the input grid
    rows, cols = input_array.shape

    # Create output grid by mirroring
    output_array = np.concatenate((input_array, np.fliplr(input_array)), axis=1)
    output_array = np.concatenate((output_array, np.flipud(output_array)), axis=0)
    
    return output_array.tolist()