"""
The transformation involves reflecting the input grid across the X-axis (vertical flip) and then conditionally changing the color of pixels that were originally black (0) to green (3) if they end up in the top-most row after the reflection.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by reflecting it vertically and then conditionally changing the color of
    pixels that were black in the input and end up in the top row post-reflection.
    """
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Reflect the array vertically.
    reflected_array = np.flip(input_array, axis=0)
    
    # Create a copy to serve as the output array.
    output_array = reflected_array.copy()

    # Iterate through the original input grid to find black pixels.
    for r in range(input_array.shape[0]):
        for c in range(input_array.shape[1]):
            if input_array[r, c] == 0:  # Check if the original pixel was black.
                # Check if the reflected position is in the top row.
                if input_array.shape[0] - 1 - r == 0:
                    output_array[0, c] = 3  # Change to green.

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid