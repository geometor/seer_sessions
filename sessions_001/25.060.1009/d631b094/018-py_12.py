"""
1.  Scan the input grid to identify all non-zero pixels.
2.  Extract the values of these non-zero pixels.
3.  Collect the non-zero pixel values in the order they are encountered, row by row from top-left to bottom-right, and arrange them in a linear sequence.
4.  Create a 1 x N output grid, where 'N' represents the total number of non-zero pixels found.
5.  Populate the output grid with the collected non-zero pixel values, maintaining their order.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)
    
    # Find the indices of non-zero elements.
    non_zero_indices = np.nonzero(input_array)
    
    # Extract the non-zero values, maintaining order (row-major).
    non_zero_values = input_array[non_zero_indices].tolist()
    
    # Create a 1 x N output grid.
    output_grid = np.array(non_zero_values).reshape(1, -1).tolist()
        
    return output_grid