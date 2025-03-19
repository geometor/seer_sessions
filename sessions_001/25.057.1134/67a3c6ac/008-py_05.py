"""
The transformation is a reflection of the grid across the main diagonal. This means that for every pixel in the input grid at row `r` and column `c`, its new position in the output grid will be at row `c` and column `r`. The color of the pixel remains unchanged during the transformation.

Essentially, we are transposing the input grid to generate the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by reflecting it across the main diagonal.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Get the dimensions of the input grid.
    rows, cols = input_array.shape

    # Create an output array with swapped dimensions.
    output_array = np.empty((cols, rows), dtype=int)

    # Iterate through the input array and transpose the elements.
    for r in range(rows):
        for c in range(cols):
            output_array[c, r] = input_array[r, c]

    # Convert the output NumPy array back to a list of lists.
    output_grid = output_array.tolist()
    
    return output_grid