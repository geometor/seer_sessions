# b8cdaf2b • 006 • refine_coder

---
```python
"""
Replace each white pixel with the color of the last non-white pixel below it in the same column.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Iterate through all pixels
    for i in range(rows):
        for j in range(cols):
            # Check if the pixel is white
            if input_grid[i][j] == 0:
                # Search the column from bottom to top, starting from the current row
                for k in range(rows - 1, i, -1):
                    # Find the last non-white pixel
                    if input_grid[k][j] != 0:
                        output_grid[i][j] = input_grid[k][j]
                        break  # Stop searching after finding the replacement color

    return output_grid
```
