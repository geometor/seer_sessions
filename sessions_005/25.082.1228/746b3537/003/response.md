```python
"""
Identifies and extracts the unique rows from the input grid, preserving their original order, and constructs the output grid by stacking these unique rows vertically.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting unique rows.
    """
    unique_rows = []

    # Iterate through each row of the input grid
    for row in input_grid:
        # Convert the row to a tuple to make it hashable for comparison
        row_tuple = tuple(row)

        # Check if this row is already in the unique_rows list
        is_unique = True
        for unique_row in unique_rows:
            if row_tuple == tuple(unique_row):
                is_unique = False
                break

        # If the row is unique, add it to the list
        if is_unique:
            unique_rows.append(list(row)) # store as list

    # Convert the list of unique rows to a NumPy array
    return np.array(unique_rows)
```