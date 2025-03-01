# ce9e57f2 • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Vertical Red Lines:** Find all contiguous vertical sequences of red (2) pixels. A vertical sequence is defined as a set of adjacent red pixels where each pixel is directly above or below another red pixel in the same column.

2.  **Bottom-Up Fill:** For each vertical red line identified, change the color of the bottom red pixel to azure (8).

3. **Propagate Upwards:** Starting with each newly azure pixel that replaced red pixel. If the pixel directly above is the color red, change the color to azure, repeat this step until the pixel above current one is not red.

4. Leave any part of input that is not part of step 3 unchanged.
"""

import numpy as np

def find_vertical_red_lines(grid):
    """Finds contiguous vertical sequences of red pixels."""
    red_lines = []
    rows, cols = len(grid), len(grid[0])
    for j in range(cols):
        start_row = -1
        for i in range(rows):
            if grid[i][j] == 2:
                if start_row == -1:
                    start_row = i
            elif start_row != -1:
                red_lines.append((start_row, i - 1, j))
                start_row = -1
        if start_row != -1:  # Handle lines ending at the last row
            red_lines.append((start_row, rows - 1, j))
    return red_lines

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    rows, cols = len(output_grid), len(output_grid[0])

    # Find vertical red lines
    red_lines = find_vertical_red_lines(output_grid)

    # Bottom-up fill and propagate upwards
    for start_row, end_row, col in red_lines:
        #change bottom to azure
        output_grid[end_row][col] = 8
        
        #propagate upwards
        current_row = end_row -1
        while current_row >= start_row and output_grid[current_row][col] == 2:
          output_grid[current_row][col] = 8
          current_row -= 1
            

    return output_grid
```
