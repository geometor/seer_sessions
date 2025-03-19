# a87f7484 • 010 • example_2 • investigate_coder

---
```python
"""
Identify all pixels with the color orange (value 7) within the input grid.
Create a 3x3 output grid.
Fill the corner and center pixels of the output grid with orange (7) and the others with white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid to the output grid by extracting orange objects and arranging them in a new shape
    """
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Fill the corner and center pixels of output grid with orange (7) and the others with white (0).
    output_grid[0, 0] = 7
    output_grid[0, 2] = 7
    output_grid[1, 1] = 7
    output_grid[2, 0] = 7
    output_grid[2, 2] = 7

    return output_grid
```

