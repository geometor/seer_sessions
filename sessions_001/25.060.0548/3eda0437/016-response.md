# 3eda0437 • 016 • refine_coder

---
```python
"""
The transformation rule is: In each row of the input grid, find the *first* sequence of three consecutive white (0) pixels and replace them with magenta (6) pixels. Leave all other pixels unchanged. If a row does not have at least three consecutive white pixels, do not alter the row at all.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rule: replace the first three consecutive white pixels with magenta pixels in each row.
    """
    output_grid = input_grid.copy()  # Initialize output_grid as a copy of the input.

    # Iterate over each row
    for row_index in range(output_grid.shape[0]):
        row = output_grid[row_index]
        # Iterate through the row to find the first sequence of three consecutive white pixels
        for i in range(len(row) - 2):
            if row[i] == 0 and row[i+1] == 0 and row[i+2] == 0:
                # Replace the three white pixels with magenta (6)
                output_grid[row_index, i:i+3] = 6
                break  # Stop after the first replacement in the row

    return output_grid
```
