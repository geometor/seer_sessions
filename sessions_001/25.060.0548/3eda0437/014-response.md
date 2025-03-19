# 3eda0437 • 014 • refine_coder

---
```python
"""
The transformation rule is: In each row of the input grid, replace the *first* three consecutive white (0) pixels with magenta (6) pixels. Leave all other pixels unchanged. If a row does not have at least three consecutive white pixels at the beginning, do not alter the row at all.
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

        # Check if the first three pixels are white
        if len(row) >= 3 and all(row[i] == 0 for i in range(3)):
            # Replace the first three pixels with magenta (6)
            output_grid[row_index, :3] = 6

    return output_grid
```
