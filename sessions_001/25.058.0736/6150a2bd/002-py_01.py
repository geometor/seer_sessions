"""
The input is a 3x3 grid of numbers. Rotate the entire grid 90 degrees clockwise. The resulting rotated grid is the output.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array
    input_np = np.array(input_grid)

    # Rotate the grid 90 degrees clockwise
    output_np = np.rot90(input_np, k=-1)  # k=-1 for clockwise rotation

    # Convert the NumPy array back to a list
    output_grid = output_np.tolist()

    return output_grid