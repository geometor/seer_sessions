# d22278a0 • 002 • example_4 • investigate_coder

---
```python
"""
The transformation rule identifies non-zero digits in the input grid and replicates them in a checkerboard pattern in the output grid, combined with creating solid filled blocks downwards and to the right.
"""

import numpy as np

def get_non_zero_digits(grid):
    """Finds non-zero digits and their locations."""
    non_zero_digits = []
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value != 0:
                non_zero_digits.append({'value': value, 'row': r, 'col': c})
    return non_zero_digits

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    non_zero_digits = get_non_zero_digits(input_grid)

    # Create checkerboard pattern and filled regions
    for digit_info in non_zero_digits:
        value = digit_info['value']
        row_start = digit_info['row']
        col_start = digit_info['col']

        # filled blocks, going down and right
        for r in range(row_start, input_grid.shape[0]):
            for c in range(col_start,input_grid.shape[1] ):
                output_grid[r,c] = value

        # Checkerboard
        for r in range(input_grid.shape[0]):
           for c in range(input_grid.shape[1]):
               if ( (r - row_start)%2 == 0 and (c - col_start)%2 ==0) or  ((r-row_start)%2 !=0 and (c-col_start)%2 !=0) :
                if r >= row_start and output_grid[r,c] == value: # prioritize filling the blocks
                        continue; # already filled
                else:
                    if r < row_start: # fill above the digit
                         output_grid[r,c] = value if ( (r - row_start)%2 == 0 and (c - col_start)%2 ==0) or  ((r-row_start)%2 !=0 and (c-col_start)%2 !=0)  else 0

    return output_grid.tolist()
```
