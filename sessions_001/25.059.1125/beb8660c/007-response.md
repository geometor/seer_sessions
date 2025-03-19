# beb8660c • 007 • refine_coder

---
```python
"""
1.  **Identify Horizontal Bars:** Scan the input grid row by row. Identify contiguous horizontal sequences of pixels with the same color. Each such sequence is a "bar." Record the bar's color, length, starting/ending column, and original row.
2.  **Sort Bars:** Sort the identified bars in ascending order based on their original row index. This ensures that bars originally higher up in the grid are processed before those lower down.
3.  **Reposition Bars:** Create an empty output grid of the same dimensions as the input. Starting from the *bottom* row of the output grid, and working upwards, place each bar on the output grid.
4. **Preserve Order** Preserve the horizontal position of each bar, as indicated in the original input.
5.  **Empty Cells:** Any cells in the output grid not filled by a bar should be set to color 0 (background - white).
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
