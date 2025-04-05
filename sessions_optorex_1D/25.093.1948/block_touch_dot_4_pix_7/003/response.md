```python
import re
from typing import List, Tuple, Optional

"""
Identifies the location of the digit '2' and a contiguous block of identical digits (not '0' or '2') within an input sequence of 12 integers.
If there is a non-empty sequence composed entirely of '0's between the block and '2', swaps the block and the sequence of '0's, moving the block adjacent to '2'.
If the block is already adjacent to '2', or if the space between them contains non-zero digits (other than the block itself), or if the space is empty, no changes are made.
Returns the potentially modified sequence.
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
    Assumes only one such block exists per sequence based on examples.
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
                # Found a different non-zero/non-2 digit, meaning the previous block ended.
                # This case assumes only one block type exists based on examples.
                # If multiple *different* blocks existed, this logic would need adjustment.
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
    """Checks if a list contains only zeros and is not empty."""
    if not sub_list: # Empty list is not considered "all zeros" for the swap condition
        return False
    return all(digit == 0 for digit in sub_list)

def transform(input_list: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input list of integers.
    """
    # Initialize output_list as a copy of the input
    output_list = list(input_list)

    # 1. Identify the index of '2'
    two_index = find_digit_index(output_list, 2)
    if two_index is None:
        # Should not happen based on examples, return original if '2' is missing
        return output_list

    # 2. Identify the non-zero/non-2 digit block
    block_info = find_digit_block(output_list)
    if block_info is None:
         # Should not happen based on examples, return original if block is missing
        return output_list

    block_digit, block_start, block_end = block_info
    # block_len = block_end - block_start + 1 # Not strictly needed for reconstruction

    # 3. Determine relative position and check for intermediate zeros
    if block_end < two_index:
        # Case: Block is to the left of '2'
        # 4a. Examine the intermediate subsequence
        intermediate_slice = output_list[block_end + 1 : two_index]

        # 5a. Check if intermediate slice is non-empty and all zeros
        if is_all_zeros(intermediate_slice):
            # Perform swap: Move block next to '2', zeros to block's original start
            zeros_slice = intermediate_slice
            block_slice = output_list[block_start : block_end + 1]

            # Reconstruct the list
            new_list = (output_list[:block_start] +
                        zeros_slice +
                        block_slice +
                        output_list[two_index:])
            output_list = new_list # Update the list to be returned

    elif block_start > two_index:
        # Case: Block is to the right of '2'
        # 4b. Examine the intermediate subsequence
        intermediate_slice = output_list[two_index + 1 : block_start]

        # 5b. Check if intermediate slice is non-empty and all zeros
        if is_all_zeros(intermediate_slice):
            # Perform swap: Move block next to '2', zeros after block's original end
            zeros_slice = intermediate_slice
            block_slice = output_list[block_start : block_end + 1]

            # Reconstruct the list
            new_list = (output_list[:two_index + 1] +
                        block_slice +
                        zeros_slice +
                        output_list[block_end + 1:])
            output_list = new_list # Update the list to be returned

    # 6. Else (block is adjacent to '2', separated by non-zeros, or intermediate space is empty):
    # No changes were made to output_list in these cases.

    # 7. Return the resulting sequence
    return output_list
```