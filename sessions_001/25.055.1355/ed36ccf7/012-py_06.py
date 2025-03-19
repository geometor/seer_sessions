"""
The transformation rule can be described as follows:

1. **Identify Object:** Find the contiguous block of magenta (color 6) pixels. This constitutes the primary object (in this case, always a single pixel).
2. **Context:**  The magenta pixel exists within a 3x3 grid of white pixels.  It doesn't interact with other objects.
3. **Movement:** The magenta pixel moves one step clockwise *along the edges* of the 3x3 area. If it reaches a "corner", it continues to the next available space along the perimeter.

The previous code incorrectly implemented the rule, assuming *counter-clockwise* movement. This version corrects that. The key difference is the order of `positions`.
"""

import numpy as np

def find_magenta_pixel(grid):
    """Finds the coordinates of the magenta pixel."""
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == 6:
                return (i, j)
    return None

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the magenta pixel
    magenta_pos = find_magenta_pixel(input_grid)

    if magenta_pos is None:
        return output_grid  # No magenta pixel found, return original grid

    magenta_row, magenta_col = magenta_pos

    # Define the possible positions in *clockwise* order
    positions = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0)]

    # Find the current position index
    try:
        current_index = positions.index((magenta_row, magenta_col))
    except ValueError:
        return output_grid  # magenta is not on the perimeter

    # Calculate the next position index (clockwise)
    next_index = (current_index + 1) % len(positions)

    # Get the next position coordinates
    next_row, next_col = positions[next_index]

    # Clear the current magenta pixel and set the next position
    output_grid[magenta_row, magenta_col] = 0
    output_grid[next_row, next_col] = 6

    return output_grid