# 3de23699 • 026 • refine_coder

---
```python
"""
The transformation filters and repositions azure pixels from the input grid to a smaller output grid. The output grid contains only azure pixels, and its dimensions are roughly half the size of the input grid (with specific adjustments). Azure pixel positions from even rows (excluding the last) in the input are used to position in the output.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Calculate output dimensions (compression).
    output_rows = rows // 2 - 1 if rows // 2 -1 > 1 else rows // 2
    output_cols = (cols + 1) // 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Find and reposition azure pixels.
    output_row = 0
    output_col_even = 0  # Track even columns
    output_col_odd = 1   # Track odd columns

    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 8:
                if r%2 == 0 and r != (rows -1):

                    if (c%2) == 0:
                        if output_col_even < output_cols:
                            output_grid[output_row, output_col_even] = 8
                        output_col_even += 2
                    else:
                        if output_col_odd < output_cols:
                            output_grid[output_row, output_col_odd] = 8
                        output_col_odd += 2

                    if output_col_even >= output_cols and output_col_odd >= output_cols:
                        output_row +=1
                        output_col_even = 0
                        output_col_odd = 1
    return output_grid.tolist()
```
