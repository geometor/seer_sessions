"""
1.  **Identify Horizontal Lines:** Scan the input grid row by row. Identify contiguous horizontal sequences of pixels with the same non-zero color. Each sequence is a "line". Record the line's original row index, color, and length.
2.  **Determine Output Grid Size:** If the expected output grid size is different, use the expected output grid size.
3.  **Create Output Grid:** Initialize an output grid of zeros with the determined size.
4.  **Reorder and Place Lines:** Iterate through the identified lines, preserving their original order (from top to bottom of the *input* grid). Place each line in the output grid, starting from the bottom row and moving upwards. The horizontal position of each line segment should align with the left edge, and its length will dictate where it extends.
5. **Fill Empty Rows:** implicitly done when creating the output grid with zeros.
"""

import numpy as np

def get_lines(grid):
    """
    Identifies horizontal lines of uniform color in a grid.
    Returns a list of tuples: (row_index, color, length)
    """
    lines = []
    for row_index, row in enumerate(grid):
        current_color = None
        current_length = 0
        for cell in row:
            if cell != 0:  # Consider 0 as background/empty
                if current_color is None:
                    current_color = cell
                    current_length = 1
                elif cell == current_color:
                    current_length += 1
                else:
                    lines.append((row_index, current_color, current_length))
                    current_color = cell
                    current_length = 1
            elif current_color is not None:
                lines.append((row_index, current_color, current_length))
                current_color = None
                current_length = 0
        if current_color is not None:
            lines.append((row_index, current_color, current_length))
    return lines

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    lines = get_lines(input_grid)
    output_grid = np.zeros_like(input_grid)
   
    # Reorder and Place Lines
    current_row = output_grid.shape[0] - 1
    lines_sorted = sorted(lines, key = lambda x:x[0], reverse=False)

    for row_index, color, length in lines_sorted:
        output_grid[current_row, :length] = color
        current_row -= 1
        if current_row < 0:
          # create a new grid that is bigger.
          new_output_grid = np.zeros((output_grid.shape[0] + 1, output_grid.shape[1]), dtype=int)

          # copy over existing
          new_output_grid[1:, :] = output_grid
          output_grid = new_output_grid
          current_row = 0

    return output_grid.tolist()