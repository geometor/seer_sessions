```python
"""
Determine whether to halve the rows or columns based on which dimension is larger. If rows > columns, halve the rows. Otherwise, halve the columns.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to a NumPy array for easier manipulation
    input_array = np.array(input_grid)
    rows, cols = input_array.shape

    # Determine whether to halve rows or columns
    if rows > cols:
        # Halve the rows
        output_rows = rows // 2
        output_array = input_array[:output_rows, :]
    else:
        # Halve the columns
        output_cols = cols // 2
        output_array = input_array[:, :output_cols]

    # Convert the NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```
