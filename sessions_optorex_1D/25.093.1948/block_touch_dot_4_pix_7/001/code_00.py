import re
from typing import List, Tuple, Optional

"""
Identifies the location of the digit '2' and a contiguous block of identical digits (not '0' or '2').
If there is a sequence composed entirely of '0's between the block and '2', swaps the block and the sequence of '0's, moving the block adjacent to '2'.
If the block is already adjacent to '2', or if the space between them contains non-zero digits (other than the block itself), no changes are made.
"""

def find_digit_index(data: List[int], digit: int) -> Optional[int]:
    """Finds the index of the first occurrence of a digit."""
    try:
        return data.index(digit)
    except ValueError:
        return None

def find_digit_block(data: List[int]) -> Optional[Tuple[int, int, int]]:
    """
    Finds the contiguous block of identical digits that are not 0 or 2.
    Returns (digit_value, start_index, end_index) or None if not found.
    """
    block_digit = -1
    start_index = -1
    end_index = -1
    in_block = False

    for i, digit in enumerate(data):
        if digit != 0 and digit != 2:
            if not in_block:
                # Start of a potential block
                block_digit = digit
                start_index = i
                in_block = True
            elif digit == block_digit:
                # Continue the current block
                pass
            else:
                # Found a different non-zero/non-2 digit, meaning the previous block ended
                end_index = i - 1
                return block_digit, start_index, end_index
        elif in_block:
            # End of the block detected (found 0 or 2)
            end_index = i - 1
            return block_digit, start_index, end_index

    # Handle case where block goes to the end of the list
    if in_block:
        end_index = len(data) - 1
        return block_digit, start_index, end_index

    return None # No block found

def is_all_zeros(sub_list: List[int]) -> bool:
    """Checks if a list contains only zeros."""
    if not sub_list: # Empty list doesn't count as all zeros for swapping purpose
        return False
    return all(digit == 0 for digit in sub_list)

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string sequence.

    1. Parses the input string into a list of integers.
    2. Finds the index of '2'.
    3. Finds the contiguous block of identical non-zero, non-'2' digits.
    4. Checks if intermediate zeros exist between the block and '2'.
    5. If yes, swaps the block and the zeros.
    6. Returns the transformed sequence as a string.
    """
    # Parse input string into a list of integers
    input_list = [int(x) for x in input_str.split()]
    output_list = list(input_list) # Start with a copy

    # Find the index of '2'
    two_index = find_digit_index(output_list, 2)
    if two_index is None:
        # Should not happen based on examples, but handle defensively
        return input_str # Return original if '2' is missing

    # Find the digit block
    block_info = find_digit_block(output_list)
    if block_info is None:
         # Should not happen based on examples, but handle defensively
        return input_str # Return original if block is missing

    block_digit, block_start, block_end = block_info
    block_len = block_end - block_start + 1

    # Determine relative position and check for intermediate zeros
    if block_end < two_index:
        # Case: Block is to the left of '2'
        intermediate_slice = output_list[block_end + 1 : two_index]
        
        # Check if the intermediate slice consists only of zeros and is not empty
        if is_all_zeros(intermediate_slice):
            # Perform swap: Move block next to '2', zeros to block's original start
            zeros_slice = intermediate_slice
            block_slice = output_list[block_start : block_end + 1]
            
            # Reconstruct the list
            new_list = (output_list[:block_start] + 
                        zeros_slice + 
                        block_slice + 
                        output_list[two_index:])
            output_list = new_list
            
    elif block_start > two_index:
        # Case: Block is to the right of '2'
        intermediate_slice = output_list[two_index + 1 : block_start]

        # Check if the intermediate slice consists only of zeros and is not empty
        if is_all_zeros(intermediate_slice):
            # Perform swap: Move block next to '2', zeros after block's original end
            zeros_slice = intermediate_slice
            block_slice = output_list[block_start : block_end + 1]

            # Reconstruct the list
            new_list = (output_list[:two_index + 1] +
                        block_slice +
                        zeros_slice +
                        output_list[block_end + 1:])
            output_list = new_list

    # Else (block is adjacent to '2' or separated by non-zeros): No change needed

    # Format output list back into a string
    return " ".join(map(str, output_list))
