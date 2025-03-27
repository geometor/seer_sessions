"""
The transformation identifies non-zero pixels in the input grid and swaps each with the pixel located at the reflected position across both the main diagonal and the center of the grid. Zero-valued pixels remain unchanged. The input grid is assumed to be square.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by reflecting and swapping non-zero pixels.
    """
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)
    rows, cols = input_array.shape
    
    # Initialize the output grid as a copy of the input.
    output_array = np.copy(input_array)

    # Iterate through each cell of the input grid.
    for r in range(rows):
        for c in range(cols):
            # Process only non-zero pixels.
            if input_array[r, c] != 0:
                # Calculate the reflected position.
                new_r = cols - 1 - c
                new_c = rows - 1 - r

                # Swap the values.
                output_array[r, c], output_array[new_r, new_c] = input_array[new_r, new_c], input_array[r, c]

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()
    return output_grid