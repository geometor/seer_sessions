import numpy as np
from typing import List, Tuple, Dict

"""
Transforms a 1D NumPy array of integers based on the lengths of contiguous blocks of '3's.

Rule:
1. Input is a 1D NumPy array containing 0s and 3s.
2. Output is a 1D NumPy array of the same length containing 0s, 1s, and 2s.
3. '0's in the input remain '0's in the output.
4. Contiguous blocks of '3's (separated by '0's or array boundaries) are identified.
5. It's assumed there are exactly two such blocks of '3's in the input array.
6. The block with the greater number of '3's is transformed into a block of '1's.
7. The block with the fewer number of '3's is transformed into a block of '2's.
"""

def find_blocks_of_3(arr: np.ndarray) -> List[Dict[str, int]]:
    """
    Identifies contiguous blocks of the number 3 in a 1D NumPy array.

    Args:
        arr: The input 1D NumPy array.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        and contains 'start' (index), 'end' (index, exclusive), and 'length'.
        Returns an empty list if no blocks of 3 are found.
    """
    blocks = []
    n = len(arr)
    i = 0
    while i < n:
        if arr[i] == 3:
            # Found the start of a potential block
            start_index = i
            # Find the end of the block
            while i < n and arr[i] == 3:
                i += 1
            end_index = i
            length = end_index - start_index
            blocks.append({'start': start_index, 'end': end_index, 'length': length})
            # Continue searching from the end of this block
        else:
            # Not a 3, move to the next element
            i += 1
    return blocks

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the block transformation rule based on length comparison.

    Args:
        input_grid: A 1D NumPy array containing 0s and 3s.

    Returns:
        A 1D NumPy array with blocks of 3s transformed to 1s (longer block)
        and 2s (shorter block).
    """
    # Ensure input is 1D
    if input_grid.ndim != 1:
        # Handle potential multi-dimensional arrays if necessary,
        # but based on examples, assume 1D.
        # For now, let's flatten if it's not 1D, though this might
        # not be the correct interpretation for ARC tasks in general.
        # If the task guarantees 1D, this check can be simpler.
        if input_grid.size == 0:
             return input_grid # Handle empty input
        input_grid = input_grid.flatten() # Or raise error if dim > 1 expected


    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Find all contiguous blocks of '3's
    blocks = find_blocks_of_3(input_grid)

    # Check if exactly two blocks were found (as per observations)
    if len(blocks) == 2:
        # Compare the lengths of the two blocks
        block1 = blocks[0]
        block2 = blocks[1]

        # Assign target values based on length
        if block1['length'] > block2['length']:
            target_block1 = 1
            target_block2 = 2
        elif block2['length'] > block1['length']:
            target_block1 = 2
            target_block2 = 1
        else:
            # Handle the case of equal length blocks if necessary.
            # Based on examples, lengths seem different.
            # Let's assume the first encountered block gets 1 if lengths are equal.
            target_block1 = 1
            target_block2 = 2

        # Apply transformations to the output grid
        output_grid[block1['start']:block1['end']] = target_block1
        output_grid[block2['start']:block2['end']] = target_block2

    # If not exactly two blocks, the rule might be different or incomplete.
    # For now, based on examples, we only handle the two-block case.
    # If zero or one block exists, the output grid remains as the initial copy
    # (0s remain 0s, any single block of 3s remains unchanged by this logic).
    # If more than two blocks exist, this logic doesn't cover it.

    return output_grid