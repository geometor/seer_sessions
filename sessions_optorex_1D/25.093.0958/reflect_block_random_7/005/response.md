```python
import math
import numpy as np
import re # Not strictly required by the final logic, but potentially useful for more complex parsing if needed

"""
Transforms an input sequence of digits (provided as a string, list, or NumPy array) 
by reversing the order of the subsequence located between the first and last 
non-zero digits. Any leading and trailing zeros in the original sequence are 
preserved in their respective positions in the output. If the sequence contains 
only zeros, it remains unchanged. The final output is formatted as a 
space-separated string.
"""

def _parse_input_to_list(input_data) -> list[int]:
    """
    Converts various input types (string, list, ndarray) into a list of integers.
    Handles space-separated digit strings.
    """
    if isinstance(input_data, str):
        # Assume space-separated digits based on task examples
        parts = input_data.split()
        if not parts:
            return []
        try:
            # Convert each part to an integer
            int_list = [int(part) for part in parts]
        except ValueError as e:
            # Handle cases where parts are not valid integers
            print(f"Warning: Input string contains non-integer parts: {e}")
            # Attempt to filter out non-digit parts, or raise error depending on desired strictness
            # For now, let's try filtering, assuming digits are the goal
            int_list = [int(part) for part in parts if part.isdigit() or (part.startswith('-') and part[1:].isdigit())]
            # If strict adherence to example format (only non-negative single digits) is required:
            # int_list = [int(part) for part in parts if part.isdigit() and len(part) == 1]
    elif isinstance(input_data, (list, np.ndarray)):
        # If it's a list or numpy array, convert elements to int
        try:
            int_list = [int(item) for item in input_data]
        except (ValueError, TypeError) as e:
             raise TypeError(f"Input list/array contains non-integer elements: {e}")
    else:
        raise TypeError(f"Unsupported input type: {type(input_data)}")
    return int_list

def _find_first_non_zero_index(int_list: list[int]) -> int:
    """Finds the index of the first non-zero element. Returns -1 if none found."""
    for i, val in enumerate(int_list):
        if val != 0:
            return i
    return -1

def _find_last_non_zero_index(int_list: list[int]) -> int:
    """Finds the index of the last non-zero element. Returns -1 if none found."""
    n = len(int_list)
    for i in range(n - 1, -1, -1):
        if int_list[i] != 0:
            return i
    return -1

def _format_list_to_string(int_list: list[int]) -> str:
    """Converts a list of integers to a space-separated string."""
    return ' '.join(map(str, int_list))

def transform(input_data) -> str:
    """
    Applies the core transformation logic: reverse the segment between the
    first and last non-zero elements, preserving leading/trailing zeros.
    """
    # 1. Robustly parse the input into a list of integers
    input_list = _parse_input_to_list(input_data)
    n = len(input_list)

    # Handle empty input list
    if n == 0:
        return ""

    # 2. Find the boundaries of the core (non-zero) block
    first_nz_idx = _find_first_non_zero_index(input_list)

    # 3. Handle the case where all elements are zero
    if first_nz_idx == -1:
        # If no non-zero elements, return the original list formatted as string
        return _format_list_to_string(input_list)

    # Find the last non-zero index (guaranteed to exist if first_nz_idx != -1)
    last_nz_idx = _find_last_non_zero_index(input_list)

    # 4. Extract the three components: leading zeros, core block, trailing zeros
    leading_zeros = input_list[:first_nz_idx]
    core_block = input_list[first_nz_idx : last_nz_idx + 1]
    trailing_zeros = input_list[last_nz_idx + 1:]

    # 5. Reverse the core block
    reversed_core_block = core_block[::-1] # Using slice notation for reversal

    # 6. Concatenate the components to form the output list
    output_list = leading_zeros + reversed_core_block + trailing_zeros

    # 7. Format the output list into a space-separated string
    output_str = _format_list_to_string(output_list)

    return output_str
```