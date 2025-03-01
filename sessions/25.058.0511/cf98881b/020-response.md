# cf98881b • 020 • example_4 • investigate_coder

---
```python
"""
1. **Identify Target Columns:** Examine the input grid and select columns 4, 5, 9, and 3 (indexed from 0). These correspond to the first instances of colors 4, 2, 9, and 4.

2. **Extract Sub-grid:** Create a new grid using *only* the values found in these selected columns, maintaining the original row order (top to bottom).

3.  Rearrange the grid into a square.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, 4), dtype=int)

    # Identify target columns
    target_cols = [3, 4, 5, 9] # update: include columns 3 and 5, these were present in example 3

    # Extract sub-grid and rearrange
    
    for i, col_index in enumerate(target_cols):
        if col_index < cols:
            output_grid[:, i] = input_grid[:, col_index]
        else:
           pass #If selected column not present, keep it as 0

    return output_grid.tolist()
```
