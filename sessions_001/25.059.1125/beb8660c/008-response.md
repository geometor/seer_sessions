# beb8660c • 008 • refine_coder

---
```python
"""
1.  **Identify Horizontal Bars:** Find all horizontal bars in the input grid. A horizontal bar is defined as a contiguous sequence of pixels of the same color within a single row. Record the color, length, starting row index, start column, and end column of each bar.
2.  **Sort Bars:** Sort the identified bars by their original row index, preserving their top-to-bottom order from the input.
3.  **Reposition Bars:** Create an output grid filled with the background color (0). Starting from the *bottom* row of the output grid, place the sorted bars one by one. Each bar's pixels should be placed in their original horizontal positions (using the bar length and starting column) and original color. Successive bars are placed in rows above the previous, thus building the final output grid from the bottom upward, preserving relative vertical position from the input.
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
```
