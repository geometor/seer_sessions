import math
from typing import List, Tuple, Sequence 

"""
Rearranges a sequence of 12 integers, provided as a space-separated string, 
by splitting the sequence into two blocks (first 4 integers and remaining 8 integers) 
and swapping their positions in the output string.
"""

def parse_string_to_list(input_str: str, delimiter: str = ' ') -> List[str]:
    """Splits a string by a delimiter and returns a list of non-empty strings."""
    return [item for item in input_str.split(delimiter) if item]

def format_list_to_string(input_list: List[str], delimiter: str = ' ') -> str:
    """Joins a list of strings into a single string using a delimiter."""
    return delimiter.join(input_list)

def transform(input_str: str) -> str:
    """
    Rearranges a space-separated string of 12 numbers.

    Args:
        input_str: A string containing 12 space-separated numbers.

    Returns:
        A string containing the rearranged 12 space-separated numbers.
    """

    # 1. Split the input string into a list of number strings.
    number_strings = parse_string_to_list(input_str)

    # Basic validation - ensure we have 12 elements after splitting
    if len(number_strings) != 12:
        # Handle error case appropriately, e.g., raise an exception or return an error indicator.
        # For now, let's raise a ValueError consistent with the previous attempt's logic.
        raise ValueError(f"Input string '{input_str}' does not contain exactly 12 space-separated numbers.")

    # 2. Divide the list of number strings into two parts:
    #    - part1: The first 4 number strings.
    part1 = number_strings[0:4]
    #    - part2: The remaining 8 number strings (from the 5th to the 12th).
    part2 = number_strings[4:12]

    # 3. Create a new list by concatenating part2 followed by part1.
    rearranged_list = part2 + part1

    # 4. Join the strings in the rearranged list back into a single, space-separated string.
    output_str = format_list_to_string(rearranged_list)

    # 5. Return the final output string.
    return output_str