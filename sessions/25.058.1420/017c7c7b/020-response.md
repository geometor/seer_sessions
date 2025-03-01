# 017c7c7b • 020 • example_3 • investigate_coder

---
```python
"""
The transformation rule is: Replace all occurrences of the value 1 (blue) in the input grid with the value 2 (red), then append three rows of the existing modified grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    # Create a copy of the input grid to modify.  This will become the output grid.
    output_grid = np.copy(input_grid)

    # Replace all 1s (blue) with 2s (red)
    output_grid[output_grid == 1] = 2
    
    # Calculate number of rows and entries for extension
    rows_to_add = output_grid[-3:,:]

    # Add the rows
    output_grid = np.vstack((output_grid, rows_to_add))

    return output_grid
```
