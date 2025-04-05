```python
"""
Transforms the input grid based on the relative density of '7's in rows versus columns.

1. Calculate the maximum number of '7's found in any single row (`max_row_sevens`).
2. Calculate the maximum number of '7's found in any single column (`max_col_sevens`).
3. If `max_col_sevens` is strictly greater than `max_row_sevens`:
    - Apply "column gravity": For each column independently, move all '7's to the
      bottom, stacking them up, and fill the remaining cells above with '0's.
4. Otherwise (if `max_row_sevens` is greater than or equal to `max_col_sevens`):
    - Apply "row gravity": For each row independently, move all '7's to the
      right, stacking them against the right edge, and fill the remaining cells
      to the left with '0's.
"""

import numpy as np

def transform(input_grid):
    """
    Applies either column gravity or row gravity based on maximum densities.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid)
    rows, cols = input_array.shape
    
    # Initialize the output grid with zeros, same dimensions as input
    output_array = np.zeros_like(input_array)
    
    # Value to manipulate
    target_value = 7

    # Calculate max '7's per row
    max_row_sevens = 0
    for r in range(rows):
        # Count non-zero elements matching target_value in the current row
        row_count = np.count_nonzero(input_array[r, :] == target_value)
        # Update maximum if current row count is higher
        if row_count > max_row_sevens:
            max_row_sevens = row_count

    # Calculate max '7's per column
    max_col_sevens = 0
    for c in range(cols):
        # Count non-zero elements matching target_value in the current column
        col_count = np.count_nonzero(input_array[:, c] == target_value)
        # Update maximum if current column count is higher
        if col_count > max_col_sevens:
            max_col_sevens = col_count

    # Decide transformation logic based on max counts comparison
    if max_col_sevens > max_row_sevens:
        # Apply column gravity (fall down)
        # Iterate through each column
        for c in range(cols):
            # Count the number of '7's in this input column
            num_sevens = np.count_nonzero(input_array[:, c] == target_value)
            # If there are any '7's in this column
            if num_sevens > 0:
                # Place the '7's at the bottom of the corresponding output column
                # Start filling from the bottom row index (rows - num_sevens) up to the last row (rows - 1)
                output_array[rows - num_sevens:, c] = target_value
    else:
        # Apply row gravity (push right)
        # Iterate through each row
        for r in range(rows):
            # Count the number of '7's in this input row
            num_sevens = np.count_nonzero(input_array[r, :] == target_value)
            # If there are any '7's in this row
            if num_sevens > 0:
                # Place the '7's at the right end of the corresponding output row
                # Start filling from the rightmost column index (cols - num_sevens) up to the last column (cols - 1)
                output_array[r, cols - num_sevens:] = target_value

    # Convert the output NumPy array back to a list of lists for the required format
    output_grid = output_array.tolist()

    return output_grid
```