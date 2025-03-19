"""
Transforms the input grid by rearranging horizontal bars of colors. The bars are sorted by their original row position and then placed in the output grid, right-aligned.
"""

import numpy as np

def find_bars(grid):
    """Finds all horizontal bars in the grid."""
    bars = []
    for row_index, row in enumerate(grid):
        col_index = 0
        while col_index < len(row):
            if row[col_index] != 0:
                color = row[col_index]
                start_col = col_index
                length = 0
                while col_index < len(row) and row[col_index] == color:
                    length += 1
                    col_index += 1
                bars.append({'color': color, 'length': length, 'row': row_index, 'start_col': start_col})
            else:
                col_index += 1
    return bars

def transform(input_grid):
    # Initialize output grid
    output_grid = np.zeros_like(input_grid)
    grid_height, grid_width = input_grid.shape

    # Find all horizontal bars
    bars = find_bars(input_grid)

    # Sort bars by row index
    bars.sort(key=lambda bar: bar['row'])

    # Place bars in the output grid
    output_row = grid_height - len(bars)

    for bar in bars:
        start_col = grid_width - bar['length']
        output_grid[output_row, start_col:start_col + bar['length']] = bar['color']
        output_row += 1


    return output_grid