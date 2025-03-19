"""
The transformation rearranges horizontal bars of colored pixels. It identifies these bars in the input grid,
records their properties (color, length, row position), and then re-positions them at the bottom of the output grid.
The bars are stacked at the bottom in the same vertical order they appeared in the input.
"""

import numpy as np

def find_horizontal_bars(grid):
    """
    Finds all horizontal bars in the grid.
    Returns a list of dictionaries, each representing a bar.
    """
    bars = []
    rows, cols = grid.shape
    for r in range(rows):
        c = 0
        while c < cols:
            if grid[r, c] != 0:  # Not background
                color = grid[r, c]
                start_col = c
                while c < cols and grid[r, c] == color:
                    c += 1
                end_col = c - 1
                length = end_col - start_col + 1
                bars.append({
                    'color': color,
                    'length': length,
                    'row': r,
                    'start_col': start_col,
                    'end_col': end_col
                })
            else:
                c += 1
    return bars

def transform(input_grid):
    """
    Transforms the input grid by rearranging horizontal bars to the bottom.
    """
    # initialize output_grid
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Find horizontal bars
    bars = find_horizontal_bars(input_grid)

    # Sort bars by their original row (top-to-bottom order)
    bars.sort(key=lambda bar: bar['row'])

    # Determine new row positions, starting from the bottom
    current_row = rows - 1
    for bar in bars:
        # Place the bar on the output grid
        output_grid[current_row, bar['start_col']:bar['end_col'] + 1] = bar['color']
        current_row -= 1 # Move up one row for the next bar

    return output_grid