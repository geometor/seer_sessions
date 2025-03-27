"""
For each row in the input grid, find the color of the first non-white (0) pixel encountered when scanning from left to right. If this 'source_color' is neither white (0) nor gray (5), then replace all gray (5) pixels in that same row of the output grid with this 'source_color'. Otherwise, leave the row unchanged (gray pixels remain gray).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on a row-specific color replacement rule.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Create a copy of the input grid to modify and return as the output
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Iterate through each row of the grid
    for r in range(height):
        source_color = 0  # Initialize source_color for the row to white (0)

        # Find the first non-white color in the current row
        for c in range(width):
            pixel_color = input_grid[r, c]
            if pixel_color != 0:
                source_color = pixel_color
                break  # Found the first non-white color, stop scanning this row

        # Check if the found source_color is valid for replacement (not white and not gray)
        if source_color != 0 and source_color != 5:
            # If the source_color is valid, iterate through the row again
            for c in range(width):
                # Check if the pixel in the *original* input grid is gray
                if input_grid[r, c] == 5:
                    # Replace the gray pixel in the output grid with the source_color
                    output_grid[r, c] = source_color

    return output_grid