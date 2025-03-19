# d0f5fe59 • 014 • refine_coder

---
```python
"""
Downscales a 12x12 input grid to a 3x3 output grid.
Each pixel in the output grid corresponds to a 4x4 region in the input grid.
If *all* pixels within the 4x4 region are azure (8), the output pixel is set to azure (8).
Otherwise, the output pixel is set to white (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a 3x3 array filled with white (0).
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through the output grid's rows and columns.
    for row in range(3):
        for col in range(3):
            # Define the corresponding 4x4 region in the input grid.
            start_row = row * 4
            end_row = start_row + 4
            start_col = col * 4
            end_col = start_col + 4

            # Extract the 4x4 region from the input grid.
            region = input_grid[start_row:end_row, start_col:end_col]

            # Check if the 4x4 region contains *only* azure (8) pixels.
            if np.all(region == 8):
                # If all pixels are azure, set output to azure.
                output_grid[row, col] = 8

    return output_grid
```

