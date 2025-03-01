# 963e52fc • 002 • example_1 • investigate_coder

---
```python
"""
The transformation rule is to double the width of the input grid. The central pattern of alternating red (2) and azure (8) pixels in rows 1 and 2 (0-indexed) is extended, while the surrounding white (0) pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with double the width, filled with white (0)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols * 2), dtype=int)

    # Iterate through the input grid rows
    for i in range(rows):
        if i == 1 or i == 2:  # Rows with the alternating pattern (0-indexed)
            # Extend the pattern by duplicating each pixel
            k=0
            for j in range(cols):
                output_grid[i, k] = input_grid[i, j]
                output_grid[i, k+1] = input_grid[i, j]
                k+=2
        else:
            # Copy the white rows, extending their width.
            for j in range(cols * 2):
               output_grid[i,j]=0

    return output_grid
```
