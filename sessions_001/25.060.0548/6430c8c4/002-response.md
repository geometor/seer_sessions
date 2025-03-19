# 6430c8c4 • 002 • example_4 • investigate_coder

---
```python
"""
The input grid is compressed into a 4x4 output grid. If any orange (7) pixels are present in the region of the input grid corresponding to a cell in the output grid, that output cell is colored green (3). Otherwise, the output cell is colored white (0).
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape
    output_grid = np.zeros((4, 4), dtype=int)

    # Calculate the size of the regions in the input grid
    height_step = input_height / 4
    width_step = input_width / 4

    # Iterate through each cell of the output grid
    for i in range(4):
        for j in range(4):
            # Define the boundaries of the corresponding region in the input grid
            start_row = int(i * height_step)
            end_row = int((i + 1) * height_step)
            start_col = int(j * width_step)
            end_col = int((j + 1) * width_step)

            # Extract the region from the input grid
            region = input_grid[start_row:end_row, start_col:end_col]

            # Check if any orange (7) pixel is present in the region
            if 7 in region:
                output_grid[i, j] = 3  # Set to green
            else:
                output_grid[i, j] = 0  # Set to white

    return output_grid.tolist()
```
