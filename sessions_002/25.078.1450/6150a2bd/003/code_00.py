"""
The transformation rule is a 180-degree rotation of the input grid. This is achieved by first reversing the order of elements within each row (horizontal flip) and then reversing the order of the rows themselves (vertical flip). The output grid has the same dimensions as the input grid, but the elements are repositioned according to the rotation.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Reverse each row (horizontal flip).
    reversed_rows = [row[::-1] for row in input_array]

    # Reverse the order of the rows (vertical flip).
    output_array = np.array(reversed_rows[::-1])

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid