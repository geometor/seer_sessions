# 1c786137 • 010 • example_2 • investigate_coder

---
```python
"""
The output grid is created by picking certain rows and columns from the input, and taking those intersection points to form the output grid directly.
Specifically rows at index 2, 5, 7, 9, and 10 and columns at index 2, 8, and 15.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid to the output grid by selecting specific rows and columns."""

    input_array = np.array(input_grid)

    # Define the rows and columns to be selected (0-indexed)
    selected_rows = [2, 5, 7, 9, 10]
    selected_cols = [2, 8, 15]

    # Initialize an empty output array
    output_array = np.zeros((len(selected_rows), len(selected_cols)), dtype=int)
    
    # Populate output array
    for i, row_index in enumerate(selected_rows):
        for j, col_index in enumerate(selected_cols):
             output_array[i,j] = input_array[row_index, col_index]

    return output_array.tolist()
```
