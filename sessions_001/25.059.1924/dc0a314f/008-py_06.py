"""
Extracts a horizontal line of 3 pixels representing the object in the input grid.
"""

import numpy as np

def find_contiguous_object(input_grid):
    """
    Finds a contiguous object (horizontal or vertical line) in the input grid.
    Returns the color and a list of coordinates of the object's pixels.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    object_pixels = []
    target_color = None

    for r in range(rows):
        for c in range(cols):
            color = input_grid[r, c]
            if color == 0:  # Skip background
                continue

            # Check for contiguity (horizontal or vertical)
            if (r > 0 and input_grid[r-1, c] == color) or \
               (c > 0 and input_grid[r, c-1] == color):
                if target_color is None:
                    target_color = color
                if target_color == color: # add pixels if it belongs to the same object.
                    object_pixels.append((r, c))

    return target_color, object_pixels

def transform(input_grid):
    # Find the contiguous object
    target_color, object_pixels = find_contiguous_object(input_grid)

    # Initialize output grid
    output_grid = []

    # If no object is found, return None
    if target_color is None:
        return None

    # Create the output grid (1x3) and fill with the object's color
    output_grid = [[target_color] * 3]

    return output_grid