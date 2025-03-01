# 4093f84a • 002 • example_3 • investigate_coder

---
```python
"""
The transformation identifies a horizontal band of gray (5) pixels.  It then locates all non-gray (not 5) and non-white (not 0) pixels above and below this band. These identified pixels are replaced with gray (5) pixels.
"""

import numpy as np

def find_gray_band(grid):
    """Finds the rows that make up the gray band."""
    rows, cols = grid.shape
    gray_band_rows = []
    for r in range(rows):
        if all(grid[r, c] == 5 for c in range(cols)):
            gray_band_rows.append(r)
    return gray_band_rows

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    
    gray_band_rows = find_gray_band(output_grid)
    
    # Replace non-gray and non-white pixels with gray above and below the band
    for r in range(rows):
        if r not in gray_band_rows:  # Check if the row is NOT part of the gray band
            for c in range(cols):
                if output_grid[r, c] != 5 and output_grid[r, c] != 0:
                    output_grid[r, c] = 5

    return output_grid
```
