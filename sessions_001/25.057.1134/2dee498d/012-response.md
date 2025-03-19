# 2dee498d • 012 • refine_coder

---
```python
"""
The input grid is transformed into the output grid by keeping only the columns that are identical to all other columns in the input. If all columns are identical, keep all of them. If a column differs from any other, remove it.
"""

import numpy as np

def transform(input_grid):
    # Convert input to numpy array for easier manipulation
    input_grid = np.array(input_grid)
    num_rows = input_grid.shape[0]
    num_cols = input_grid.shape[1]

    # Initialize an empty list to store columns to keep
    cols_to_keep = []

    # Iterate through each column
    for j in range(num_cols):
        current_col = input_grid[:, j]
        all_same = True

        # Compare the current column with all other columns
        for k in range(num_cols):
            other_col = input_grid[:, k]
            if not np.array_equal(current_col, other_col):
                all_same = False
                break  # Exit the inner loop if a different column is found

        # If the current column is the same as all others, add its index to cols_to_keep
        if all_same:
            cols_to_keep.append(j)

    # If no columns are identical to each other, cols_to_keep will be empty and no columns are kept
    # Construct the output grid using only the selected columns
    output_grid = input_grid[:, cols_to_keep].tolist()


    return output_grid
```
