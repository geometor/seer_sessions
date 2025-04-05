import math
from typing import List

"""
Identifies all contiguous blocks of non-zero numbers in the input list.
Determines the maximum length among these blocks.
Selects the first block (by starting index) that achieves this maximum length.
Constructs the output list by placing the selected block's numbers at their original positions and filling all other positions with zero. If no non-zero numbers exist, the output is all zeros.
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
        # Start of a potential block
        if input_list[i] != 0 and current_start == -1:
            current_start = i
        # End of a block (hit a zero or end of list)
        if (input_list[i] == 0 or i == n - 1) and current_start != -1:
            # Adjust end index if the last element was non-zero
            current_end = i - 1 if input_list[i] == 0 else i
            block_length = current_end - current_start + 1
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
    n = len(input_grid)
    # Initialize output grid with zeros
    output_grid = [0] * n

    # Find all contiguous blocks of non-zero numbers
    blocks = find_blocks(input_grid)

    # If no blocks were found, return the grid of zeros
    if not blocks:
        return output_grid

    # Find the maximum length among the blocks
    max_len = 0
    for block in blocks:
        if block['length'] > max_len:
            max_len = block['length']

    # Find the first block that has the maximum length
    target_block = None
    for block in blocks:
        if block['length'] == max_len:
            target_block = block
            break # Found the first one, stop searching

    # If a target block was identified, copy its elements to the output grid
    if target_block:
        start = target_block['start']
        end = target_block['end']
        for i in range(start, end + 1):
            output_grid[i] = input_grid[i]

    return output_grid
