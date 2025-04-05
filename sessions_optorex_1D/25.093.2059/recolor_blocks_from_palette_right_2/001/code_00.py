import re
from typing import List, Tuple

"""
Transforms a sequence of integers based on the first two numbers and blocks of '5's.

1.  Parses the input string into a list of integers.
2.  Identifies the first number (`key1`) and second number (`key2`) from the list.
3.  Finds all contiguous blocks (sequences) of the number 5 in the input list.
4.  Initializes the output list as a copy of the input list.
5.  If at least one block of 5s is found, replaces the elements in the output list corresponding to the *first* block with `key1`.
6.  If at least two blocks of 5s are found, replaces the elements in the output list corresponding to the *second* block with `key2`.
7.  Converts the modified output list back into a space-separated string.
"""

def find_contiguous_blocks(sequence: List[int], target_value: int) -> List[Tuple[int, int]]:
    """
    Finds contiguous blocks of a target value in a sequence.

    Args:
        sequence: The list of integers to search within.
        target_value: The integer value to find blocks of.

    Returns:
        A list of tuples, where each tuple contains (start_index, length)
        of a contiguous block.
    """
    blocks = []
    n = len(sequence)
    i = 0
    while i < n:
        if sequence[i] == target_value:
            start_index = i
            length = 0
            # Continue while the value matches the target and we're within bounds
            while i < n and sequence[i] == target_value:
                length += 1
                i += 1
            blocks.append((start_index, length))
        else:
            # Move to the next element if no block starts here
            i += 1
    return blocks

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string sequence.

    Args:
        input_str: A string containing space-separated integers.

    Returns:
        A string containing the transformed space-separated integers.
    """
    # Parse input string into a list of integers
    input_list = [int(x) for x in input_str.split()]

    # Initialize output_list as a copy of input_list
    # This handles all elements that are not part of the target blocks
    output_list = list(input_list)

    # Identify key1 and key2
    # Based on examples, assume input always has at least 2 elements
    if len(input_list) < 2:
        # Handle potentially short inputs if necessary, though examples are longer.
        # This basic handling prevents index errors but might need refinement
        # depending on strict task requirements for edge cases.
        key1 = input_list[0] if len(input_list) > 0 else 0 # Default or error
        key2 = 0 # Default or error
    else:
        key1 = input_list[0]
        key2 = input_list[1]

    # Define the target digit
    target_digit = 5

    # Find all contiguous blocks of the target_digit (5)
    target_blocks = find_contiguous_blocks(input_list, target_digit)

    # Replace the first block with key1, if it exists
    if len(target_blocks) >= 1:
        start_index, length = target_blocks[0]
        # Iterate through the indices of the first block in the output list
        for i in range(start_index, start_index + length):
            # Check bounds just in case, though lengths should match
            if i < len(output_list):
                output_list[i] = key1

    # Replace the second block with key2, if it exists
    if len(target_blocks) >= 2:
        start_index, length = target_blocks[1]
        # Iterate through the indices of the second block in the output list
        for i in range(start_index, start_index + length):
            # Check bounds
            if i < len(output_list):
                output_list[i] = key2

    # Format the output list back into a space-separated string
    output_str = " ".join(map(str, output_list))

    return output_str
