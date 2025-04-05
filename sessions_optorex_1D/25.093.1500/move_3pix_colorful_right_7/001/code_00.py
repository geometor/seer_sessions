"""
Transforms an input sequence of 12 digits by shifting the first 9 digits 
3 positions to the right and prepending three '0' digits. The last 3 digits
of the original input are discarded.
"""

import numpy as np

# Constants derived from observations
SEQUENCE_LENGTH = 12
SHIFT_AMOUNT = 3
PADDING_VALUE = 0

def parse_input(input_str: str) -> list[int]:
    """Parses the space-separated string into a list of integers."""
    return [int(x) for x in input_str.strip().split()]

def format_output(output_list: list[int]) -> str:
    """Formats the list of integers into a space-separated string."""
    return " ".join(map(str, output_list))

def transform(input_str: str) -> str:
    """
    Applies the right-shift transformation to the input sequence string.

    1.  Parse the input string into a list of digits.
    2.  Take the first (SEQUENCE_LENGTH - SHIFT_AMOUNT) digits from the input list.
    3.  Create a padding list consisting of SHIFT_AMOUNT zeros.
    4.  Concatenate the padding list and the truncated input list to form the output list.
    5.  Format the output list back into a space-separated string.
    """
    # 1. Parse the input string into a list of integers.
    input_list = parse_input(input_str)
    
    # Validate input length (optional but good practice)
    if len(input_list) != SEQUENCE_LENGTH:
        raise ValueError(f"Input sequence must have length {SEQUENCE_LENGTH}")

    # 2. Take the first (SEQUENCE_LENGTH - SHIFT_AMOUNT) digits from the input list.
    # Calculate the number of elements to keep from the original input
    elements_to_keep_count = SEQUENCE_LENGTH - SHIFT_AMOUNT
    kept_elements = input_list[:elements_to_keep_count]

    # 3. Create a padding list consisting of SHIFT_AMOUNT zeros.
    padding_list = [PADDING_VALUE] * SHIFT_AMOUNT

    # 4. Concatenate the padding list and the truncated input list.
    output_list = padding_list + kept_elements

    # 5. Format the output list back into a space-separated string.
    output_str = format_output(output_list)

    return output_str
