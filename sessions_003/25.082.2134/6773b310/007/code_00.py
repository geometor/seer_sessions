"""
1.  **Sectioning:**
    *   Examine the input grid for a horizontal line consisting entirely of azure (8) pixels.
    *   If found, divide the grid into three sections: `top` (rows above the azure line), `middle` (the azure line itself), and `bottom` (rows below the azure line).
    *   If no azure line is found, divide the grid into three sections based on row indices: `top` (rows 0 up to, but not including, row at index `rows // 3`), `middle` (rows from `rows // 3` up to but not including row at index `(2 * rows) // 3`), and `bottom` (the remaining rows from `(2*rows)//3` to the end).

2.  **Magenta Pixel Identification:**
    *   Iterate through all cells in the input grid.
    *   Identify and record the row and column indices of all pixels with the value 6 (magenta).

3.  **Output Grid Population:**
    *   Create a 3x3 output grid initialized with all zeros.
    *   For each magenta pixel found:
        *   Determine the output row based on the section the magenta pixel belongs to: 0 for `top`, 1 for `middle`, and 2 for `bottom`.
        *   Determine the output column based on the input grid's width:
            *   If the magenta pixel's column index is less than `input_grid_width // 3`, the output column is 0.
            *   If the magenta pixel's column index is greater or equal to than `input_grid_width // 3` and less than `(2 * input_grid_width) // 3`, the output column is 1.
            *   Otherwise, the output column is 2.
        *    Set output cell to 1 (blue).

4. Return output grid.
"""

import numpy as np

def _get_sections(grid):
    """Divides the grid into top, middle, and bottom sections."""
    rows = grid.shape[0]
    azure_line_row = -1
    for r in range(rows):
        if np.all(grid[r] == 8):
            azure_line_row = r
            break

    if azure_line_row != -1:
        top_section = (0, azure_line_row)  # Start and end row indices
        middle_section = (azure_line_row, azure_line_row + 1)
        bottom_section = (azure_line_row + 1, rows)
    else:
        top_row_end = rows // 3
        middle_row_end = (2 * rows) // 3
        top_section = (0, top_row_end)
        middle_section = (top_row_end, middle_row_end)
        bottom_section = (middle_row_end, rows)
    return top_section, middle_section, bottom_section

def _find_magenta_pixels(grid):
    """Returns a list of (row, col) tuples for magenta pixels."""
    magenta_pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 6:
                magenta_pixels.append((r, c))
    return magenta_pixels

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    input_grid = np.array(input_grid)  # Ensure numpy array

    # 1. Sectioning
    top_section, middle_section, bottom_section = _get_sections(input_grid)

    # 2. Magenta Pixel Identification
    magenta_pixels = _find_magenta_pixels(input_grid)

    # 3. Output Grid Population
    output_grid = np.zeros((3, 3), dtype=int)
    input_width = input_grid.shape[1]

    for r, c in magenta_pixels:
        # Determine output row
        if top_section[0] <= r < top_section[1]:
            output_row = 0
        elif middle_section[0] <= r < middle_section[1]:
            output_row = 1
        elif bottom_section[0] <= r < bottom_section[1]:
            output_row = 2
        else:
            output_row = -1 #should not happen

        # Determine output column
        if c < input_width // 3:
            output_col = 0
        elif c < (2 * input_width) // 3:
            output_col = 1
        else:
            output_col = 2

        # Set output cell to 1
        if output_row != -1: #should always be true
            output_grid[output_row, output_col] = 1

    return output_grid