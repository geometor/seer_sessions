# cdecee7f • 006 • refine_coder

---
```python
"""
1.  The output is always a 3x3 grid.
2.  Identify the single non-zero pixel within the input grid.
3.  Note the column *index* of the non-zero pixel in the input grid.
4.  Place the non-zero pixel into the output grid at row 0, and the column identified in step 3.
5.  All other pixels in the output grid are 0.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # find the non-zero pixel and its column index
    non_zero_col = -1
    non_zero_val = 0
    for i, row in enumerate(input_grid):
        for j, pixel in enumerate(row):
            if pixel != 0:
                non_zero_col = j
                non_zero_val = pixel
                break  # only one non-zero, so exit inner loop
        if non_zero_col != -1:
          break # and outer

    # Place the non-zero pixel in the output grid
    if non_zero_col != -1:
      output_grid[0, non_zero_col] = non_zero_val
    

    return output_grid
```

