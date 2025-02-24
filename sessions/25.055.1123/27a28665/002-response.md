# 27a28665 • 002 • example_1 • investigate_coder

---
```python
"""
1. Observe the input grid: Examine the 3x3 input grid and identify all the colors present and their locations.
2. Count the number of 'gray' (5) pixels.
3. If the Count of 'gray' pixels is greater than or equal to 4 output 1 (blue), otherwise the output will be 0.
"""

import numpy as np

def count_pixels(grid, color):
    # Count the number of pixels of a specific color in the grid.
    return np.sum(grid == color)

def transform(input_grid):
    # Count the number of gray (5) pixels.
    gray_count = count_pixels(input_grid, 5)
    
    # Determine the output based on the count of gray pixels.
    if gray_count >= 4:
        output_grid = np.array([[1]])  # Output 1 (blue)
    else:
        output_grid = np.array([[0]])  # Output 0 (white)

    return output_grid
```
