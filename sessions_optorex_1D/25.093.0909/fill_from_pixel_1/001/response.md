```python
import math

"""
Identifies the first and last non-zero digits in a sequence of 12 digits.
Counts the number of leading zeros (before the first non-zero) and trailing zeros (after the last non-zero).
If the count of leading zeros is less than or equal to the count of trailing zeros, replace the leading zeros with the value of the first non-zero digit.
Otherwise, replace the trailing zeros with the value of the last non-zero digit.
If the sequence contains only zeros, return it unchanged.
"""

def find_first_non_zero(seq):
    """Finds the value and index of the first non-zero element."""
    for i, val in enumerate(seq):
        if val != 0:
            return val, i
    return None, -1 # Return None and -1 if all zeros

def find_last_non_zero(seq):
    """Finds the value and index of the last non-zero element."""
    last_val = None
    last_idx = -1
    for i, val in enumerate(seq):
        if val != 0:
            last_val = val
            last_idx = i
    return last_val, last_idx

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input sequence string.

    Args:
        input_str: A string of 12 space-separated digits.

    Returns:
        A string representing the transformed sequence.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_str.split()]
    n = len(input_list) # Should be 12 based on examples

    # Find the first non-zero digit and its index
    first_val, first_idx = find_first_non_zero(input_list)

    # Handle the case where the input is all zeros
    if first_val is None:
        return input_str # Return unchanged if all zeros

    # Find the last non-zero digit and its index
    last_val, last_idx = find_last_non_zero(input_list)

    # Calculate the number of leading zeros
    num_left_zeros = first_idx

    # Calculate the number of trailing zeros
    num_right_zeros = (n - 1) - last_idx

    # Create a copy of the input list to modify
    output_list = list(input_list)

    # Compare the number of leading and trailing zeros
    if num_left_zeros <= num_right_zeros:
        # Fill leading zeros with the first non-zero value
        for i in range(first_idx):
            output_list[i] = first_val
    else:
        # Fill trailing zeros with the last non-zero value
        for i in range(last_idx + 1, n):
            output_list[i] = last_val

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))

    return output_str
```