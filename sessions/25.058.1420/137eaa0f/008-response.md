# 137eaa0f • 008 • refine_coder

---
```python
"""
Arranges colored pixels from the input grid into a 3x3 output grid based on color-specific rules.
"""

import numpy as np

def transform(input_grid):
    # Initialize a 3x3 output grid filled with zeros.
    output_grid = np.zeros((3, 3), dtype=int)

    # Count the number of pixels of each color (magenta, orange, grey, yellow).
    pixel_counts = {}
    for color in [4, 5, 6, 7]:  # Only count relevant colors
        pixel_counts[color] = np.sum(input_grid == color)

    # Place Magenta (6) pixels.
    magenta_count = pixel_counts.get(6, 0)
    for i in range(min(magenta_count, 3)):  # Limit to 3 (width of the grid)
        output_grid[0, i] = 6

    # Place Orange (7) pixels.
    orange_count = pixel_counts.get(7, 0)
    if orange_count >= 1:
        output_grid[0, 2] = 7
    if orange_count >= 2:
        output_grid[1, 2] = 7

    # Place Grey (5) pixels.
    grey_count = pixel_counts.get(5, 0)
    if grey_count >= 1:
        output_grid[1, 1] = 5

    # Place Yellow (4) pixels.
    yellow_count = pixel_counts.get(4, 0)
    for i in range(min(yellow_count, 3)):  # Limit to 3 (width of the grid)
        output_grid[2, i] = 4

    return output_grid
```
