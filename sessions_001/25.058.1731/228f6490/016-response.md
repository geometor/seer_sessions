# 228f6490 • 016 • example_3 • investigate_coder

---
```python
"""
The transformation rule is as follows:
1. Change all Red(2) pixels to White(0).
2. Change all Azure(8) pixels to White(0).
3. Keep all other colors unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rule:
    Red(2) -> White(0)
    Azure(8) -> White(0)
    Other colors remain unchanged.
    """
    output_grid = np.copy(input_grid)

    # Iterate through the grid
    for row_index, row in enumerate(input_grid):
        for col_index, pixel in enumerate(row):
            # Change Red(2) to White(0)
            if pixel == 2:
                output_grid[row_index][col_index] = 0
            # Change Azure(8) to White(0)
            elif pixel == 8:
                output_grid[row_index][col_index] = 0

    return output_grid
```
