"""
1.  **Identify Vertical Lines:** Find all vertical lines composed entirely of grey (5) pixels within the input grid.
2.  **Determine Transformation Color by Position:**
    *   If it is the first grey line from left to right, change all its pixels to yellow (4).
    *   If it is the second grey line, change all its pixels to red (2).
    *   If the grey vertical line is the third or greater, change all its pixels to blue(1).
3.  **Apply Transformation:** Replace the grey (5) pixels in each identified vertical line with their assigned `transformed_color`.
4. **Other Pixels:** All pixels that aren't part of a grey vertical line remain unchanged.
"""

import numpy as np

def find_vertical_lines(grid, color=5):
    """Finds vertical lines of a specified color in the grid."""
    lines = []
    rows, cols = grid.shape
    for c in range(cols):
        start = -1
        for r in range(rows):
            if grid[r, c] == color:
                if start == -1:
                    start = r
            elif start != -1:
                lines.append((start, r - 1, c))
                start = -1
        if start != -1:
            lines.append((start, rows - 1, c))
    return lines

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    lines = find_vertical_lines(input_grid)

    # Create a dictionary to track line columns and their order
    line_cols = {}
    for start_row, end_row, col in lines:
        line_cols.setdefault(col, []).append((start_row, end_row))

    # Sort the columns to determine their left-to-right order
    sorted_cols = sorted(line_cols.keys())

    # Determine the output color for each line based on its position
    for i, col in enumerate(sorted_cols):
        lines_in_col = line_cols[col]

        if i == 0:  # First line
            output_color = 4  # Yellow
        elif i == 1:  # Second line
            output_color = 2  # Red
        else:  # Third or greater
            output_color = 1  # Blue

        for start_row, end_row in lines_in_col:
            for r in range(start_row, end_row + 1):
                output_grid[r, col] = output_color

    return output_grid