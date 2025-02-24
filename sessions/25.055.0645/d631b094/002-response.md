# d631b094 • 002 • example_1 • investigate_coder

---
```python
"""
Counts the number of blue pixels (value 1) in the input grid and creates a 1-row output grid where the length is equal to number of blue pixels
and all pixels are blue.
"""

import numpy as np

def count_blue_pixels(grid):
    """Counts the number of blue pixels (value 1) in a grid."""
    count = 0
    for row in grid:
        for pixel in row:
            if pixel == 1:
                count += 1
    return count

def transform(input_grid):
    """Transforms the input grid into the output grid."""

    # Count blue pixels in the input grid.
    blue_count = count_blue_pixels(input_grid)

    # Create output grid: 1 x blue_count, filled with blue (1s).
    output_grid = np.ones((1, blue_count), dtype=int)

    return output_grid
```
