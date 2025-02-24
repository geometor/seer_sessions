# ed36ccf7 • 002 • example_1 • investigate_coder

---
```python
"""
The top-left '9' becomes a '0', and the two zeroes in the first row becomes '9'.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # change top-left pixel to white (0)
    output_grid[0, 0] = 0

    # Find the indices of the first two white pixels (0)
    white_indices = np.where(input_grid.flatten() == 0)[0]
    if len(white_indices) >= 2:
      output_grid.reshape(-1,)[white_indices[0]] = 9
      output_grid.reshape(-1,)[white_indices[1]] = 9

    return output_grid
```
