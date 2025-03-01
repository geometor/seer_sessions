# e8593010 • 010 • example_2 • investigate_coder

---
```python
"""
Replaces white (0) pixels in the input grid with red (2), green (3), or blue (1) based on their position, 
leaving gray (5) pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing white pixels with specific colors
    based on their location.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through the grid to find white pixels
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 0:
                # Replace white pixels based on location
                if r < 3 and c < 3:
                    output_grid[r, c] = 2  # Top-left: Red
                elif r < 3 and c >= cols-3:
                    output_grid[r,c] = 3
                elif r >= rows - 3 and c < 3 :
                    output_grid[r,c] = 1
                elif r >= rows - 5 and  3 <= c < cols - 3:
                    output_grid[r,c] = 1
                elif r < rows-3 and  3 <= c < cols - 3:
                    if output_grid[r,c] == 0: # added to prevent overwrite.
                       output_grid[r,c] = 2
                elif r < rows-3 and c>= cols-3:
                    output_grid[r,c] = 3

    return output_grid
```
