"""
Transforms a sequence of 12 space-separated digits represented as a single string by moving the first three digits to the end of the sequence, maintaining the relative order within both the moved part and the remaining part.
"""

import math
import numpy as np
# No complex imports needed for this specific string manipulation task

def transform(input_str: str) -> str:
    """
    Applies a cyclic left shift of 3 positions to a sequence of 12 digits
    represented as a space-separated string.

    Args:
        input_str: A string containing 12 space-separated digits.
                   (Note: Although the template parameter is named input_grid,
                    based on observations and previous errors, this function
                    expects and processes a single string.)

    Returns:
        A string containing the transformed sequence with digits separated by spaces.
    """

    # 1. Split the input string by spaces to get a list of digit strings.
    # Example: "0 0 0 7 3 6 4 8 2 0 0 0" -> ['0', '0', '0', '7', '3', '6', '4', '8', '2', '0', '0', '0']
    digits = input_str.split(' ')

    # --- Perform the cyclic shift using list slicing ---

    # 2. Extract the first three elements (the prefix block).
    prefix_block = digits[:3]
    # Example: ['0', '0', '0']

    # 3. Extract the remaining nine elements (the suffix block).
    suffix_block = digits[3:]
    # Example: ['7', '3', '6', '4', '8', '2', '0', '0', '0']

    # 4. Create the new list by concatenating the suffix block followed by the prefix block.
    output_digits = suffix_block + prefix_block
    # Example: ['7', '3', '6', '4', '8', '2', '0', '0', '0'] + ['0', '0', '0']
    #       -> ['7', '3', '6', '4', '8', '2', '0', '0', '0', '0', '0', '0']

    # 5. Join the elements of the new list back into a single string separated by spaces.
    output_str = ' '.join(output_digits)
    # Example: "7 3 6 4 8 2 0 0 0 0 0 0"

    # 6. Return the resulting output string.
    return output_str
