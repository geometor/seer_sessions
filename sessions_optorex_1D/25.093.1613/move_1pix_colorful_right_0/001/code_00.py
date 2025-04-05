import math
import numpy as np
import re

"""
Transforms an input sequence of space-separated digits based on the following logic:
1. Convert the input string into a list of integers.
2. Check if the sequence contains any non-zero digits.
   - If all digits are zero, return the original input string.
   - Otherwise, proceed to the next step.
3. Find the index of the first non-zero digit in the list.
4. Insert the integer 0 into the list at this found index.
5. Remove the last element from the modified list to maintain the original length.
6. Convert the final list back into a space-separated string.
7. Return the resulting string.
"""

def _find_first_non_zero_index(data_list):
    """Helper function to find the index of the first non-zero element."""
    for index, value in enumerate(data_list):
        if value != 0:
            return index
    return -1 # Indicate no non-zero element found

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string sequence.
    """
    # 1. Convert the input string into a list of integers.
    # Handle potential empty strings or non-integer inputs gracefully if needed,
    # but based on examples, assume valid input format.
    input_list = [int(digit) for digit in input_str.split()]

    # 2. Check if the sequence contains only zeros.
    if all(digit == 0 for digit in input_list):
        # If all digits are zero, return the original input string.
        return input_str

    # 3. Find the index of the first non-zero digit.
    first_nz_idx = _find_first_non_zero_index(input_list)

    # Check if a non-zero index was actually found (handles edge case, though covered by step 2)
    if first_nz_idx != -1:
        # 4. Insert the integer 0 into the list at the found index.
        # Create a copy to avoid modifying the original list if it's needed elsewhere,
        # although in this standalone function, modifying in place is also fine.
        output_list = list(input_list) # Make a copy
        output_list.insert(first_nz_idx, 0)

        # 5. Remove the last element from the modified list.
        output_list.pop() # Removes the last element
    else:
        # This case should technically not be reached if step 2 works correctly
        # for inputs with non-zero numbers, but included for robustness.
        output_list = list(input_list)


    # 6. Convert the final list back into a space-separated string.
    output_str = " ".join(map(str, output_list))

    # 7. Return the resulting string.
    return output_str
