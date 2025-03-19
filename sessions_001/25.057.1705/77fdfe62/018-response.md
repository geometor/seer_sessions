# 77fdfe62 • 018 • refine_coder

---
```python
"""
The transformation rule extracts the colors from the four 2x2 corner regions of the input grid and uses them to fill corresponding 2x2 quadrants in the output grid. The output grid has the same shape as the example output grids. Each quadrant in the output is filled with the color from its input corner.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)
    
    # Get input grid dimensions
    input_height, input_width = input_grid.shape

    # Initialize output grid with the dimensions matching the 2x2 corner regions replicated
    output_grid = np.zeros((input_height, input_width), dtype=int)

    # Top-left corner
    top_left_color = input_grid[0, 0]
    output_grid[0:2, 0:2] = top_left_color

    # Top-right corner
    top_right_color = input_grid[0, input_width - 1]
    output_grid[0:2, input_width - 2:input_width] = top_right_color

    # Bottom-left corner
    bottom_left_color = input_grid[input_height - 1, 0]
    output_grid[input_height - 2:input_height, 0:2] = bottom_left_color

    # Bottom-right corner
    bottom_right_color = input_grid[input_height - 1, input_width - 1]
    output_grid[input_height - 2:input_height, input_width - 2:input_width] = bottom_right_color

    return output_grid
```
