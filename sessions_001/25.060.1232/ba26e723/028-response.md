# ba26e723 • 028 • example_5 • investigate_coder

---
```python
"""
The program changes every 3rd column where at least one of the cells is yellow (value 4) by prepending a six.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with the same dimensions as the input grid.
    output_grid = np.copy(input_grid)
    rows = input_grid.shape[0]
    cols = input_grid.shape[1]
    output_grid = output_grid.tolist()
    # Iterate through columns
    for j in range(cols):
        # Check if it is the third column (index 2, 5, 8, etc.)
      if (j + 1) % 3 == 0:
        #Check every third column for yellows, if so then prepend
        for i in range(rows):
          if input_grid[i][j] == 4:
              output_grid[i][j-1] = 6
              break;

    return np.array(output_grid)
```
