# 90c28cc7 • 006 • refine_coder

---
```python
"""
The transformation extracts the non-zero color in each solid horizontal color band of the input grid,
ignoring rows of all 0, and places these colors into a single-row output grid, maintaining the original order.
"""

import numpy as np

def get_color_bands(input_grid):
    """
    Identifies distinct horizontal color bands in the input grid.
    Returns a list of representative colors for each band.
    """
    bands = []
    for row in input_grid:
        # Consider only rows that have non-zero (non-white) pixels
        if np.any(row != 0):
            # Check if the row is a solid color band
            unique_colors = np.unique(row)
            if len(unique_colors) == 1:
                bands.append(unique_colors[0])
    return bands

def transform(input_grid):
    """
    Transforms the input grid into a single-row output grid by extracting
    the color from each horizontal color band.
    """
    # Identify distinct color bands and their representative colors
    bands = get_color_bands(input_grid)

    # Determine output grid dimensions (1 x number of bands)
    num_bands = len(bands)
    output_grid = np.zeros((1, num_bands), dtype=int)

    # Populate the output grid with the band colors
    for i, color in enumerate(bands):
        output_grid[0, i] = color

    return output_grid
```
