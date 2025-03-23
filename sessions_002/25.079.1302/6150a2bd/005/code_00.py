"""
Rotate the input grid 90 degrees clockwise, mirror the rotated grid vertically, and then sort the columns of the mirrored grid in descending order based on the cell values.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array
    input_array = np.array(input_grid)

    # Rotate the input grid 90 degrees clockwise
    rotated_array = np.rot90(input_array, k=-1)

    # Mirror/Flip the rotated grid vertically
    mirrored_array = np.flipud(rotated_array)

    # Sort columns in descending order
    num_cols = mirrored_array.shape[1]
    sorted_cols = []
    for i in range(num_cols):
        col = mirrored_array[:, i]
        sorted_cols.append(col.tolist())

    sorted_cols.sort(key=lambda x: tuple(x), reverse=True)

    # reconstruct the output
    output_array = np.array(sorted_cols).T
    
    return output_array.tolist()