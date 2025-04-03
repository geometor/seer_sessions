```python
import numpy as np
from typing import List, Tuple, Dict

"""
Transforms a 1D sequence of pixels by identifying contiguous blocks of azure (8) pixels.
Among those blocks that are immediately surrounded by white (0) pixels on both sides,
it finds the block(s) with the maximum length. 
The color of the pixels within these maximum-length, surrounded azure blocks is changed to orange (7).
All other pixels retain their original color.
"""

def find_azure_blocks(grid: List[int]) -> List[Dict[str, int]]:
    """
    Identifies contiguous blocks of azure (8) pixels in a 1D grid.

    Args:
        grid: A list of integers representing the 1D grid.

    Returns:
        A list of dictionaries, where each dictionary represents an azure block
        and contains 'start', 'end', and 'length' keys.
    """
    blocks = []
    n = len(grid)
    i = 0
    while i < n:
        if grid[i] == 8:
            start = i
            while i < n and grid[i] == 8:
                i += 1
            end = i - 1
            length = end - start + 1
            blocks.append({'start': start, 'end': end, 'length': length})
        else:
            i += 1
    return blocks

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the described transformation rule to the input grid.

    Args:
        input_grid: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the transformed 1D output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = list(input_grid)
    n = len(input_grid)

    # 1. Scan the input sequence to identify all contiguous horizontal blocks of azure (8)
    azure_blocks = find_azure_blocks(input_grid)

    # 2. Create a list of "candidate" blocks: Filter azure blocks surrounded by white (0)
    candidate_blocks = []
    for block in azure_blocks:
        start = block['start']
        end = block['end']
        
        # Check left boundary (must be white 0)
        is_left_surrounded = (start > 0 and input_grid[start - 1] == 0)
        
        # Check right boundary (must be white 0)
        is_right_surrounded = (end < n - 1 and input_grid[end + 1] == 0)

        if is_left_surrounded and is_right_surrounded:
            candidate_blocks.append(block)

    # 3. If the list of candidate blocks is empty, return the initial copy
    if not candidate_blocks:
        return output_grid

    # 4. Determine the maximum length among the candidate blocks
    max_length = 0
    for block in candidate_blocks:
        if block['length'] > max_length:
            max_length = block['length']

    # 5. Iterate through candidate blocks and change color for those with max length
    for block in candidate_blocks:
        if block['length'] == max_length:
            start = block['start']
            end = block['end']
            # Change the color of pixels within this block's range to orange (7)
            for i in range(start, end + 1):
                output_grid[i] = 7

    # 6. Return the modified output sequence
    return output_grid

```