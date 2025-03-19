"""
1.  **Identify Objects:** Locate all single-pixel objects within the input grid.
2.  **Find Maroon (9):** Specifically identify the coordinates of the maroon (9) pixel.
3.  **Conditional Maroon Movement:**
    *   If the maroon (9) pixel is *not* in the last row of the grid, move it down one row, keeping its column the same.
    *   If the maroon (9) pixel *is* in the last row, it remains in its original position.
4.  **Preserve Other Objects:** All other colored objects (single pixels) remain in their exact original positions.
5.  **Output Grid:** Create an output grid of the same dimensions as the input, reflecting the changes (or lack thereof) to the maroon pixel and the preservation of other objects. The background is implicitly 0 (white).
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

        # Clear the old position of 9 and set the new position if not at the bottom.
        output_grid[pos_9[0], pos_9[1]] = 0
        if new_pos_9[0] < output_grid.shape[0]:
            output_grid[new_pos_9[0], new_pos_9[1]] = 9

    return output_grid