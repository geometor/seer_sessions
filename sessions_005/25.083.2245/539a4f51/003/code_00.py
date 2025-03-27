"""
1. Copy: The input grid, excluding its last column, is copied.
2. Stack: Two copies of the section, described at the point 1. are stacked vertically.
3. Append: The input grid, excluding its last column, is replicated, and appendend on the right.
"""

import numpy as np

def transform(input_grid):
    # Convert input to numpy array
    input_array = np.array(input_grid)

    # Get dimensions of input grid, excluding the last column
    rows, cols = input_array.shape
    cols -= 1  # Exclude the last column

    # Create a copy of the input grid excluding the last column
    input_subset = input_array[:, :cols]

    # Stack two copies of the input subset vertically
    stacked_array = np.vstack((input_subset, input_subset))
    
    # Append the input subset to the right of stacked array
    output_array = np.hstack((stacked_array, input_subset))
    
    return output_array.tolist()