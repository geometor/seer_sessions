"""
The input grid is transformed into an output grid by selectively filling regions with blue. Red and magenta pixels are preserved. A downward-propagating blue fill starts from the top and is blocked by certain colors. The fill is blocked *before* it reaches the blocking color.

1.  **Copy:** Create a copy of the input grid.
2.  **Preserve:** Identify all red (2) and magenta (6) pixels.  Their positions and colors are preserved in the output.
3.  **Column-wise Blue Fill:**
    *   Iterate through each column.
    *   For each column, iterate through rows from top to bottom.
    *   **Check for Blocking:** Before filling a cell, check if *any* cell *below* the current cell in the *same* column has a color other than 0, 2, or 6 (a "blocking color").
    *   **If a blocker is found below:** Do *not* fill the current cell (or any above it in this column). Move to the next column.
    *   **If no blocker is found below:**
        *   If the current cell is white (0), change to blue (1).
        *   If the current cell is red (2) or magenta (6), it is already preserved.
        *   If the current cell is any other color, it is blocking color - do nothing here.
"""

import numpy as np

def _check_for_blocker(grid, col, start_row):
    """Checks for a blocking color below a given cell in the same column."""
    rows = grid.shape[0]
    for r in range(start_row + 1, rows):  # Check rows *below* the current cell
        if grid[r, col] not in (0, 2, 6):
            return True  # Blocker found
    return False  # No blocker found

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows = output_grid.shape[0]
    cols = output_grid.shape[1]

    # Iterate through columns
    for c in range(cols):
        # Iterate through rows from top to bottom
        for r in range(rows):
            current_color = output_grid[r, c]

            # Check for blocker *before* filling
            if _check_for_blocker(output_grid, c, r):
                continue  # Skip to the next cell if a blocker is below

            # If no blocker and white, change to blue
            if current_color == 0:
                output_grid[r, c] = 1
            # Red and magenta are already preserved by the copy

    return output_grid