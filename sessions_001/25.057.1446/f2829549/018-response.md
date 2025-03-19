# f2829549 • 018 • refine_coder

---
```python
"""
1.  **Identify Blue Lines:** Find all vertical lines composed entirely of blue (1) pixels in the input grid. A vertical line is defined as a contiguous sequence of pixels of the same color extending downwards from a starting point to the bottom of the grid or until a different color is encountered.
2.  **Create Output Grid:** Initialize an output grid with the same dimensions as the input grid, filled with black (0) pixels.
3.  **Replace with Green Lines:** For each blue vertical line identified in the input, create a corresponding green (3) vertical line in the output grid. The green line should occupy the *same column* as the blue line and have the *same length and starting row*.
"""

import numpy as np

def find_vertical_lines(grid, color):
    """
    Finds the starting positions and lengths of vertical lines of a specified color.
    Returns a list of (row, col, length) tuples.
    """
    lines = []
    rows, cols = grid.shape
    for j in range(cols):
        for i in range(rows):
            if grid[i, j] == color:
                # Check if it's a vertical line (all same color)
                length = 0
                for k in range(i, rows):
                    if grid[k, j] == color:
                        length += 1
                    else:
                        break
                if length > 0:
                  lines.append((i, j, length))
                  break # only want the start
    return lines

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    # 2. Create Output Grid
    output_grid = np.zeros_like(input_grid)

    # 1. Identify Blue Lines
    blue_lines = find_vertical_lines(input_grid, 1)  # Blue

    # 3. Replace with Green Lines
    for row, col, length in blue_lines:
        for i in range(length):
            output_grid[row + i, col] = 3  # Green

    return output_grid
```

