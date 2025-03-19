"""
The transformation takes the horizontal colored lines from the input, reverses their order of appearance from top-left to bottom-right, and stacks them at the bottom of the output grid. The remaining space at the top is filled with 0.
"""

import numpy as np

def find_lines(grid):
    # Find all horizontal lines of contiguous pixels with the same color.
    lines = []
    rows, cols = grid.shape
    for r in range(rows):
        c = 0
        while c < cols:
            if grid[r, c] != 0:
                color = grid[r, c]
                start_c = c
                while c < cols and grid[r, c] == color:
                    c += 1
                lines.append(((r, start_c), color, c - start_c))  # ((row, col), color, length)
            else:
                c += 1
    return lines

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Find lines in input grid
    lines = find_lines(input_grid)

    # Reverse the order of lines
    lines.reverse()

    # Stack lines at the bottom of output_grid
    current_row = rows - 1
    for (start_r, start_c), color, length in lines:
        output_grid[current_row, 0:length] = color
        current_row -= 1

    return output_grid.tolist()