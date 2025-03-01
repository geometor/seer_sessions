"""
This program transforms an input grid by identifying azure lines and filling the spaces between them with specific colors.
The azure lines are preserved, and the spaces are filled according to these rules:
    - Above the first horizontal line:
        - Left of the vertical line: red (2)
        - Right of the vertical line: magenta (6)
    - Between the horizontal lines:
        - Left of the vertical line: blue (1)
        - Right of the vertical line: green (3)
       - If no vertical line, fill with blue (1)
    - Below the last horizontal line: blue (1)
"""

import numpy as np

def find_azure_lines(grid):
    # Find the vertical and horizontal azure lines.
    azure_indices = np.where(grid == 8)
    rows = np.unique(azure_indices[0])
    cols = np.unique(azure_indices[1])
    
    vertical_line_col = None
    horizontal_lines_row = []

    for col in cols:
        if np.sum(grid[:, col] == 8) > 2:  # Assuming a vertical line has more than two azure pixels
            vertical_line_col = col
            break

    for row in rows:
        if np.sum(grid[row, :] == 8) > 2 :
            horizontal_lines_row.append(row)
    
    return vertical_line_col, horizontal_lines_row

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the azure lines
    vertical_line_col, horizontal_lines_row = find_azure_lines(input_grid)

    # Fill the spaces between the lines
    for r in range(rows):
        for c in range(cols):
            # Preserve azure pixels
            if input_grid[r, c] == 8:
                continue

            # Above the first horizontal line
            if horizontal_lines_row and r < horizontal_lines_row[0]:
                if vertical_line_col is not None:
                    if c < vertical_line_col:
                        output_grid[r, c] = 2  # Red
                    else:
                        output_grid[r, c] = 6  # Magenta

            # Between the horizontal lines
            elif horizontal_lines_row and len(horizontal_lines_row) > 1 :
                if horizontal_lines_row[0] <= r < horizontal_lines_row[-1]:
                    if vertical_line_col is not None:
                        if c < vertical_line_col:
                            output_grid[r, c] = 1  # Blue
                        else:
                            output_grid[r, c] = 3  # Green
                    else:
                        output_grid[r,c] = 1
            # Below last horizontal
            elif horizontal_lines_row and  r >= horizontal_lines_row[-1]:
                output_grid[r,c] = 1


    return output_grid