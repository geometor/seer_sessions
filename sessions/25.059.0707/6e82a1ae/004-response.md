# 6e82a1ae • 004 • example_1 • investigate_coder

---
```python
"""
Transforms an input grid by replacing gray (5) pixels with blue (1), red (2), or green (3) based on their location. White (0) pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell of the input grid.
    for i in range(rows):
        for j in range(cols):
            # Preserve any cell with the value 0 (white).
            if output_grid[i, j] == 0:
                continue
            # Identify cells with the value 5 (gray).
            elif output_grid[i, j] == 5:
                # Replace based on location
                if i < rows / 2 and j >= cols / 2:  # Top-right quadrant
                    output_grid[i, j] = 1  # Blue
                elif i >= rows / 2 and j >= cols / 2:  # Bottom-right quadrant
                    output_grid[i, j] = 2  # Red
                elif i >= rows / 2 and j < cols / 4:   # left middle region
                    output_grid[i,j] = 3

    return output_grid
```
