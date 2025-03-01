"""
Transformation Rule:

1.  **Identify Horizontal Lines:** Scan the input grid row by row. Identify all horizontal lines, defined as contiguous sequences of one or more pixels of the same non-zero color. Record the row index, starting column, ending column, and color of each line.
2.  **Calculate New Row Index:** For each horizontal line, calculate its new row index in the output grid. The new row index is equal to the original distance from the bottom of the input grid (calculated as `total_rows - 1 - original_row_index`).
3.  **Construct Output Grid:** Create a new grid filled with zeros (color 0), having the same dimensions as the input grid.
4.  **Place Lines in Output:** For each identified horizontal line, place it in the output grid at its calculated `new_row_index`, maintaining its original length and color.
5. If the new index is less that the total number of rows - 1, insert blank rows on top.
"""

import numpy as np

def get_horizontal_lines(grid):
    """
    Identifies horizontal lines of non-zero, same-colored pixels.
    Returns a list of tuples: (row_index, start_col, end_col, color).
    """
    lines = []
    rows, cols = grid.shape
    for r in range(rows):
        start_col = -1
        current_color = 0
        for c in range(cols):
            if grid[r, c] != 0:
                if start_col == -1:
                    start_col = c
                    current_color = grid[r, c]
                elif grid[r, c] != current_color:
                    lines.append((r, start_col, c - 1, current_color))
                    start_col = c
                    current_color = grid[r, c]
            elif start_col != -1:
                lines.append((r, start_col, c - 1, current_color))
                start_col = -1
                current_color = 0
        if start_col != -1:
             lines.append((r, start_col, cols-1, current_color))
    return lines

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    input_grid_np = np.array(input_grid)
    rows, cols = input_grid_np.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Get horizontal lines
    lines = get_horizontal_lines(input_grid_np)

    # Determine new row index based on original row's distance to bottom
    for line in lines:
        row_index, start_col, end_col, color = line
        new_row_index = rows - 1 - row_index
        output_grid[new_row_index, start_col:end_col+1] = color

    return output_grid.tolist()