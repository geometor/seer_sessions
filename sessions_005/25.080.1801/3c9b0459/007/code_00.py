"""
The transformation rule is a 180-degree rotation of the input grid. This can be achieved by reversing the order of the rows and then reversing the order of elements within each row, or vice versa. The color of each pixel remains unchanged; only its position is altered according to the rotation.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the array by 180 degrees.  We can achieve this by flipping
    # the array both vertically and horizontally.
    rotated_array = np.flip(np.flip(input_array, 0), 1)

    # Convert the rotated array back to a list.
    output_grid = rotated_array.tolist()

    return output_grid