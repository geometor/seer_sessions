# d037b0a7 • 014 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Key Pixels:** Locate non-white pixels in the input grid.
2.  **Propagate Colors Downward:** For each non-white pixel in the top row (row 0), its color is copied to all the rows in that column that are below it. If other color appears in column below the current color it copies down until that point.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # change output pixels 
    # Iterate through each column.
    for j in range(cols):
        # Find the top-most non-white pixel.
        for i in range(rows):
            if input_grid[i][j] != 0:
                color = input_grid[i][j]
                
                # Propagate the color downwards.
                for k in range(i, rows):
                    output_grid[k][j] = color
                break # Move onto next col
    

    return output_grid
```
