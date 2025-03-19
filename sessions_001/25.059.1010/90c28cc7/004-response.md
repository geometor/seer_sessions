# 90c28cc7 • 004 • example_1 • investigate_coder

---
```python
"""
The transformation extracts the first non-zero color in each solid horizontal color band of the input grid,
ignoring rows of all 0, and places these colors into a smaller output grid, maintaining the original order.
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
            # Extract the first non-zero color as representative of the band
            first_non_zero = row[row != 0][0]
            bands.append(first_non_zero)
    return bands

def transform(input_grid):
    """
    Transforms the input grid into a smaller output grid by extracting
    representative colors from horizontal color bands.
    """
    # Identify distinct color bands and their representative colors
    bands = get_color_bands(input_grid)

    # Determine output grid dimensions (up to 3x3)
    num_bands = len(bands)
    output_height = min(num_bands, 3)
    output_width = min(len(bands) + 1, 3)

    # Initialize the output grid with zeros and shape of 3 x len(bands)
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    #populate based on number of bands detected
    if num_bands >= 1:
        output_grid[0,0] = bands[0]
    if num_bands >= 2:
        output_grid[0,1] = bands[1]
    if num_bands >= 3:
        output_grid[0,2] = bands[2]
    if num_bands >= 4:
        output_grid[1,0] = bands[3]
    if num_bands >= 5:
        output_grid[1,1] = bands[4]
    if num_bands >= 6:
        output_grid[1,2] = bands[5]
    if num_bands >= 7:
        output_grid[2,0] = bands[6]
    if num_bands >= 8:
        output_grid[2,1] = bands[7]
    if num_bands >= 9:
        output_grid[2,2] = bands[8]
    # we will stop at 3x3 (9)

    return output_grid
```
