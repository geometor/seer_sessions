"""
1.  **Identify Non-Zero Pixels:** Find all pixels in the input grid that are not black (color 0).
2.  **Single Non-Zero Pixel Check:** If there is only *one* non-zero pixel in the entire input grid.
3. **Fill:** Create an output grid of the same dimensions as the input, and fill the entire output grid with the color of that single non-zero pixel.
"""

import numpy as np

def count_non_zero_pixels(grid):
    """Counts the number of non-zero pixels in a grid."""
    return np.count_nonzero(grid)

def get_non_zero_pixel_color(grid):
    """Gets the color of the first non-zero pixel found in the grid."""
    grid = np.array(grid)
    non_zero_indices = np.nonzero(grid)
    if non_zero_indices[0].size > 0:  # Check if any non-zero pixels exist
        first_non_zero_row = non_zero_indices[0][0]
        first_non_zero_col = non_zero_indices[1][0]
        return grid[first_non_zero_row, first_non_zero_col]
    return 0  # Should not happen given the program logic, but good practice

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # Count non-zero pixels
    num_non_zero = count_non_zero_pixels(input_grid)

    # Check if there's only one non-zero pixel
    if num_non_zero == 1:
        # Get the color of the single non-zero pixel
        color = get_non_zero_pixel_color(input_grid)
        # Fill the output grid with that color
        output_grid[:] = color

    return output_grid.tolist()