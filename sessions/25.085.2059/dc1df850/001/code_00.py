"""
Identify all red (2) pixels in the input grid. For each red pixel, examine its 8 neighboring cells (including diagonals). If a neighbor cell is within the grid boundaries and its original color is white (0), change the color of that cell to blue (1) in the output grid. All other cells retain their original color from the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing white neighbors of red pixels to blue.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    # Create a copy to serve as the output grid
    output_array = np.copy(input_array)
    rows, cols = input_array.shape

    # Find the locations of all red (2) pixels
    red_pixels = np.argwhere(input_array == 2)

    # Iterate through each found red pixel
    for r_row, r_col in red_pixels:
        # Iterate through the 3x3 neighborhood around the red pixel
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                # Skip the center pixel itself (the red pixel)
                if dr == 0 and dc == 0:
                    continue

                # Calculate neighbor coordinates
                n_row, n_col = r_row + dr, r_col + dc

                # Check if the neighbor is within the grid boundaries
                if 0 <= n_row < rows and 0 <= n_col < cols:
                    # Check if the neighbor pixel in the *original* input grid was white (0)
                    if input_array[n_row, n_col] == 0:
                        # Change the corresponding pixel in the *output* grid to blue (1)
                        output_array[n_row, n_col] = 1

    # Convert the NumPy array back to a list of lists for the final output
    return output_array.tolist()