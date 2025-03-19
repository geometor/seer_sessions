# 10fcaaa3 • 002 • example_4 • investigate_coder

---
```python
"""
The transformation rule replicates non-zero pixels from the input grid to the output grid, expanding the grid and inserting rows and columns of color 8 (blue).

1. **Identify Non-Zero Pixels:** Locate all pixels in the input grid with a value other than 0.
2. **Replicate and Position:** For each non-zero pixel, place it at output[2r, 2c]
3. **Insert Blue Rows/Columns:**
    -If a row is only zeros in the input, it gets duplicated in the output, and an all blue (8) line is inserted below the duplicated row.
    - If a column is all zeros, it gets duplicated in the output, and a blue (8) column is inserted after it.
    - if a pixel at `input[r,c]` exists and it is not `0`. Put this pixel at `output[2r, 2c]`.
    - if a pixel does not exist at `input[r,c]` because the row index is out of bound, then add rows of zeros at the end and insert the all `8` rows after the just appended rows
    - if a pixel does not exist at `input[r,c]` because the col index is out of bound, then add cols of zeros at the end and insert the all `8` cols after the just appended cols
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_rows, input_cols = input_grid.shape

    # Initialize output grid dimensions (find max needed)
    output_rows = 2 * input_rows
    output_cols = 2 * input_cols
    
    for r in range(input_rows):
      if all(input_grid[r,:] == 0):
        output_rows +=1
    for c in range(input_cols):
      if all(input_grid[:,c] == 0):
        output_cols += 1
        
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Add blue rows at the end
    row_offset = 0
    for r in range(input_rows):
      if all(input_grid[r,:] == 0):
        output_grid[2*r + row_offset,:] = 0
        row_offset+=1
        output_grid[2*r + row_offset,:] = 8
      else:
        for c in range(input_cols):
            output_grid[2*r + row_offset, 2*c] = input_grid[r,c]
    # Add blue columns
    col_offset = 0
    for c in range(input_cols):
      if all(input_grid[:,c] == 0):
        output_grid[:, 2*c + col_offset] = output_grid[:, 2*c + col_offset] * 1 # keep existing
        col_offset+=1
        output_grid[:, 2*c + col_offset] = 8

    return output_grid.tolist()
```
