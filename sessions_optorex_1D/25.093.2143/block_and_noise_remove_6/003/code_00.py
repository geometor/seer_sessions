import math
from typing import List

"""
Identifies all contiguous blocks of non-zero numbers in the input list.
Determines the maximum length among these blocks.
Selects the first block (by starting index) that achieves this maximum length.
Constructs the output list by placing the selected block's numbers at their
original positions and filling all other positions with zero. If no non-zero
numbers exist, the output is all zeros.
"""

def find_blocks(input_list: List[int]) -> List[dict]:
    """
    Finds all contiguous blocks of non-zero numbers.

    Args:
        input_list: The input list of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        and contains 'start', 'end', and 'length'. Returns an empty list
        if no non-zero numbers are found.
    """
    blocks = []
    current_start = -1
    n = len(input_list)

    for i in range(n):
        is_non_zero = input_list[i] != 0
        is_last_element = (i == n - 1)

        # Start of a potential block: current element is non-zero, and we are not already in a block
        if is_non_zero and current_start == -1:
            current_start = i

        # End of a block: (current element is zero OR it's the last element) AND we were in a block
        if (not is_non_zero or is_last_element) and current_start != -1:
            # Determine the correct end index
            current_end = i - 1 if not is_non_zero else i
            # Calculate block length
            block_length = current_end - current_start + 1
            # Store block info
            blocks.append({
                'start': current_start,
                'end': current_end,
                'length': block_length
            })
            # Reset for the next potential block
            current_start = -1
            
    return blocks


def transform(input_grid: List[int]) -> List[int]:
    """
    Transforms the input list by keeping only the first longest contiguous
    block of non-zero numbers and replacing everything else with zero.
    """
    # Get the length of the input list
    n = len(input_grid)
    
    # Initialize the output grid with zeros, matching the input length
    output_grid = [0] * n

    # Find all contiguous blocks of non-zero numbers in the input
    blocks = find_blocks(input_grid)

    # If no non-zero blocks were found, return the grid of zeros
    if not blocks:
        return output_grid

    # Find the maximum length among all identified blocks
    max_len = 0
    for block in blocks:
        if block['length'] > max_len:
            max_len = block['length']
    
    # Find the first block (earliest start index) that has the maximum length
    target_block = None
    for block in blocks:
        if block['length'] == max_len:
            target_block = block
            break # Stop searching once the first longest block is found

    # If a target block was successfully identified (should always happen if blocks is not empty)
    if target_block:
        # Get the start and end indices of the target block
        start = target_block['start']
        end = target_block['end']
        # Copy the elements from the input grid corresponding to the target block
        # into the output grid at the same positions
        for i in range(start, end + 1):
            # Check index bounds just in case, though logic should prevent out-of-bounds
            if 0 <= i < n:
                output_grid[i] = input_grid[i]

    # Return the final transformed grid
    return output_grid