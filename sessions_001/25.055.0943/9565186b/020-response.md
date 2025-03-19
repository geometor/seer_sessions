# 9565186b • 020 • example_4 • investigate_coder

---
```python
"""
The program replaces blues and greens with grey, while keeping yellow and grey pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Iterate through each pixel of the grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Change any 3(green) pixel to 5 (grey).
            if output_grid[i, j] == 3:
                output_grid[i, j] = 5
            # Change any 1(blue) pixel to 5 (grey).
            elif output_grid[i, j] == 1:
                output_grid[i, j] = 5
            # Keep all pixels that are color 4 (yellow) or 5(grey) unchanged.
            # (Implicitly handled by copying the input grid initially)

    return output_grid
```
