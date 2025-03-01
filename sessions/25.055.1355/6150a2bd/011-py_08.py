"""
The grid is reflected across the main diagonal (top-left to bottom-right).
This is equivalent to swapping the row and column indices of each pixel (i, j) -> (j, i).
The background color (8) remains unchanged. The foreground pixels (color 0) are moved to their reflected position.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array.
    input_np = np.array(input_grid)

    # Transpose the NumPy array to reflect across the main diagonal.
    output_np = input_np.transpose()

    # Convert the NumPy array back to a list.
    output_grid = output_np.tolist()

    return output_grid