```python
import numpy as np # Import numpy, common for grid manipulation
from typing import List, Tuple, Optional # For type hinting

"""
The transformation rule identifies a single, stationary pivot digit '2' within a sequence (list or array) of 12 digits. 
It then locates the first contiguous block of non-zero digits (excluding the pivot '2').
If this block is located entirely to the left of the pivot '2', and there is a '0' immediately to the right of the block, the block is shifted one position to the right, swapping places with that '0'.
If the block is located entirely to the right of the pivot '2', and there is a '0' immediately to the left of the block, the block is shifted one position to the left, swapping places with that '0'.
The pivot '2' and any other '0's remain in their positions unless directly involved in the swap.
The function takes a list or NumPy array as input and returns a NumPy array representing the modified sequence.
"""

def find_pivot_index(grid: List[int]) -> Optional[int]:
    """Finds the index of the pivot digit '2'."""
    try:
        # Convert to list if it's a numpy array for index() method
        return list(grid).index(2) 
    except ValueError:
        return None # Pivot '2' not found

def find_movable_block(grid: List[int], pivot_index: Optional[int]) -> Optional[Tuple[int, int]]:
    """
    Finds the start and end indices of the first contiguous block of 
    non-zero digits (excluding the pivot '2').
    Returns (start_index, end_index) or None if no such block is found.
    """
    start_index = -1
    for i, digit in enumerate(grid):
        # Start block if digit is non-zero and not the pivot
        if digit != 0 and i != pivot_index:
            start_index = i
            # Find the end of this block
            end_index = i
            for j in range(i + 1, len(grid)):
                # Block ends if we hit a zero or the pivot
                if grid[j] == 0 or j == pivot_index:
                    break 
                end_index = j
            # Return the first block found
            return start_index, end_index 
            
    return None # No block found

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the block shifting transformation based on the pivot '2'.

    Args:
        input_grid: A numpy array of 12 integers.

    Returns:
        A numpy array representing the transformed grid.
    """
    # Work on a copy to avoid modifying the original input array
    output_grid = np.copy(input_grid)
    grid_list = list(output_grid) # Use list for easier index/slice manipulation
    n = len(grid_list)

    # 1. Find the pivot ('2') index
    pivot_index = find_pivot_index(grid_list)
    if pivot_index is None:
        # If no pivot '2' is found, return the original grid
        return output_grid 

    # 2. Find the block to potentially move
    block_indices = find_movable_block(grid_list, pivot_index)

    # 3. If a block is found, determine position and attempt shift/swap
    if block_indices:
        start_index, end_index = block_indices
        block_content = grid_list[start_index : end_index + 1]
        
        # 3a. Check if block is to the LEFT of the pivot
        if end_index < pivot_index:
            # Check if a swap to the RIGHT is possible (adjacent '0')
            swap_pos = end_index + 1
            if swap_pos < n and grid_list[swap_pos] == 0:
                # Perform right shift: place 0 at start, block content at start+1
                grid_list[start_index] = 0
                grid_list[start_index + 1 : end_index + 2] = block_content
                
        # 3b. Check if block is to the RIGHT of the pivot
        elif start_index > pivot_index:
            # Check if a swap to the LEFT is possible (adjacent '0')
            swap_pos = start_index - 1
            if swap_pos >= 0 and grid_list[swap_pos] == 0:
                 # Perform left shift: place 0 at end, block content at start-1
                 grid_list[end_index] = 0
                 grid_list[start_index - 1 : end_index] = block_content

    # 4. Convert the potentially modified list back to a numpy array
    output_grid = np.array(grid_list)

    return output_grid
```