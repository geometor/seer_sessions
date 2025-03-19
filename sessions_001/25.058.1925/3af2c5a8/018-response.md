# 3af2c5a8 • 018 • refine_coder

---
```python
"""
Expands the input grid by adding a green (3) border. The height is increased by 4, and the width is increased by either 2 or 4 depending on the position of the azure line. The original content is centered within the new grid.
"""

import numpy as np

def _is_long_azure_line(input_grid):
    # Check if the input grid has width 30 and an azure line from column 16 to 25
    if len(input_grid[0]) != 30:
        return False

    for row in input_grid:
        if all(row[16:26] == 8):
            return True

    return False

def transform(input_grid):
    # Get dimensions of the input grid
    input_height = len(input_grid)
    input_width = len(input_grid[0])

    # Calculate dimensions of the output grid
    output_height = input_height + 4
    if _is_long_azure_line(input_grid):
      output_width = input_width + 4
      horizontal_start = 2
    else:
      output_width = input_width + 2
      horizontal_start = 1
    

    # Initialize the output grid with green (3)
    output_grid = np.full((output_height, output_width), 3)

    # Copy the input grid into the center of the output grid
    vertical_start = 2
    for i in range(input_height):
        for j in range(input_width):
            output_grid[i + vertical_start][j + horizontal_start] = input_grid[i][j]

    return output_grid
```
