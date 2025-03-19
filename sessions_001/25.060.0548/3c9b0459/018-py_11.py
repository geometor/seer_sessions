"""
The output grid is created by reflecting the input grid across its vertical central axis. Each pixel in the input grid is mirrored to the opposite side, maintaining its distance from the central vertical axis. This is equivalent to a horizontal flip.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Flip the array horizontally (left-right).
    output_array = np.fliplr(input_array)

    # Convert the NumPy array back to a list.
    output_grid = output_array.tolist()

    return output_grid