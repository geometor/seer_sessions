"""
The transformation rule is:

1. **Identify Target Line:** Locate the vertical column in the input grid consisting of the color blue (1).
2. **Create Output Grid:** Initialize a new grid with the same number of rows as the input grid, with a column for each column located and set all values to white (0).
3.  **Translate Column:** For each target, add a new column to the output at a row index +1 from the input.
4.  **Recolor Pixels:** Replace each pixel in the output that came from the target to green (3).
"""

import numpy as np

def find_vertical_lines(grid, color):
    """
    Finds the starting positions of vertical lines of a specified color.
    Returns a list of (row, col) tuples.
    """
    lines = []
    rows, cols = grid.shape
    for j in range(cols):
        for i in range(rows):
            if grid[i, j] == color:
                # Check if it's a vertical line (all same color)
                is_vertical_line = True
                for k in range(i + 1, rows):
                    if grid[k, j] != color:
                        is_vertical_line = False
                        break
                if is_vertical_line:
                    lines.append((i,j))
                    break  # Only find the start of the line
    return lines

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    # 1. Identify Target Line(s)
    target_color = 1  # Blue
    target_lines = find_vertical_lines(input_grid, target_color)

    # 2. Create Output Grid
    output_grid = np.zeros((input_grid.shape[0], len(target_lines) * 1), dtype=int)

    # 3. & 4. Translate and Recolor
    new_col_index = 0
    for start_row, start_col in target_lines:

        for i in range(input_grid.shape[0]):
          row_index = i + 1
          if row_index < output_grid.shape[0]:
            output_grid[row_index, new_col_index] = 3
          else:
             output_grid[0, new_col_index] = 3

        new_col_index += 1


    return output_grid