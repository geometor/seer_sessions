"""
The transformation rule extracts a sub-grid containing only the non-zero pixels,
removing the surrounding "whitespace" (pixels with value 0) while preserving
the core pattern of the colored pixels.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to a NumPy array
    input_array = np.array(input_grid)

    # Find rows and columns that are not all zeros
    non_zero_rows = np.any(input_array != 0, axis=1)
    non_zero_cols = np.any(input_array != 0, axis=0)

    # Extract the sub-grid based on non-zero rows and columns
    output_array = input_array[non_zero_rows][:, non_zero_cols]

    return output_array.tolist()