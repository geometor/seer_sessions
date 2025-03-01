"""
If the input grid's height is not equal to its width, rotate the grid 90 degrees clockwise. Otherwise, if the height and width are equal, the output grid is identical to the input grid (no transformation).
"""

import numpy as np

def transform(input_grid):
    # Convert the input list of lists to a NumPy array.
    input_array = np.array(input_grid)
    input_height, input_width = input_array.shape

    # Check if height and width are unequal.
    if input_height != input_width:
        # Rotate the array 90 degrees clockwise.
        output_array = np.rot90(input_array, k=-1)
    else:
        # Identity transformation: output is the same as the input.
        output_array = input_array

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()
    
    return output_grid