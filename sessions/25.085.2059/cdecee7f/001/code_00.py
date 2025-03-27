"""
Extracts all non-white pixels from the input grid by scanning column by column, top to bottom.
Places these extracted pixels into a 3x3 output grid, filling row by row, left to right.
If there are fewer than 9 non-white pixels, the remaining cells in the 3x3 grid are filled with white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the described rule.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 3x3 numpy array representing the transformed output grid.
    """
    input_height, input_width = input_grid.shape
    output_size = 3

    # 1. Initialize an empty list to store the non-white pixels
    extracted_pixels = []

    # 2. Iterate through the columns of the input grid (left to right)
    for col in range(input_width):
        # 3. Within each column, iterate through the rows (top to bottom)
        for row in range(input_height):
            pixel_value = input_grid[row, col]
            # 4. If the current pixel's value is not white (0), add it to the list
            if pixel_value != 0:
                extracted_pixels.append(pixel_value)

    # 5. Create a new 3x3 grid, initialized with white (0) pixels
    output_grid = np.zeros((output_size, output_size), dtype=int)

    # 6. Iterate through the cells of the 3x3 output grid (row by row, left to right)
    pixel_index = 0
    for r_out in range(output_size):
        for c_out in range(output_size):
            # 7. If there are still pixels remaining in the list, place the next one
            if pixel_index < len(extracted_pixels):
                output_grid[r_out, c_out] = extracted_pixels[pixel_index]
                pixel_index += 1
            # 8. Otherwise, the cell remains white (0) due to initialization

    # 9. Return the filled 3x3 output grid
    return output_grid
