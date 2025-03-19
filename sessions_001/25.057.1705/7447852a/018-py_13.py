"""
Transforms an input grid by replacing white pixels (0) with yellow pixels (4) based on their proximity to red pixels (2). A white pixel becomes yellow only if it is directly adjacent (horizontally, vertically, or diagonally) to a red pixel in the *original* input grid.
"""

import numpy as np

def _is_adjacent_to_red(grid, r, c):
    """Checks if a cell at (r, c) is adjacent to a red pixel in the given grid."""
    rows, cols = grid.shape
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the cell itself
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 2:
                return True
    return False

def transform(input_grid):
    """
    Transforms the input grid according to the observed rules.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Create a list to store the coordinates of white pixels that should be changed to yellow.
    white_pixels_to_change = []

    # Iterate through each pixel in the original input grid.
    for r in range(rows):
        for c in range(cols):
            # Check if the current pixel is white (0).
            if input_grid[r, c] == 0:
                # Check for adjacent red pixels in all 8 directions in the original grid.
                if _is_adjacent_to_red(input_grid, r, c):
                    white_pixels_to_change.append((r, c))

    # Change the color of the identified white pixels to yellow.
    for r, c in white_pixels_to_change:
        output_grid[r, c] = 4

    return output_grid