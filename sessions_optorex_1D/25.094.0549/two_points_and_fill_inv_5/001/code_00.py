import re
from typing import List

"""
Transforms a sequence of space-separated single-digit integers.
It identifies contiguous blocks (runs) of identical non-zero digits.
If a run of a non-zero digit has a length of 3 or more, the first and last digits
of the run are kept, and all digits in between are replaced with '0'.
Runs of non-zero digits with length 1 or 2, and all runs of '0's, remain unchanged.
The overall length of the sequence is preserved.
"""

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string sequence.

    Args:
        input_str: A string containing space-separated single-digit integers.

    Returns:
        A string containing the transformed space-separated sequence.
    """
    # Parse the input string into a list of digit strings
    digits = input_str.split(' ')
    n = len(digits)
    output_digits = []
    i = 0

    # Iterate through the digits to find blocks
    while i < n:
        current_digit = digits[i]
        # Find the end of the current block of identical digits
        j = i + 1
        while j < n and digits[j] == current_digit:
            j += 1

        # Calculate the length of the block
        block_length = j - i
        block = digits[i:j]

        # Apply transformation logic based on the digit and block length
        if current_digit == '0':
            # Keep blocks of '0's as they are
            output_digits.extend(block)
        else:
            # Handle non-zero blocks
            if block_length < 3:
                # Keep short blocks (length 1 or 2) as they are
                output_digits.extend(block)
            else:
                # Modify blocks of length 3 or more
                # Keep the first digit
                output_digits.append(current_digit)
                # Add '0's in the middle
                output_digits.extend(['0'] * (block_length - 2))
                # Keep the last digit
                output_digits.append(current_digit)

        # Move the index to the start of the next block
        i = j

    # Join the processed digits back into a space-separated string
    return ' '.join(output_digits)
