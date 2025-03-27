```python
"""
1.  **Identify Horizontal Lines:** Scan the input grid row by row. Identify contiguous horizontal sequences of pixels with the same non-zero color. Each sequence is a "line segment." Record the row index, color, length, and starting column (x-offset) of each segment.
2.  **Determine initial output grid:** Initialize an output grid filled with zeros that is the same shape as the input grid.
3.  **Reorder and Place:** Iterate through the identified line segments from top to bottom, based on their original row index in the input grid.
4.  **Stacking:** Place each segment in the output grid, starting from the *bottom* row and moving upwards. Preserve the original x-offset of the segment when placing it.
5.  **Vertical Resizing:** If, during placement, the current row index becomes negative (meaning we've run out of rows at the top), increase the height of the output grid by one row *at the top*. When inserting rows, shift existing content in the grid down by one before placing. Repeat until the line segment is placed.
"""

import numpy as np

def get_lines(grid):
    """
    Identifies horizontal lines of uniform color in a grid.
    Returns a list of tuples: (row_index, color, length, x_offset)
    """
    lines = []
    for row_index, row in enumerate(grid):
        current_color = None
        current_length = 0
        x_offset = 0
        for x, cell in enumerate(row):
            if cell != 0:  # Consider 0 as background/empty
                if current_color is None:
                    current_color = cell
                    current_length = 1
                    x_offset = x
                elif cell == current_color:
                    current_length += 1
                else:
                    lines.append((row_index, current_color, current_length, x_offset))
                    current_color = cell
                    current_length = 1
                    x_offset = x
            elif current_color is not None:
                lines.append((row_index, current_color, current_length, x_offset))
                current_color = None
                current_length = 0
        if current_color is not None:
            lines.append((row_index, current_color, current_length, x_offset))
    return lines

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    lines = get_lines(input_grid)
    output_grid = np.zeros_like(input_grid)

    # Reorder and Place Lines
    current_row = output_grid.shape[0] - 1
    lines_sorted = sorted(lines, key = lambda x:x[0], reverse=False)

    for row_index, color, length, x_offset in lines_sorted:
        # Vertical Resizing (add rows to top as needed)
        while current_row < 0:
            new_row = np.zeros((1, output_grid.shape[1]), dtype=int)
            output_grid = np.vstack((new_row, output_grid))
            current_row += 1

        # Place segment with correct offset
        output_grid[current_row, x_offset : x_offset + length] = color
        current_row -= 1


    return output_grid.tolist()
```