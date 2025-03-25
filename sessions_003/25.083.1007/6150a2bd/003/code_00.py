"""
1. Rotate: Rotate the input grid 180 degrees clockwise. This is equivalent to flipping the grid both horizontally and vertically.
2. Reverse Rows: Reverse the order of elements within each row.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array
    input_array = np.array(input_grid)

    # Rotate the array 180 degrees clockwise (which is equivalent to two flips)
    rotated_array = np.rot90(input_array, 2)

    # Reverse each row of the rotated array
    output_array = np.array([row[::-1] for row in rotated_array])
    
    # Convert back to list
    output_grid = output_array.tolist()

    return output_grid