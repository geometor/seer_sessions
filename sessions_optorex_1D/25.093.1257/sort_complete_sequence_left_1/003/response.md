```python
"""
Identifies the unique non-zero digit (X) in the last 8 elements of the 12-element input sequence/array.
Constructs the output sequence/array by keeping the first 4 elements (always 0) and replacing
the last 8 elements with a fixed pattern using the identified digit X: X, X, X, 0, X, X, 0, X.
"""

import numpy as np

def find_key_digit(suffix_list):
    """
    Finds the unique non-zero digit in a list or array of digits.
    Assumes there is exactly one unique non-zero digit present.

    Args:
        suffix_list: A list or array containing the last 8 digits of the input.

    Returns:
        The unique non-zero digit found, or 0 if none are found (though unlikely).
    """
    for digit in suffix_list:
        if digit != 0:
            return digit
    # Fallback if no non-zero digit is found (based on examples, should not happen)
    return 0

def transform(input_grid):
    """
    Applies the transformation rule to the input grid (sequence/array).

    Args:
        input_grid: A NumPy array or list-like structure of 12 integers.

    Returns:
        A NumPy array representing the transformed sequence of 12 integers.
    """
    # Ensure input is a NumPy array for consistent handling
    input_array = np.array(input_grid)

    # Initialize output_grid as a copy or a new array of the same size
    # A new array is safer if the input shouldn't be modified
    output_grid = np.zeros_like(input_array)

    # Extract the prefix and suffix from the input
    prefix = input_array[:4] # First 4 elements
    input_suffix = input_array[4:] # Last 8 elements

    # Identify the unique non-zero digit (X) in the input suffix
    key_digit = find_key_digit(input_suffix)

    # Construct the output suffix based on the fixed pattern
    # Pattern: X, X, X, 0, X, X, 0, X
    output_suffix = np.array([
        key_digit, key_digit, key_digit, 0,
        key_digit, key_digit, 0, key_digit
    ])

    # Combine the prefix (which is always zeros in this case, so we can just assign)
    # and the new output suffix into the output grid
    # output_grid[:4] is already initialized to zeros
    output_grid[4:] = output_suffix

    return output_grid
```