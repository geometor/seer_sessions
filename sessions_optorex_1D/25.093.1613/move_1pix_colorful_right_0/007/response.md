```python
import math # Not strictly needed, but often useful
import numpy as np # Not used in this implementation, but common
import re # Not used in this implementation, but common

"""
Transforms an input sequence of space-separated digits by inserting a '0' 
before the first non-zero digit found in the sequence and removing the 
last digit to maintain the original sequence length. If the sequence 
contains only zeros, it is returned unchanged.
"""

def _find_first_non_zero_index(data_list):
    """
    Helper function to find the index of the first non-zero element in a list.

    Args:
        data_list: A list of numbers.

    Returns:
        The index of the first non-zero element, or -1 if all elements are zero.
    """
    for index, value in enumerate(data_list):
        if value != 0:
            return index
    return -1 # Indicate no non-zero element found

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string sequence.

    Args:
        input_str: A string containing space-separated single digits (0-9).

    Returns:
        A string representing the transformed sequence with digits separated by spaces.
    """
    # 1. Split the input string by spaces to create a list of digit strings.
    str_list = input_str.split()

    # 2. Convert the list of digit strings into a list of integers.
    # Handle potential errors if input format is unexpected, though examples suggest valid input.
    try:
        input_list = [int(digit) for digit in str_list]
    except ValueError:
        # Handle cases where conversion fails (e.g., non-digit characters)
        # For this problem based on examples, assume valid input.
        # If error handling is needed, could return input_str or raise exception.
        print(f"Warning: Input string '{input_str}' contained non-integer values.")
        return input_str # Or raise appropriate error

    # 3. Find the index of the first non-zero element.
    first_nz_idx = _find_first_non_zero_index(input_list)

    # 4. Check if a non-zero digit was found.
    if first_nz_idx == -1:
        # 4a. If no non-zero digit found (all zeros), return the original string.
        return input_str
    else:
        # 4b. If a non-zero digit was found:
        # i. Create a new list by copying the original integer list.
        output_list = list(input_list)

        # ii. Insert the integer 0 into this new list at the found index.
        output_list.insert(first_nz_idx, 0)

        # iii. Remove the last element from this new list to maintain length.
        output_list.pop() # Removes the last element

        # iv. Convert the elements of the modified list back into strings.
        output_str_list = [str(digit) for digit in output_list]

        # v. Join these strings with a single space delimiter.
        output_str = " ".join(output_str_list)

        # vi. Return the resulting output string.
        return output_str

```