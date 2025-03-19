"""
1. Identify the largest black rectangle in the input grid.
2. Determine the bounding box of the largest black rectangle.
3. Reflect the content within the bounding box horizontally across its vertical midpoint.
4. Set all pixels outside the bounding box to black (0).  The output grid's dimensions are cropped to match the bounding box.
"""

import numpy as np

def get_largest_black_rectangle(grid):
    """Finds the largest black rectangle in a grid."""
    black_pixels = np.argwhere(grid == 0)
    if len(black_pixels) == 0:
        return None  # No black pixels

    min_row, min_col = black_pixels.min(axis=0)
    max_row, max_col = black_pixels.max(axis=0)

    # Check if it forms a rectangle
    expected_size = (max_row - min_row + 1) * (max_col - min_col + 1)
    actual_size = np.sum(grid[min_row:max_row+1, min_col:max_col+1] == 0)

    if expected_size == actual_size:
        return (min_row, min_col, max_row, max_col)
    else:
        return None

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    # Find the largest black rectangle
    black_rect = get_largest_black_rectangle(input_grid)

    if black_rect is None:
        return np.zeros((0, 0), dtype=int) # Return empty array if no black rectangle

    min_row, min_col, max_row, max_col = black_rect

    # Create a cropped input grid representing the bounding box
    cropped_input = input_grid[min_row:max_row+1, min_col:max_col+1]

    # Reflect the cropped input horizontally
    reflected_cropped_input = np.flipud(cropped_input)

    # The output grid is the reflected cropped input
    output_grid = reflected_cropped_input

    return output_grid