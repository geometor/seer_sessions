"""
Identify all vertical lines composed of blue (1) pixels in the input grid.
For each identified blue vertical line, change the color of all pixels in that line to green (3).
The output grid is the same as the input grid, except that all blue vertical lines are now green vertical lines.
"""

import numpy as np

def find_vertical_lines(grid, color):
    """Finds vertical lines of a specified color in a grid."""
    lines = []
    rows, cols = grid.shape
    for j in range(cols):
        start = -1
        for i in range(rows):
            if grid[i, j] == color:
                if start == -1:
                    start = i
            elif start != -1:
                lines.append((start, i - 1, j))
                start = -1
        if start != -1:
            lines.append((start, rows - 1, j))
    return lines

def transform(input_grid):
    """Transforms the input grid by replacing blue lines with green lines."""
    output_grid = input_grid.copy()
    # Find blue lines
    blue_lines = find_vertical_lines(input_grid, 1)
    # Replace with green
    for start_row, end_row, col in blue_lines:
        output_grid[start_row:end_row+1, col] = 3
    return output_grid