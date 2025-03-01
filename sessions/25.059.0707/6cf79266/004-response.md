# 6cf79266 • 004 • example_1 • investigate_coder

---
```python
"""
Identifies a 3x3 square of gray (5) pixels at a specific location (x=16, y=6) within a 20x20 grid and replaces it with a 3x3 square of blue (1) pixels. The rest of the grid remains unchanged.
"""

import numpy as np

def transform(input_grid):
    # Create a copy of the input grid to serve as the output grid.  We'll modify this copy.
    output_grid = np.copy(input_grid)

    # Define the dimensions of the square to be overlaid and its top-left corner coordinates.
    square_size = 3
    x_start = 16
    y_start = 6

    # Overlay a blue (1) square onto the output grid.
    output_grid[y_start:y_start + square_size, x_start:x_start + square_size] = 1

    return output_grid
```
