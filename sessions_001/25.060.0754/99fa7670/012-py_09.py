"""
1.  **Identify Non-Zero Pixels:** Locate all pixels in the input grid that have a non-zero color value.
2.  **Create 2x2 Squares:** For *each* non-zero pixel found in the input grid, create a 2x2 square in the output grid. The top-left corner of this 2x2 square should be at the same location as the original non-zero pixel in the input grid. The 2x2 square will consist of four pixels, all having the same color as the original input pixel.
3. **All Other Pixels**: All other pixels in the output grid that are not part of a created 2x2 square should have a value of 0 (white).
"""

import numpy as np

def find_non_zero_pixels(grid):
    """Finds the coordinates of all non-zero pixels in a grid."""
    non_zero_coords = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] != 0:
                non_zero_coords.append((i, j))
    return non_zero_coords

def transform(input_grid):
    # Initialize the output grid with zeros and the same dimensions as the input.
    output_grid = np.zeros_like(input_grid)

    # Find the coordinates of all non-zero pixels.
    non_zero_coords = find_non_zero_pixels(input_grid)

    # Iterate through the non-zero pixel coordinates.
    for i, j in non_zero_coords:
        # Get the color of the current non-zero pixel.
        color = input_grid[i, j]

        # Create a 2x2 square in the output grid.
        output_grid[i:i+2, j:j+2] = color

    return output_grid