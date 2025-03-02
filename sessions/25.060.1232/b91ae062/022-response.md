# b91ae062 • 022 • example_4 • investigate_coder

---
```python
"""
The transformation takes each pixel in the input 3x3 grid and expands it into a 3x3 block of the same color in the output 9x9 grid. The relative positions of the colors are maintained.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a 9x9 array filled with zeros
    output_grid = np.zeros((9, 9), dtype=int)

    # Iterate through each cell in the input grid
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            # Get the color of the current cell
            color = input_grid[i, j]

            # Expand the cell into a 3x3 block in the output grid
            for x in range(3):
                for y in range(3):
                    output_grid[i*3 + x, j*3 + y] = color

    return output_grid
```
