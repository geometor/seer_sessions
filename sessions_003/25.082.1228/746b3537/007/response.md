```python
"""
Transforms the input grid by extracting the first element of each unique row, preserving their original order, and constructing the output grid from these elements.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting the first element of each unique row.
    """
    unique_rows = []
    first_elements = []

    # Iterate through each row of the input grid
    for row in input_grid:
        # Convert the row to a list to make it hashable for comparison
        row_list = list(row)

        # Check if this row is already in the unique_rows list
        if row_list not in unique_rows:
            unique_rows.append(row_list)

    # Extract the first element of each unique row
    for row in unique_rows:
        first_elements.append(row[0])

    # Convert the list of first elements to a NumPy array of shape (N, 1)
    return np.array(first_elements).reshape(-1, 1)
```
