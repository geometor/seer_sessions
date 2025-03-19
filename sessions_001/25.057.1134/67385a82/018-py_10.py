"""
The transformation rule can be described as follows:

1.  **White (0) pixels remain unchanged.**
2.  **Green (3) pixels change to azure (8) if they are part of a contiguous line (horizontal or vertical) of green pixels and are *not* the last pixel in that line.** A line is defined as a sequence of adjacent pixels of the same color, either horizontally or vertically.
3. **The last green pixel in a contiguous horizontal or vertical line of green pixels remains green.** "Last" is determined by reading direction (left-to-right for horizontal lines, top-to-bottom for vertical lines).
4. If a Green pixel has both a horizontal and vertical neighbor, it is
   transformed independently - in the context of horizontal and vertical
   sequences separately.

"""

import numpy as np

def transform(input_grid):
    """Transforms an input grid according to the specified rules."""

    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Horizontal pass
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 3:
                if c + 1 < cols and output_grid[r, c + 1] == 3:
                    output_grid[r, c] = 8
                

    # Vertical pass (separate to handle intersections correctly)
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 3:  # Use input_grid to check original color
                if r + 1 < rows and output_grid[r + 1, c] == 3:
                    if input_grid[r+1,c] == 3:
                        output_grid[r, c] = 8

    return output_grid