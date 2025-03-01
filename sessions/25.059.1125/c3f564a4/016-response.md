# c3f564a4 • 016 • example_3 • investigate_coder

---
```python
"""
The transformation performs a cyclic permutation of the non-zero values in the grid, 
shifting them down by one row and to the right by one column. The zero are not 
moved, but take the values from the shifted pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)

    # Iterate through each cell in the input grid
    for r in range(rows):
        for c in range(cols):
            # Perform cyclic shift for non-zero values
            if input_grid[r, c] != 0:
                new_r = (r + 1) % rows
                new_c = (c + 1) % cols
                output_grid[new_r, new_c] = input_grid[r, c]

    return output_grid
```
