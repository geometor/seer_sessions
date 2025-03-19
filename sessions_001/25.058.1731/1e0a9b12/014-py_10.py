"""
The transformation rule is as follows:

1.  **Identify Objects:** Locate all single-pixel, non-zero colored objects within the input grid.
2.  **Find Maroon (9):** Specifically identify the coordinates of the maroon (9) object.
3. **Move the Maroon Object:** The maroon (9) pixel moves *down one row*, but does not change column.
4.  **Preserve Other Objects:** All other colored objects (single pixels) remain in their exact original positions.
5.  **Output Grid:** Create an output grid of the same dimensions as the input, where all the other cells are '0' (white).
"""

import numpy as np

def find_object(grid, color):
    """Finds the coordinates of a single-cell object with the given color."""
    coords = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color:
                coords.append((r,c))
    return coords

def transform(input_grid):
    """Transforms the input grid according to the rule."""

    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the position of 9 (maroon).
    pos_9 = find_object(input_grid, 9)
    
    if pos_9: # only proceed if 9 exists
        pos_9 = pos_9[0] # get the single coordinate

        # Calculate the new position of 9 (one row down).
        new_pos_9 = (pos_9[0] + 1, pos_9[1])

        # Clear the old position of 9 and set the new position.
        output_grid[pos_9[0], pos_9[1]] = 0
        if new_pos_9[0] < output_grid.shape[0]:
            output_grid[new_pos_9[0], new_pos_9[1]] = 9

    return output_grid