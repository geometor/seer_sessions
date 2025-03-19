# 662c240a • 006 • refine_coder

---
```python
"""
The transformation rule can be described as follows:

1.  **Identify the Bounding Box:** Find the smallest rectangular region within the input grid that contains all the non-white (non-zero) pixels. This is equivalent to finding the minimum and maximum row and column indices where non-white pixels exist.
2.  **Extract Subgrid:** Extract the subgrid defined by this bounding box. This subgrid becomes the output grid.

In simpler terms, imagine drawing the tightest possible rectangle around all the colored pixels. The content of that rectangle is the output.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the subgrid defined by the bounding box of non-zero pixels.
    """
    # Convert input_grid to a NumPy array
    input_array = np.array(input_grid)

    # Find the indices of non-zero elements
    non_zero_indices = np.argwhere(input_array != 0)

    # If there are no non-zero elements, return an empty grid (or a default, like a 1x1 grid with 0)
    if non_zero_indices.size == 0:
        return [[0]]  # Or return [] if a truly empty grid is desired

    # Find the minimum and maximum row and column indices
    min_row = non_zero_indices[:, 0].min()
    max_row = non_zero_indices[:, 0].max()
    min_col = non_zero_indices[:, 1].min()
    max_col = non_zero_indices[:, 1].max()

    # Extract the subgrid using array slicing
    output_array = input_array[min_row:max_row+1, min_col:max_col+1]

    # Convert the NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```

