"""
Expands non-white pixels horizontally until they encounter another non-white pixel.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by expanding non-white pixels horizontally.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row
    for r in range(rows):
        # Iterate through each pixel in the row
        for c in range(cols):
            # Check if the pixel is non-white
            if input_grid[r, c] != 0:
                # Expand to the right
                for c_right in range(c + 1, cols):
                    if input_grid[r, c_right] == 0:
                        output_grid[r, c_right] = input_grid[r, c]
                    else:
                        break  # Stop when hitting another non-white pixel
                #Expand to the left
                for c_left in range(c -1, -1, -1):
                    if input_grid[r, c_left] == 0:
                        output_grid[r,c_left] = input_grid[r,c]
                    else:
                        break

    return output_grid