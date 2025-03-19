# 4c4377d9 • 008 • example_2 • investigate_coder

---
```python
"""
The transformation rule is:
1. Flip: Take the input grid and create a vertically flipped copy of it.
2. Stack: Stack the vertically flipped copy of the input on top of the original input grid.
3. Output Resulting Grid: The stacked array constitutes the transformed output.
"""

import numpy as np

def transform(input_grid):
    # Create a vertically flipped copy of the input grid.
    flipped_grid = np.flipud(input_grid)

    # Stack the flipped grid on top of the original input grid.
    output_grid = np.vstack((flipped_grid, input_grid))

    return output_grid
```
