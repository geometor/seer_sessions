# 88a62173 • 012 • refine_coder

---
```python
"""
The transformation rule for this task is to keep the blue (color 1) pixels in the input grid exactly the same in the output grid. The output grid has the minimal dimensions to contain all blue pixels.
"""

import numpy as np

def transform(input_grid):
    # Convert input to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # Find the coordinates of all blue pixels
    blue_pixels = np.argwhere(input_grid == 1)

    # If there are no blue pixels, return an empty grid
    if len(blue_pixels) == 0:
        return []

    # Determine the dimensions of the output grid
    min_row, min_col = np.min(blue_pixels, axis=0)
    max_row, max_col = np.max(blue_pixels, axis=0)
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1

    # Initialize the output grid with zeros
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Copy the blue pixels to their corresponding positions in the output grid
    for row, col in blue_pixels:
        output_grid[row - min_row, col - min_col] = 1

    return output_grid.tolist()
```
