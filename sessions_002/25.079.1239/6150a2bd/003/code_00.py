"""
The input grid is transformed to the output grid by rotating the entire grid by 180 degrees. This is equivalent to flipping the grid both horizontally and vertically. The colors of the pixels remain unchanged; only their positions are altered according to the rotation.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by rotating it 180 degrees.
    """
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Rotate the array 180 degrees (k=2 for 90-degree rotations).
    output_array = np.rot90(input_array, k=2)

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid