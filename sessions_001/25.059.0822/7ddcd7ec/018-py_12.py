"""
1.  **Identify the 2x2 Orange Square:** Find the contiguous 2x2 square of orange (color 7) pixels within the input grid. This square serves as an anchor point. The position is recorded as the top-left pixel of the square.

2.  **Create Pixels/Columns Relative to Corners:**
    *   **Top-Left Corner:** Create a single orange pixel directly above and to the left of the top-left corner of the 2x2 square.
    *   **Bottom-Left Corner:** Create a single orange pixel directly below and to the left of the *bottom*-left corner of the 2x2 square.
    *   **Top-Right Corner:** Create a 2x1 orange *column* of pixels directly above and to the right of the *top*-right corner of the 2x2 square.

3. **No changes to original 2x2 square** The 2x2 block remains in place.
"""

import numpy as np

def find_2x2_square(grid, color):
    """Finds the top-left corner of a 2x2 square of the given color."""
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if (grid[r, c] == color and
                grid[r + 1, c] == color and
                grid[r, c + 1] == color and
                grid[r + 1, c + 1] == color):
                return (r, c)
    return None

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the 2x2 orange square
    square_coords = find_2x2_square(input_grid, 7)

    if square_coords:
        r, c = square_coords

        # Top-Left Corner: Create a single orange pixel
        if r > 0 and c > 0:
            output_grid[r - 1, c - 1] = 7

        # Bottom-Left Corner: Create a single orange pixel
        if r + 2 < rows and c > 0:
          output_grid[r + 2, c - 1] = 7
        # Top-Right Corner: Create a 2x1 orange column
        if r > 1 and c + 2 < cols:
            output_grid[r - 1, c + 2] = 7
            output_grid[r - 2, c + 2] = 7

    return output_grid