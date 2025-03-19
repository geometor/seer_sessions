"""
1.  **Identify Rows:** Examine each row of the input grid.
2.  **Classify Rows:**
    *   A row is classified as a "magenta row" if all its pixels are magenta (6).
    *   A row is classified as a "green row" if all its pixels are green (3).
    *  Otherwise the row is white
3.  **Construct Output Grid (3x3):**
    *   If any green rows exist:
        * The first row of the output grid is all green (3).
        * If a magenta row exists *anywhere* in input, the *second* output row is all magenta (6).
        * If one or more green rows exist *after* any magenta row, the *third* output row is all green (3).
    *   If NO green rows exist, but one or more magenta row exists:
        *   The first row of the output is all magenta (6).
    * All other rows of output grid are white.
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
                last_mag_pos = magenta_positions[-1]
                if any(pos > last_mag_pos for pos in green_positions):                   
                   output_grid[2, :] = 3
    elif has_magenta:
        output_grid[0, :] = 6  # First row is magenta

    return output_grid