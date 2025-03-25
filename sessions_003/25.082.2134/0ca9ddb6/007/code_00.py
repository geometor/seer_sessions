"""
1.  **Preservation:** The original blue (1), red (2), magenta (6), and azure (8) pixels in the input grid remain in their original positions in the output grid.

2.  **Yellow Pixel Placement (Conditional on Red):** For each red (2) pixel in the input grid:
    *   Place a yellow (4) pixel one row *below* the red pixel.
    *   Place a yellow (4) pixel two rows *below* and one columns *to the left* of the red pixel.
    *   Place a yellow (4) pixel two rows *below* and one columns *to the right* of the red pixel.

3.  **Orange Pixel Placement (Conditional on Blue):** For each blue (1) pixel in the input grid:
    *   Place an orange (7) pixel one row *below* the blue pixel.
    *   Place an orange (7) pixel in the same row, one column *to the left* of the blue pixel.
    *   Place an orange (7) pixel in the same row, one column *to the right* of the blue pixel.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the grid to find red and blue pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 2:  # Red pixel
                # Add yellow pixels below, and two below and one to the left/right RELATIVE to the red pixel
                if r + 1 < rows:
                    output_grid[r + 1, c] = 4  # One row below
                if r + 2 < rows:
                    if c - 1 >= 0:
                        output_grid[r + 2, c - 1] = 4  # Two rows below, one column left
                    if c + 1 < cols:
                        output_grid[r + 2, c + 1] = 4  # Two rows below, one column right
            elif input_grid[r, c] == 1:  # Blue pixel
                # Add orange pixels below, left, and right RELATIVE to the blue pixel
                if r + 1 < rows:
                    output_grid[r + 1, c] = 7  # One row below
                if c - 1 >= 0:
                    output_grid[r, c - 1] = 7  # Same row, one column left
                if c + 1 < cols:
                    output_grid[r, c + 1] = 7  # Same row, one column right

    return output_grid