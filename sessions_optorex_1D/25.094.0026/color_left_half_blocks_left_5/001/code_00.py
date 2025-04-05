import re
from typing import List, Tuple

"""
Identifies contiguous blocks of the digit '2' in a space-separated string sequence of digits. 
For each block found:
- If the block length is 2 or 3, the last '2' in the block is changed to '8'.
- If the block length is 4 or more, the last two '2's in the block are changed to '8'.
Digits '0' remain unchanged.
"""

def find_two_blocks(sequence: List[int]) -> List[Tuple[int, int]]:
    """
    Finds the start and end indices of contiguous blocks of '2's.

    Args:
        sequence: A list of integers (0s and 2s).

    Returns:
        A list of tuples, where each tuple is (start_index, end_index)
        for a block of '2's.
    """
    blocks = []
    in_block = False
    start_index = -1
    for i, digit in enumerate(sequence):
        if digit == 2 and not in_block:
            # Start of a new block
            in_block = True
            start_index = i
        elif digit != 2 and in_block:
            # End of the current block
            in_block = False
            blocks.append((start_index, i - 1))
    # Check if the sequence ends with a block
    if in_block:
        blocks.append((start_index, len(sequence) - 1))
    return blocks

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input sequence string.

    Args:
        input_str: A space-separated string of digits (0s and 2s).

    Returns:
        A space-separated string with '2's transformed to '8's based on block rules.
    """
    # 1. Parse the input sequence string into a list of integers.
    input_list = [int(digit) for digit in input_str.split()]

    # 2. Create a mutable copy to serve as the working output sequence.
    output_list = list(input_list)

    # 3. Scan the sequence to identify all contiguous blocks of '2's.
    two_blocks = find_two_blocks(input_list)

    # 4. Iterate through the identified blocks and apply transformation rules.
    for start_index, end_index in two_blocks:
        block_length = end_index - start_index + 1

        if block_length == 2 or block_length == 3:
            # a. If block length is 2 or 3, change the digit at the end index to '8'.
            if end_index < len(output_list): # Basic boundary check
                 output_list[end_index] = 8
        elif block_length >= 4:
            # b. If block length is 4 or more, change the last two digits to '8'.
            if end_index < len(output_list): # Basic boundary checks
                output_list[end_index] = 8
            if end_index - 1 >= 0 and end_index -1 < len(output_list):
                 output_list[end_index - 1] = 8

    # 5. Return the final working output sequence as a space-separated string.
    return " ".join(map(str, output_list))
