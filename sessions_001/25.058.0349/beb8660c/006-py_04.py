"""
Transforms the input grid by identifying horizontal bars of pixels and repositioning them to the right edge of the output grid, while maintaining their original vertical order.
"""

import numpy as np

def find_horizontal_bars(grid):
    """
    Identifies horizontal bars in the grid.
    Returns a list of dictionaries, each representing a bar.
    """
    bars = []
    for row_index, row in enumerate(grid):
        start_col = -1
        current_color = -1
        for col_index, pixel in enumerate(row):
            if pixel != 0:  # Non-background pixel
                if start_col == -1:
                    start_col = col_index
                    current_color = pixel
                elif pixel != current_color:
                    bars.append({
                        "color": current_color,
                        "length": col_index - start_col,
                        "row": row_index,
                        "start_col": start_col
                    })
                    start_col = col_index
                    current_color = pixel
            elif start_col != -1:
                bars.append({
                    "color": current_color,
                    "length": col_index - start_col,
                    "row": row_index,
                    "start_col": start_col
                })
                start_col = -1
                current_color = -1
        if start_col != -1:  # Handle bars ending at the last column
             bars.append({
                "color": current_color,
                "length": len(row) - start_col,
                "row": row_index,
                 "start_col" : start_col
            })
    return bars

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Find horizontal bars
    bars = find_horizontal_bars(input_grid)

    # Sort bars by their row index (top to bottom)
    sorted_bars = sorted(bars, key=lambda x: x['row'])

    # Reposition bars in the output grid, right-aligned
    for bar in sorted_bars:
        row = bar['row']
        for i in range(bar['length']):
            output_grid[row, cols - bar['length'] + i] = bar['color']

    return output_grid