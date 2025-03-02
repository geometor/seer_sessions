# bc1d5164 • 004 • example_1 • investigate_coder

---
```python
"""
Extracts the smallest rectangle from the input grid that contains all azure (8) pixels.
"""

import numpy as np

def get_bounding_box(grid):
    #Find the min and max row and column indices of the azure pixels.
    rows, cols = np.where(grid == 8)
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Transforms the input grid by extracting the bounding box of azure pixels.
    """
    # Convert input to numpy array
    input_array = np.array(input_grid)

    # Find the bounding box
    min_row, max_row, min_col, max_col = get_bounding_box(input_array)

    # Extract the subgrid
    output_grid = input_array[min_row:max_row+1, min_col:max_col+1]

    return output_grid.tolist()
```
