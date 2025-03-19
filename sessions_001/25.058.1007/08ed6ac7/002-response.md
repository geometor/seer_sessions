# 08ed6ac7 • 002 • example_2 • investigate_coder

---
```python
"""
1.  **Identify Vertical Bars:** Locate all vertical bars within the input grid. A vertical bar is defined as a contiguous sequence of grey (5) pixels extending downwards in a single column.
2. **Background to White:** All pixels that have value 0 or that are grey pixels (value 5) that are not part of any identified vertical bars are turned to white (0).
3.  **Recolor Vertical Bars:** Each vertical bar is assigned a new color. Iterate through the columns from left to right, start with the first one blue (1), the second to be red (2), the third is green (3) and the fouth is yellow (4). If there are more vertical bars after that, repeat this color assignment rule (start from blue (1))
4.  **Output:** Generate the output grid with the recolored vertical bars and the white background.
"""

import numpy as np

def find_vertical_bars(grid):
    """Finds contiguous vertical bars of grey pixels (value 5)."""
    bars = []
    num_cols = grid.shape[1]
    for col in range(num_cols):
        start_row = -1
        for row in range(grid.shape[0]):
            if grid[row, col] == 5:
                if start_row == -1:
                    start_row = row
            elif start_row != -1:
                bars.append((col, start_row, row - 1))  # (column, start_row, end_row)
                start_row = -1
        if start_row != -1:  # Handle bar extending to the bottom edge
            bars.append((col, start_row, grid.shape[0] - 1))
    return bars

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    output_grid = np.zeros_like(input_grid)  # Initialize with white (0)

    # Find vertical bars
    vertical_bars = find_vertical_bars(input_grid)

    # Create a mask for bar pixels
    bar_mask = np.zeros_like(input_grid, dtype=bool)
    for col, start_row, end_row in vertical_bars:
        bar_mask[start_row:end_row+1, col] = True

    # set background
    output_grid[(input_grid == 0) | ((input_grid == 5) & ~bar_mask)] = 0

    # Recolor vertical bars
    color_sequence = [1, 2, 3, 4]  # Blue, Red, Green, Yellow
    color_index = 0
    for col, start_row, end_row in vertical_bars:
        output_grid[start_row:end_row+1, col] = color_sequence[color_index % len(color_sequence)]
        color_index += 1

    return output_grid
```
