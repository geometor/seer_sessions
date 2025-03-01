# 7fe24cdd • 002 • example_3 • investigate_coder

---
```python
"""
The input is a 3x3 grid. The output is a 6x6 grid. The transformation expands the input grid,
rearranging and replicating the original pixels in a specific "cross" pattern. The color pattern in
the input grid forms four quadrants that make a cross-like structure in the larger grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize the 6x6 output grid with zeros.
    output_grid = np.zeros((6, 6), dtype=int)

    # Iterate through the input grid.
    for i in range(3):
        for j in range(3):
            # Get the color of the current pixel.
            color = input_grid[i, j]

            # Apply the cross pattern transformation.
            x1 = i if i < 2 else i + 2
            y1 = j if j < 2 else j + 2
            output_grid[x1, y1] = color

            x2 = i + 3 if i < 2 else i - 1
            y2 = j if j < 2 else j + 2
            output_grid[x2, y2] = color

            x3 = i if i < 2 else i + 2
            y3 = j + 3 if j < 2 else j - 1
            output_grid[x3, y3] = color

            x4 = i + 3 if i < 2 else i -1
            y4 = j + 3 if j < 2 else j - 1
            output_grid[x4, y4] = color

    return output_grid
```
