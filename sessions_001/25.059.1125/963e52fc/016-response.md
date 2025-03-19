# 963e52fc • 016 • example_3 • investigate_coder

---
```python
"""
The central colored pattern is expanded horizontally. The two central rows in the input grid contain an alternating sequence of blue (1) and red (2) pixels.
This pattern is doubled in length horizontally. The rows with white pixels (0) are also expanded. The width gets doubled.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with doubled width, same height, and filled with 0s.
    output_grid = np.zeros((input_grid.shape[0], input_grid.shape[1] * 2), dtype=int)

    # Iterate through each row of the input grid.
    for i in range(input_grid.shape[0]):
        # Check if the row contains the pattern (1s and 2s).
        if 1 in input_grid[i] or 2 in input_grid[i]:
            # Double the pattern horizontally.
            new_row = np.concatenate((input_grid[i], input_grid[i]))
            output_grid[i] = new_row
        else:
            # expand the row by adding 0
            output_grid[i] = np.concatenate((input_grid[i], input_grid[i]))

    return output_grid
```
