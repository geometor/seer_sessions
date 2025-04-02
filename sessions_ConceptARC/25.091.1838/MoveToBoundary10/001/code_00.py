"""
Transforms the input grid by horizontally shifting colored objects.
Objects contributing to the overall minimum column index are shifted left
so their leftmost edge aligns with column 0. Objects contributing to the
overall maximum column index are shifted right so their rightmost edge aligns
with the last column of the grid. Object shapes, colors, and vertical
positions are preserved.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the horizontal alignment transformation to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_grid = np.zeros_like(input_grid) # Initialize with background color 0

    # Find coordinates and colors of all non-background pixels
    non_background_pixels = np.argwhere(input_grid != 0)

    # If there are no non-background pixels, return the initial grid
    if non_background_pixels.size == 0:
        return output_grid # which is currently a copy of the input if it was all 0s, or just all 0s

    # Find the minimum and maximum column indices occupied by non-background pixels
    min_col = non_background_pixels[:, 1].min()
    max_col = non_background_pixels[:, 1].max()

    # Identify the colors present at the minimum column
    left_moving_colors = set(input_grid[r, c] for r, c in non_background_pixels if c == min_col)

    # Identify the colors present at the maximum column
    right_moving_colors = set(input_grid[r, c] for r, c in non_background_pixels if c == max_col)

    # Calculate the required shifts
    left_shift = 0 - min_col
    right_shift = (width - 1) - max_col

    # Iterate through all pixels in the input grid
    for r in range(height):
        for c in range(width):
            color = input_grid[r, c]
            # Skip background pixels
            if color == 0:
                continue

            new_c = -1 # Initialize new column index

            # Determine if the color should move left
            if color in left_moving_colors:
                new_c = c + left_shift
            # Determine if the color should move right (only if not already moving left)
            elif color in right_moving_colors:
                new_c = c + right_shift

            # Place the pixel in the output grid if it was moved
            if new_c != -1:
                 # Ensure the new column is within grid bounds (should always be true with correct logic)
                 if 0 <= new_c < width:
                     output_grid[r, new_c] = color
                 else:
                     # This case should ideally not happen if logic is sound
                     print(f"Warning: Pixel at ({r},{c}) with color {color} shifted out of bounds to column {new_c}")


    return output_grid.tolist() # Convert back to list of lists if necessary for the environment