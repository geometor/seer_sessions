# dc433765 • 040 • example_7 • investigate_coder

---
```python
"""
Green move to center, Yellow remain at initial position. Keep all other cells empty.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find the green and yellow pixels
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == 3:  # Green pixel
                # Move green to the center
                output_grid[rows // 2, cols // 2] = 3
            elif input_grid[i, j] == 4:  # Yellow pixel
                # Yellow stays at the same place
                output_grid[i, j] = 4

    return output_grid
```
