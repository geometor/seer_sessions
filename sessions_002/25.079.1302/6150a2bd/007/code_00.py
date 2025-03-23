"""
The input grid is rotated 90 degrees clockwise, mirrored vertically, and then the rows are reordered such that the original bottom row becomes the top, the original top row becomes the bottom, and the middle row remains in place.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array
    input_array = np.array(input_grid)

    # Rotate the input grid 90 degrees clockwise
    rotated_array = np.rot90(input_array, k=-1)

    # Mirror/Flip the rotated grid vertically
    mirrored_array = np.flipud(rotated_array)

    # Reorder rows: bottom to top, top to bottom, middle stays
    num_rows = mirrored_array.shape[0]
    if num_rows == 3:
      output_array = np.array([mirrored_array[2], mirrored_array[1], mirrored_array[0]])
    else: # in case the input has different size
      output_array = mirrored_array

    return output_array.tolist()