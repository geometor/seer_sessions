import numpy as np
from typing import List

"""
Iterate through the input row (represented as a 1D list).
Identify contiguous blocks of non-white pixels.
If a block has length 1, replace it with a block of the same color but length 3 in the output.
If a block has length 3, keep it unchanged in the output.
Preserve white pixels (value 0) in their relative positions.
The output row is constructed based on these transformations.
"""

def transform(input_grid: List[int]) -> List[int]:
    """
    Transforms the input 1D grid based on the lengths of contiguous non-white blocks.
    Blocks of length 1 are expanded to length 3. Blocks of length 3 remain the same.
    White pixels are preserved.

    Args:
        input_grid: A list of integers representing the input 1D grid.

    Returns:
        A list of integers representing the transformed 1D grid.
    """
    output_grid = []
    i = 0
    n = len(input_grid)

    while i < n:
        # Check if the current pixel is white (background)
        if input_grid[i] == 0:
            output_grid.append(0)
            i += 1
        else:
            # Identify a non-white block
            block_color = input_grid[i]
            block_start = i
            # Find the end of the contiguous block of the same color
            while i < n and input_grid[i] == block_color:
                i += 1
            block_end = i
            block_length = block_end - block_start

            # Apply transformation based on block length
            if block_length == 1:
                # Expand block of length 1 to length 3
                output_grid.extend([block_color] * 3)
            elif block_length == 3:
                # Keep block of length 3 as is
                output_grid.extend([block_color] * 3)
            else:
                # Handle unexpected block lengths if necessary,
                # though the examples only show 1 and 3.
                # For now, just copy the original block.
                # This part might need adjustment based on further examples or rules.
                output_grid.extend(input_grid[block_start:block_end])

            # The loop counter 'i' is already advanced past the block

    return output_grid
