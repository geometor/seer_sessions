```python
"""
Copies the input grid to the output, then changes the centermost pixel on the
bottom row to match a pixel color from a non-bottom row, if one exists.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_grid = input_grid.copy()

    # Locate Center Column
    center_col = width // 2

    # Find Target Value on bottom row, initially set to 0 for no change
    target_value = 0

    # Find other instance of target value in upper rows
    for r in range(height - 1):
        for c in range(width):
            if input_grid[r, c] != 0:
                target_value = input_grid[r,c]
                break  # only need first non-zero color
        if target_value !=0:
            break
    
    # only change value in output if match was found and not zero
    if target_value != 0:
      output_grid[height - 1, center_col] = target_value

    return output_grid.tolist()
```