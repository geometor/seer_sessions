"""
The transformation involves reflecting the grid across its center. Elements are swapped with their symmetric counterparts, but only once to avoid double-swapping.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array
    input_array = np.array(input_grid)
    rows, cols = input_array.shape
    output_array = np.copy(input_array)

    # Iterate through "half" of the elements of the input array to avoid double-swapping
    for i in range(rows):
        for j in range(cols):
            # Calculate the indices of the symmetrically opposite element
            sym_i = rows - 1 - i
            sym_j = cols - 1 - j

            # Only swap if we are in the "upper-left" half of the grid,
            #  or along the center row/column but only the left half
            if (i < sym_i) or (i == sym_i and j < sym_j):
                # Swap the elements
                output_array[i, j], output_array[sym_i, sym_j] = input_array[sym_i, sym_j], input_array[i, j]

    # Convert the NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid