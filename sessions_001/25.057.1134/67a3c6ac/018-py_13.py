"""
The transformation rule is determined by comparing the input and output grids. The program checks for two types of transformations:

1.  Identity: The input grid remains unchanged.
2.  Transpose: The input grid is reflected across the main diagonal (rows and columns are swapped).

If an output grid is provided, the function determines which transformation (if any) matches the provided output. If no output grid is provided, it returns the input unchanged.
"""

import numpy as np

def transform(input_grid, output_grid=None):
    # Convert input to numpy array
    input_array = np.array(input_grid)

    # If output_grid is provided, determine the transformation type
    if output_grid:
        output_array = np.array(output_grid)
        if input_array.shape == output_array.shape and np.all(input_array == output_array):
            # Identity transformation
            return input_grid.copy()
        elif input_array.shape == output_array.T.shape and np.all(input_array == output_array.T):
            # Transpose transformation
            return input_array.T.tolist()
        else:
            # Default to identity if no match is found
            return input_grid.copy()
    else:
        # If no output_grid, return input_grid unchanged
        return input_grid.copy()