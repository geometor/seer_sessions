```python
import numpy as np

"""
Processes a 2D grid (NumPy array) row by row. For each row:
Identifies the first and last non-zero digits in the row.
Counts the number of leading zeros (before the first non-zero) and trailing zeros (after the last non-zero).
If the count of leading zeros is less than or equal to the count of trailing zeros, replaces the leading zeros in that row with the value of the first non-zero digit.
Otherwise (if leading zeros count is greater), replaces the trailing zeros in that row with the value of the last non-zero digit.
If a row contains only zeros, it remains unchanged.
"""

def find_first_non_zero_row(row):
    """
    Finds the value and index of the first non-zero element in a 1D array (row).

    Args:
        row: A 1D NumPy array.

    Returns:
        A tuple (value, index) of the first non-zero element.
        Returns (None, -1) if all elements are zero or the row is empty.
    """
    non_zero_indices = np.nonzero(row)[0] # Get indices of non-zero elements
    if non_zero_indices.size > 0:
        first_idx = non_zero_indices[0]
        first_val = row[first_idx]
        return first_val, first_idx
    else:
        return None, -1 # All zeros or empty

def find_last_non_zero_row(row):
    """
    Finds the value and index of the last non-zero element in a 1D array (row).

    Args:
        row: A 1D NumPy array.

    Returns:
        A tuple (value, index) of the last non-zero element.
        Returns (None, -1) if all elements are zero or the row is empty.
    """
    non_zero_indices = np.nonzero(row)[0] # Get indices of non-zero elements
    if non_zero_indices.size > 0:
        last_idx = non_zero_indices[-1]
        last_val = row[last_idx]
        return last_val, last_idx
    else:
        return None, -1 # All zeros or empty

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule row-by-row to the input grid.

    Args:
        input_grid: The input 2D NumPy array.

    Returns:
        The transformed 2D NumPy array.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    num_rows, num_cols = input_grid.shape

    # Iterate through each row
    for r in range(num_rows):
        current_row = input_grid[r, :]

        # Find the first non-zero digit and its index for the current row
        first_val, first_idx = find_first_non_zero_row(current_row)

        # If the row is all zeros, skip to the next row
        if first_val is None:
            continue

        # Find the last non-zero digit and its index for the current row
        # (We know there's at least one non-zero if first_val wasn't None)
        last_val, last_idx = find_last_non_zero_row(current_row)

        # Calculate the number of leading zeros
        num_left_zeros = first_idx

        # Calculate the number of trailing zeros
        num_right_zeros = (num_cols - 1) - last_idx

        # Compare the number of leading and trailing zeros
        if num_left_zeros <= num_right_zeros:
            # Fill leading zeros in the output grid's row with the first non-zero value
            output_grid[r, :first_idx] = first_val
        else:
            # Fill trailing zeros in the output grid's row with the last non-zero value
            output_grid[r, last_idx + 1:] = last_val

    # Return the modified grid
    return output_grid
```