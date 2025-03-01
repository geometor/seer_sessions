"""
The transformation rule is to duplicate a horizontal line of colored pixels (red and green) horizontally. The line's color pattern is repeated once to the right, effectively doubling its length. The rest of the grid, which consists of white pixels, remains unchanged in its dimensions.
"""

import numpy as np

def find_colored_line(grid):
    """Finds the single horizontal line of non-white pixels."""
    rows, cols = grid.shape
    for r in range(rows):
        line_start = -1
        line_end = -1
        color_sequence = []

        for c in range(cols):
            if grid[r, c] != 0:
                if line_start == -1:
                    line_start = c
                line_end = c
                color_sequence.append(grid[r, c])
            elif line_start != -1:
                break  # End of the continuous line

        if line_start != -1:
           return r, line_start, line_end + 1, color_sequence # exclusive end

    return None, None, None, None

def transform(input_grid):
    """Transforms the input grid by expanding the colored line horizontally."""
    # Find the colored line
    row_index, start_col, end_col, color_sequence = find_colored_line(input_grid)
    
    # Initialize the output grid: same height and white padding around
    output_grid = np.zeros((input_grid.shape[0], input_grid.shape[1] + len(color_sequence)), dtype=int)

    # Expand the line: construct expanded sequence
    expanded_sequence = color_sequence + color_sequence
    
    # Place expanded sequence into output
    if row_index is not None:
      output_grid[row_index, start_col:start_col + len(expanded_sequence)] = expanded_sequence

    return output_grid