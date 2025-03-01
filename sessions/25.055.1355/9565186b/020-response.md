# 9565186b • 020 • example_4 • investigate_coder

---
```python
"""
Copy the middle row of the input grid to the output grid.
Change any color in the input other than yellow to grey in the output.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Iterate through all cells of the input grid
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            # Check if the pixel is NOT yellow (4)
            if input_grid[i, j] != 4:
                # Change the corresponding pixel in output_grid to grey (5)
                output_grid[i, j] = 5

    return output_grid
```
