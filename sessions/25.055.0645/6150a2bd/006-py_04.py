"""
The transformation rule is a reflection across the line y = x. For every pixel at coordinates (x, y) in the input grid, its corresponding pixel in the output grid is located at coordinates (y, x). This effectively swaps the row and column indices of each pixel.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Get the dimensions of the input grid.
    rows, cols = input_array.shape

    # Create an output array with swapped dimensions.
    output_array = np.empty((cols, rows), dtype=int)

    # Iterate through the input array and swap row/col indices.
    for i in range(rows):
        for j in range(cols):
            output_array[j, i] = input_array[i, j]

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid