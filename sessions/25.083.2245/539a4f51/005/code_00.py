"""
1. Isolate Input: Take the input grid and remove its last column.
2. Replicate: Create an exact copy of the grid resulting from step 1.
3. Append: Append the copy from Step 2, to the right of the grid resulting from Step 1.
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

    # Append the input subset to the right of itself
    output_array = np.hstack((input_subset, input_subset))
    
    return output_array.tolist()