"""
Transforms an input sequence of digits (provided potentially as a 1D NumPy array
containing a single space-separated string, or as a 1D NumPy array of integers)
by inserting a '0' at the index of the first non-zero digit found in the
sequence. The resulting sequence is then truncated to maintain the original length
of the input sequence. Finally, the transformed sequence of digits is returned as
a space-separated string.
"""

import numpy as np
import math # math and numpy are available, though math isn't used here.

def find_first_non_zero_index(digit_list):
    """
    Finds the index of the first non-zero digit in a list of integers.
    Returns 0 if all digits are zero or the list is empty.

    Args:
        digit_list: A list of integers.

    Returns:
        The 0-based index of the first non-zero digit, or 0 if none is found.
    """
    for i, digit in enumerate(digit_list):
        if digit != 0:
            return i
    # If no non-zero digit is found, or list is empty, default to index 0
    return 0

def transform(input_grid: np.ndarray) -> str:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A NumPy array, potentially containing a single string
                    element with space-separated digits, or a 1D array of ints.

    Returns:
        A string containing the transformed sequence of digits, separated by spaces.
    """

    # --- Input Parsing ---
    # Check the structure of the input_grid
    if input_grid.size == 0:
        return "" # Handle empty input

    input_str = ""
    # Hypothesis: Input might be np.array(["0 9 1 ..."])
    if input_grid.ndim == 1 and input_grid.size == 1 and isinstance(input_grid[0], str):
         input_str = input_grid[0]
         input_digits_str = input_str.split()
    # Hypothesis: Input might be np.array([0, 9, 1, ...])
    elif input_grid.ndim == 1 and np.issubdtype(input_grid.dtype, np.integer):
         input_digits_str = [str(d) for d in input_grid]
    # Fallback/Error Handling for unexpected formats
    else:
         # Attempt to convert first element if it's string-like,
         # otherwise treat as error or empty case
         try:
            input_str = str(input_grid.flat[0])
            input_digits_str = input_str.split()
         except:
              return "" # Cannot parse input reliably

    # --- Core Logic ---
    # 1. Record original length
    original_length = len(input_digits_str)
    if original_length == 0:
        return ""

    # 2. Convert to list of integers
    try:
        digit_list = [int(d) for d in input_digits_str]
    except ValueError:
        # Handle cases where split elements are not valid integers
        return "" # Or raise an error, depending on desired behavior

    # 3. Find the index of the first non-zero digit.
    insertion_index = find_first_non_zero_index(digit_list)

    # 4. Create a copy and insert 0 at the insertion_index.
    modified_list = digit_list[:] # Create a copy using slicing
    modified_list.insert(insertion_index, 0)

    # 5. Take the first N elements (truncate) from the modified list.
    final_digit_list = modified_list[:original_length]

    # --- Output Formatting ---
    # 6. Convert the final list of integers back into a space-separated string.
    output_str = " ".join(map(str, final_digit_list))

    # 7. Return the result
    return output_str