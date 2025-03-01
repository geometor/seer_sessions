# e26a3af2 • 006 • refine_coder

---
```python
"""
1.  **Identify Columns of Interest:** Examine each column in the input grid. A column is considered "of interest" if it contains *any* of the colors azure (8), green (3), or red (2). The presence of other colors in the column does *not* disqualify it.
2.  **Construct Output Grid:** Create a new grid with same dimensions and initialize it by setting all the values to blue (1).
3.  **Transfer Columns:** Copy the columns of interest from the input grid to the output grid, maintaining their original positions and pixel values.
4. **Return Output Grid** Return the output grid
"""

import numpy as np

def get_columns_of_interest(grid):
    # identify columns of interest - with colors 8, 3, 2
    cols_of_interest = []
    for j in range(grid.shape[1]):
        unique_colors = np.unique(grid[:, j])
        if any(color in unique_colors for color in [8, 3, 2]):
            cols_of_interest.append(j)
    return cols_of_interest

def transform(input_grid):
    # initialize output_grid as all blue (1)
    output_grid = np.ones_like(input_grid)

    # get columns of interest
    cols_of_interest = get_columns_of_interest(input_grid)

    # place columns of interest into output_grid
    for j in cols_of_interest:
      output_grid[:,j] = input_grid[:,j]

    return output_grid
```
