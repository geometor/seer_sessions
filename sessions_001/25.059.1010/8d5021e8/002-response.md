# 8d5021e8 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation takes the input grid, expands it, and creates a symmetrical pattern by replicating non-zero pixels. The output grid's dimensions are 2x the input width and 3x the input height. Non-zero pixels from the input are placed in the top-left quadrant of the output grid, and then mirrored/rotated to the top-right, bottom-right and bottom-left, and all remaining pixels are filled with 0.
"""

import numpy as np

def transform(input_grid):
    input_rows, input_cols = input_grid.shape
    output_rows = 3 * input_rows
    output_cols = 2 * input_cols
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through the input grid
    for i in range(input_rows):
        for j in range(input_cols):
            pixel_value = input_grid[i, j]
            if pixel_value != 0:
                # Top-left quadrant (original position)
                output_grid[i, j] = pixel_value

                # Top-right quadrant (90-degree rotation)
                output_grid[i, output_cols - 1 - j] = pixel_value
                
                # Bottom-right quadrant (180-degree rotation)
                output_grid[output_rows - 1 - i, output_cols - 1- j] = pixel_value
                
                # Bottom-left quadrant (270-degree rotation)
                output_grid[output_rows -1 - i, j] = pixel_value

    return output_grid
```
