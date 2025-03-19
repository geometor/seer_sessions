"""
1.  **Row Classification:** Examine each row of the input grid.
    *   A row is "magenta" if all pixels are magenta (6).
    *   A row is "green" if all pixels are green (3).
    *   Otherwise, the row is classified as white.

2.  **Output Grid Construction (3x3):** Create a 3x3 output grid, initially filled with white.

3.  **Conditional Logic:**
      *   If *any* green rows exist, the *first* row of the output is all green (3).
      *   If at least one green row AND at least one magenta row exist, the *second* row of the output grid is all magenta (6).
      *  If green *and* magenta rows exist, *and* if there are any green rows *after* the *last* appearance of a magenta row, the *third* row of output is all green (3).
      *   If *no* green rows exist, but at least one magenta row exists, the *first* row of the output is all magenta (6).
      * All other rows of the output grid are filled with white.
"""

import numpy as np

def classify_row(row):
    # Classify a row as magenta (6), green (3), or white (0)
    if all(pixel == 6 for pixel in row):
        return 6  # Magenta
    elif all(pixel == 3 for pixel in row):
        return 3  # Green
    else:
        return 0  # White

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)
    rows, _ = input_grid.shape

    # Classify all rows
    row_classifications = [classify_row(input_grid[r]) for r in range(rows)]

    # Check for existence of green and magenta rows
    has_green = 3 in row_classifications
    has_magenta = 6 in row_classifications
    
    # find positions
    magenta_positions = [i for i, x in enumerate(row_classifications) if x == 6]
    green_positions = [i for i, x in enumerate(row_classifications) if x == 3]

    # Construct output grid based on rules
    if has_green:
        output_grid[0, :] = 3  # First row is green
        if has_magenta:
            output_grid[1, :] = 6  # Second row is magenta
            if len(magenta_positions) > 0:
                last_magenta_position = magenta_positions[-1]
                if any(pos > last_magenta_position for pos in green_positions):
                    output_grid[2, :] = 3 # Third row is green
    elif has_magenta:
        output_grid[0, :] = 6  # First row is magenta

    return output_grid