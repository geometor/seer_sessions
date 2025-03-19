"""
The input grid is expanded horizontally. A mirrored copy of the input grid is created and appended to the right side of the original input, effectively doubling the width.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by horizontally mirroring it.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Create a mirrored copy of the input array.
    mirrored_array = np.fliplr(input_array)

    # Concatenate the original and mirrored arrays horizontally.
    output_array = np.concatenate((input_array, mirrored_array), axis=1)

    # Convert the NumPy array back to a list.
    output_grid = output_array.tolist()

    return output_grid