# 662c240a • 008 • example_2 • investigate_coder

---
```python
"""
Extracts a 3x3 subgrid from the input grid. The subgrid starts at row 4 (index 3)
and includes all columns. The colors in the subgrid are preserved.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts a 3x3 subgrid from the input, starting at row index 3.
    """
    # Convert input grid to a NumPy array for easier slicing.
    input_array = np.array(input_grid)

    # Determine the dimensions of the input grid.
    rows, cols = input_array.shape

    # Define start and end indices for rows and columns of subgrid
    start_row = 3
    end_row = 6
    start_col = 0
    end_col = 3

    # Extract the subgrid using array slicing.
    output_array = input_array[start_row:end_row, start_col:end_col]

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid
```

