# d406998b • 016 • example_3 • investigate_coder

---
```python
"""
Replace gray pixels (value 5) with green pixels (value 3) in the top-left quadrant of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing 5s with 3s in the top-left quadrant.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through the top-left quadrant
    for i in range(rows):
        for j in range(cols):
            #check if within top-left quadrant, using integer division
            if i < rows // 2 and j < cols // 2:
                # Conditional Replacement
                if output_grid[i, j] == 5:
                    output_grid[i, j] = 3
    return output_grid
```
