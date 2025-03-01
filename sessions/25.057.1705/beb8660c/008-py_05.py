"""
Transformation Rule:

1.  **Identify Colored Lines:** Find all horizontal lines consisting of one or more contiguous pixels of the same non-zero color.
2.  **Determine New Order using Original index**: Add empty rows on the top. For the colored line, put them at the index that is equal to the number of rows from that row to the bottom.
3. **Reconstruct Grid:** fill the top lines with 0. Arrange the original line based on the new order.
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