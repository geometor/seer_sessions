"""
Identify the single row of the input grid.
Find all contiguous blocks (runs) of non-background (non-zero) pixels within this row.
Determine the size (length) of each block.
Identify the block with the maximum size. If there's a tie, the block occurring first (leftmost start index) is implicitly chosen by the search method.
Create an output grid of the same dimensions as the input, initialized entirely with the background color (zero).
Copy the pixels corresponding to the identified largest block from the input row to the same positions in the first row of the output grid.
If no non-background blocks exist in the input row, the output remains entirely background color.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional

def find_contiguous_blocks_1d(row: np.ndarray, background_color: int = 0) -> List[Dict]:
    """
    Finds all contiguous blocks of non-background colors in a 1D numpy array (row).

    Args:
        row: A 1D numpy array representing a grid row.
        background_color: The integer value representing the background color.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        and contains 'color', 'start' index, 'end' index, and 'size'. Returns
        an empty list if no non-background blocks are found.
    """
    blocks = []
    current_block = None
    n = len(row)

    for i, pixel in enumerate(row):
        if pixel != background_color:
            # Non-background pixel found
            if current_block is None:
                # Start a new block
                current_block = {'color': pixel, 'start': i, 'size': 1}
            elif pixel == current_block['color']:
                # Continue the current block (same color)
                current_block['size'] += 1
            else:
                # Different non-background color, finalize previous block and start new one
                current_block['end'] = i - 1
                blocks.append(current_block)
                current_block = {'color': pixel, 'start': i, 'size': 1}
        else:
            # Background pixel found
            if current_block is not None:
                # Finalize the current block
                current_block['end'] = i - 1
                blocks.append(current_block)
                current_block = None # Reset, we are no longer in a block

    # Handle case where the row ends with a block
    if current_block is not None:
        current_block['end'] = n - 1
        blocks.append(current_block)

    return blocks

def find_largest_block(blocks: List[Dict]) -> Optional[Dict]:
    """
    Finds the block with the maximum size from a list of blocks.
    If sizes are equal, returns the first block encountered with that max size.

    Args:
        blocks: A list of block dictionaries.

    Returns:
        The dictionary representing the largest block, or None if the list is empty.
    """
    if not blocks:
        return None

    largest_block = None
    max_size = -1 # Initialize with a value smaller than any possible block size (>= 1)

    for block in blocks:
        if block['size'] > max_size:
            max_size = block['size']
            largest_block = block
            
    return largest_block

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by keeping only the largest contiguous block
    of non-background color found in its single row.

    Args:
        input_grid: A list of lists of integers representing the 2D input grid (expected to be 1xN).

    Returns:
        A list of lists of integers representing the transformed 2D output grid.
    """
    # Convert input to numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)
    
    # Get dimensions
    rows, cols = input_np.shape
    
    # Initialize output grid with background color (0)
    output_np = np.zeros_like(input_np)
    background_color = 0

    # Check if the input grid has at least one row
    if rows == 0 or cols == 0:
        return output_np.tolist() # Return empty grid if input is empty

    # Extract the first (and only expected) row
    first_row = input_np[0, :]

    # Find all contiguous blocks in the first row
    blocks = find_contiguous_blocks_1d(first_row, background_color)

    # Find the largest block among them
    largest_block = find_largest_block(blocks)

    # If a largest block was found, copy it to the output grid
    if largest_block:
        start_index = largest_block['start']
        end_index = largest_block['end']
        color = largest_block['color']
        
        # Ensure indices are valid (should be by construction)
        if 0 <= start_index <= end_index < cols:
             # Place the block in the first row of the output grid
             output_np[0, start_index : end_index + 1] = color

    # Convert the output numpy array back to a list of lists
    return output_np.tolist()