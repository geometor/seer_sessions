"""
Rotate the input grid 90 degrees clockwise.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_np = np.array(input_grid)

    # Rotate the grid 90 degrees clockwise.
    output_np = np.rot90(input_np, k=-1)

    # Convert the NumPy array back to a list.
    output_grid = output_np.tolist()

    return output_grid