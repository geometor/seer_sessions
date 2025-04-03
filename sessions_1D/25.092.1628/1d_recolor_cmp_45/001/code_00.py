import numpy as np
from typing import List, Tuple, Dict

"""
Identifies contiguous horizontal blocks of azure (8) pixels in the input row.
Determines the maximum length among these blocks.
Changes the color of all azure (8) pixels within the block(s) that have the maximum length to magenta (6).
If multiple blocks share the maximum length, all such blocks are transformed.
Pixels not part of a maximum-length azure block remain unchanged.
"""

def find_azure_blocks(row: List[int]) -> List[Dict[str, int]]:
    """
    Finds all contiguous blocks of azure (8) pixels in a row.

    Args:
        row: A list of integers representing the pixels in the row.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        and contains 'start', 'end', and 'length'. 'end' is inclusive.
        Returns an empty list if no azure blocks are found.
    """
    blocks = []
    in_block = False
    start_index = -1
    for i, pixel in enumerate(row):
        if pixel == 8 and not in_block:
            # Start of a new block
            in_block = True
            start_index = i
        elif pixel != 8 and in_block:
            # End of the current block
            in_block = False
            blocks.append({'start': start_index, 'end': i - 1, 'length': i - start_index})
            start_index = -1
        # Handle block ending at the very end of the row
        if in_block and i == len(row) - 1:
             blocks.append({'start': start_index, 'end': i, 'length': i - start_index + 1})

    return blocks

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on the rule: change the longest
    contiguous block(s) of azure (8) pixels to magenta (6).

    Args:
        input_grid: A list of lists representing the input grid (expected to be 1xN).

    Returns:
        A list of lists representing the transformed grid.
    """
    # Since the examples show 1D grids (single row), extract the first row.
    # It's assumed input will always conform to this structure based on examples.
    if not input_grid or not input_grid[0]:
        return [] # Handle empty input

    input_row = input_grid[0]
    # Initialize output_grid as a copy of the input row to modify
    output_row = list(input_row)

    # 1. Scan the input row to identify all contiguous blocks of azure (8) pixels.
    azure_blocks = find_azure_blocks(input_row)

    # If no azure blocks are found, return the original grid
    if not azure_blocks:
        # Wrap the row back into the list-of-lists format
        return [output_row]

    # 2. Find the maximum length among all identified azure blocks.
    max_length = 0
    for block in azure_blocks:
        if block['length'] > max_length:
            max_length = block['length']

    # 3. Iterate through the blocks. For blocks matching max length, transform pixels.
    for block in azure_blocks:
        if block['length'] == max_length:
            # Change pixels from start to end (inclusive) to magenta (6)
            for i in range(block['start'], block['end'] + 1):
                if output_row[i] == 8: # Ensure we only change azure pixels
                    output_row[i] = 6

    # Wrap the modified row back into the list-of-lists format
    output_grid = [output_row]
    return output_grid
