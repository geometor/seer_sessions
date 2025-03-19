"""
The input grid is rotated 90 degrees clockwise.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array
    input_array = np.array(input_grid)

    # Extract the last row, it stays unchanged
    last_row = input_array[2, :]

    # rotate the remainder of the grid
    rotated_segment = np.rot90(input_array, k=-1) # k=-1 means 90 degrees clockwise

    # assemble the output array - take only the segment above the unchanged last row
    output_array = np.copy(rotated_segment)

    return output_array.tolist()