import math
import numpy as np
import re # Not strictly required, but kept from previous attempts

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
    Converts various input types (string, list, ndarray) into a flat list of integers.
    Handles space-separated digit strings and flattens NumPy arrays.
    """
    int_list = []
    if isinstance(input_data, str):
        # Handle string input: split by space and convert to int
        parts = input_data.split()
        if not parts:
            return []
        try:
            int_list = [int(part) for part in parts]
        except ValueError:
            # Handle potential non-integer parts if necessary, based on stricter requirements
            # For now, assume valid integer strings as per examples
             raise ValueError("Input string contains non-integer parts.")
    elif isinstance(input_data, np.ndarray):
        # Handle NumPy array input: flatten first, then convert to list of ints
        try:
            # Flatten ensures 1D, tolist converts to Python list
            # map(int, ...) ensures elements are integers
            int_list = list(map(int, input_data.flatten().tolist()))
        except (ValueError, TypeError) as e:
            raise TypeError(f"NumPy array contains non-convertible elements: {e}")
    elif isinstance(input_data, list):
        # Handle list input: ensure all elements are integers
        try:
            int_list = [int(item) for item in input_data]
        except (ValueError, TypeError) as e:
             raise TypeError(f"Input list contains non-integer elements: {e}")
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
    Handles string, list, and NumPy array inputs. Outputs a space-separated string.
    """
    # 1. Robustly parse the input into a flat list of integers
    # This now correctly handles NumPy arrays by flattening them first.
    input_list = _parse_input_to_list(input_data)
    n = len(input_list)

    # Handle empty input list -> return empty string
    if n == 0:
        return ""

    # 2. Find the boundaries (indices) of the core block (non-zero part)
    first_nz_idx = _find_first_non_zero_index(input_list)

    # 3. Handle the case where all elements are zero (or list is empty - covered above)
    if first_nz_idx == -1:
        # If no non-zero elements, the list is unchanged. Format and return.
        return _format_list_to_string(input_list)

    # Find the last non-zero index (guaranteed to exist if first_nz_idx != -1)
    last_nz_idx = _find_last_non_zero_index(input_list)

    # 4. Extract the three components using slice notation:
    # - Leading zeros: elements from start up to the first non-zero
    leading_zeros = input_list[:first_nz_idx]
    # - Core block: elements from first non-zero up to and including last non-zero
    core_block = input_list[first_nz_idx : last_nz_idx + 1]
    # - Trailing zeros: elements from after the last non-zero to the end
    trailing_zeros = input_list[last_nz_idx + 1:]

    # 5. Reverse the core block
    # Using list slicing [::-1] creates a reversed copy
    reversed_core_block = core_block[::-1]

    # 6. Concatenate the components to form the final output list
    output_list = leading_zeros + reversed_core_block + trailing_zeros

    # 7. Format the output list into a space-separated string
    output_str = _format_list_to_string(output_list)

    # Return the final transformed string
    return output_str