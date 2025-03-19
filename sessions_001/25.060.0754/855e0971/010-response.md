# 855e0971 • 010 • example_2 • investigate_coder

---
```python
"""
The grid is divided into two regions: red (left) and blue (right). White pixels are present in both regions.
For each row containing a white pixel, all red pixels to the left of the white pixel in that row are changed to white.
For each column containing a white pixel, all red pixels in that column become white. The blue region remains unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find rows with white pixels
    rows_with_white = [r for r in range(rows) if 0 in input_grid[r, :]]
    # Find columns with white pixels
    cols_with_white = [c for c in range(cols) if 0 in input_grid[:, c]]


    # Horizontal Transformation (Row-Based)
    for r in rows_with_white:
        first_white_index = np.where(input_grid[r, :] == 0)[0][0] #find the first occurance of white
        for c in range(first_white_index):
          if output_grid[r,c] == 2:
            output_grid[r, c] = 0

    # Vertical Transformation (Column-Based)
    for c in cols_with_white:
        for r in range(rows):
            if output_grid[r,c] == 2:
                output_grid[r, c] = 0

    return output_grid
```
