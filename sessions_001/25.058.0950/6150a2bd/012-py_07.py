"""
The input grid is rotated 90 degrees counter-clockwise to produce the output grid. Each pixel in the input grid retains its original color/value and is repositioned according to the 90-degree counter-clockwise rotation. The dimensions of the output grid are determined by the rotation of the input grid.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees counter-clockwise.
    output_array = np.rot90(input_array, k=1)

    # Convert the result back to a list.
    return output_array.tolist()