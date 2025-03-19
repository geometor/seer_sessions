# cf98881b • 002 • example_1 • investigate_coder

---
```python
"""
Selects specific columns (1, 3, 9, and 12, zero-indexed) from the input grid and constructs a new grid from these columns, preserving the original row order and values.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by selecting specific columns.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid.
    """
    input_grid = np.array(input_grid)
    rows = input_grid.shape[0]
    cols = input_grid.shape[1]
    output_grid = np.zeros((rows,4), dtype=int)

    # select input columns
    selected_columns = [0, 2, 8, 11]

    # build output by gathering selected input columns
    output_col_index = 0
    for input_col_index in selected_columns:
        if input_col_index < cols:
            output_grid[:, output_col_index] = input_grid[:, input_col_index]
            output_col_index += 1

    return output_grid.tolist()
```
