```python
import numpy as np # Although not strictly required by final list logic, often used in ARC context
from typing import List, Tuple, Optional 

"""
The transformation rule identifies a single, stationary pivot digit '2' within a sequence (list) of 12 digits. 
It then locates the first contiguous block of non-zero digits (excluding the pivot '2').
If this block is located entirely to the left of the pivot '2', the block is shifted one position to the right by swapping places with the adjacent '0' immediately to its right.
If the block is located entirely to the right of the pivot '2', the block is shifted one position to the left by swapping places with the adjacent '0' immediately to its left.
The pivot '2' and any other '0's remain in their positions unless directly involved in the swap.
The function takes a list of integers as input and returns a list representing the modified sequence.
"""

def find_pivot_index(grid: List[int]) -> Optional[int]:
    """Finds the index of the pivot digit '2'."""
    try:
        return grid.index(2)
    except ValueError:
        return None # Pivot '2' not found

def find_movable_block(grid: List[int], pivot_index: Optional[int]) -> Optional[Tuple[int, int]]:
    """
    Finds the start and end indices of the first contiguous block of 
    non-zero digits (excluding the pivot '2').
    Returns (start_index, end_index) or None if no such block is found.
    """
    start_index = -1 
    if pivot_index is None: # Cannot find block relative to non-existent pivot
      return None
      
    for i, digit in enumerate(grid):
        # Start block if digit is non-zero and not the pivot, and we haven't started one
        if start_index == -1 and digit != 0 and i != pivot_index:
            start_index = i
            end_index = i # Initialize end index
        # If we have started a block, continue checking
        elif start_index != -1:
             # If it's a valid block digit, extend the end
             if digit != 0 and i != pivot_index:
                 end_index = i
             # If we hit a 0 or the pivot, the block just ended
             else:
                 return start_index, end_index 
                 
    # If the loop finished and we found a start, return the indices
    if start_index != -1:
        return start_index, end_index
        
    return None # No block found

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the block shifting transformation based on the pivot '2'.

    Args:
        input_grid: A list of 12 integers.

    Returns:
        A list representing the transformed grid.
    """
    # 1. Receive the input sequence and create a mutable copy
    output_grid = list(input_grid) 
    n = len(output_grid)

    # 2. Locate the index of the pivot digit '2'.
    pivot_index = find_pivot_index(output_grid)
    
    # Handle case where pivot is missing (shouldn't happen based on examples)
    if pivot_index is None:
        return output_grid # Return original if no pivot

    # 3. Find the movable block (start and end indices)
    block_indices = find_movable_block(output_grid, pivot_index)

    # 4. If a block was found, perform the shift/swap
    if block_indices:
        start_index, end_index = block_indices
        # 5. Extract the block content
        block_content = output_grid[start_index : end_index + 1]
        
        # 6. Determine position relative to pivot and perform shift/swap
        
        # 6a. Case 1: Block is Left of Pivot
        if end_index < pivot_index:
            # Check if the space to the right is '0' (should be based on analysis)
            swap_pos = end_index + 1
            if swap_pos < n and output_grid[swap_pos] == 0:
                # Perform right shift: place 0 at start, block content at start+1
                output_grid[start_index] = 0
                # Assign the block content to the shifted position
                output_grid[start_index + 1 : end_index + 2] = block_content
                
        # 6b. Case 2: Block is Right of Pivot
        elif start_index > pivot_index:
            # Check if the space to the left is '0' (should be based on analysis)
            swap_pos = start_index - 1
            if swap_pos >= 0 and output_grid[swap_pos] == 0:
                 # Perform left shift: place 0 at end, block content at start-1
                 output_grid[end_index] = 0
                 # Assign the block content to the shifted position
                 output_grid[start_index - 1 : end_index] = block_content

    # 7. Return the modified list copy
    return output_grid
```