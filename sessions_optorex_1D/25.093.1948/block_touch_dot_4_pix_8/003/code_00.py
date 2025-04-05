import numpy as np # Although not explicitly used in the final logic, good practice to import common libs if needed.

"""
Rearrange a sequence of digits (provided as a list of integers) based on the relative positions of a 'value block' (contiguous identical digits other than 0 or 2) and the digit '2' (the pivot). 
If a value block exists and is separated from the '2' by one or more zeros ('intermediate zeros'):
- If the block is to the left of '2', move the block immediately to the left of '2' and move the intermediate zeros to the start of the sequence.
- If the block is to the right of '2', move the block immediately to the right of '2' and move the intermediate zeros to the end of the sequence.
- If the block is adjacent to '2' or no such value block exists, the sequence remains unchanged.
The output is the rearranged list of integers.
"""

def _find_pivot_index(grid, pivot_value=2):
    """Finds the index of the pivot value (2) in the grid."""
    try:
        # Convert potential numpy array to list for index method
        grid_list = list(grid) 
        return grid_list.index(pivot_value)
    except ValueError:
        return -1 # Pivot not found

def _find_first_value_block(grid, pivot_index):
    """
    Finds the first contiguous block of identical digits != 0 and != 2.
    Returns (start_index, end_index, value) or (None, None, None).
    end_index is exclusive.
    """
    n = len(grid)
    for i in range(n):
        # Skip 0s and the pivot value itself
        if grid[i] == 0 or grid[i] == 2:
            continue
        
        # Found a potential start of a block
        block_value = grid[i]
        j = i + 1
        # Find the end of the contiguous block
        while j < n and grid[j] == block_value:
            j += 1
            
        # Check if it's a valid block (length > 0)
        # No need to explicitly check j > i because the outer loop ensures grid[i] is a valid start
        return i, j, block_value # Found the first block
            
    return None, None, None # No value block found

def transform(input_grid):
    """
    Transforms the input list of digits based on the described rules.
    
    Args:
        input_grid: A list or numpy array of integers.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # 1. Ensure input is a standard Python list for easier manipulation
    grid = list(input_grid) 
    n = len(grid)

    # 2. Locate the index of the pivot digit 2.
    pivot_index = _find_pivot_index(grid, 2)
    if pivot_index == -1:
        # Pivot '2' must be present based on examples
        return grid # Return original if pivot not found (defensive)

    # 3. Search for the first value block B.
    block_start, block_end, block_value = _find_first_value_block(grid, pivot_index)

    # 4. If no such block B is found, return the original input list unchanged.
    if block_start is None:
        return grid

    # 5. & 6. Determine relative position (left/right)
    block_is_left = False
    if block_end <= pivot_index: # Block ends before or at the pivot index
        block_is_left = True
    elif block_start > pivot_index: # Block starts after the pivot index
        block_is_left = False
    # Note: block containing pivot is implicitly handled by _find_first_value_block skipping pivot value

    # 7. Identify the intermediate sequence Z (only zeros) between B and 2.
    intermediate_zeros = []
    if block_is_left:
        # Z is between block_end and pivot_index
        for i in range(block_end, pivot_index):
            if grid[i] == 0:
                intermediate_zeros.append(0)
            # else: Non-zero found between block and pivot - deviates from pattern
                # This case isn't expected based on examples. If it occurs,
                # current logic might misbehave. Treat as adjacent for now.
                # return grid 
    else: # block is right
        # Z is between pivot_index + 1 and block_start
        for i in range(pivot_index + 1, block_start):
             if grid[i] == 0:
                intermediate_zeros.append(0)
             # else: Non-zero found - treat as adjacent for now.
                # return grid

    # 8. If Z is empty (B and 2 are adjacent), return original list unchanged.
    if not intermediate_zeros:
        # Check adjacency explicitly based on indices
        if block_is_left and block_end == pivot_index:
            return grid
        if not block_is_left and block_start == pivot_index + 1:
            return grid
        # If intermediate_zeros is empty but they weren't adjacent (e.g., non-zero between)
        # the current logic will proceed, potentially incorrectly if the pattern assumption is violated.
        # However, based *strictly* on examples, empty intermediate_zeros means adjacency.

    # --- Perform Rearrangement ---

    # 9. Create a new list `temp_list` by removing B and Z.
    temp_list = []
    indices_to_remove = set(range(block_start, block_end)) # Block indices
    if block_is_left:
        indices_to_remove.update(range(block_end, pivot_index)) # Zero indices
    else: # block is right
        indices_to_remove.update(range(pivot_index + 1, block_start)) # Zero indices

    for i in range(n):
        if i not in indices_to_remove:
            temp_list.append(grid[i])
            
    # 10. Find the index `new_pivot_index` of 2 within the reduced `temp_list`.
    # We know the pivot '2' was never in indices_to_remove.
    new_pivot_index = _find_pivot_index(temp_list, 2) 
    
    # 11. Create list `value_block_elements`.
    value_block_elements = [block_value] * (block_end - block_start)

    # 12. `intermediate_zeros` list already created in step 7.

    # 13. If block B was originally to the left of 2:
    if block_is_left:
        # a. Prepend intermediate zeros.
        # b. Insert block elements before the pivot.
        # Need to find pivot index *after* prepending zeros
        final_grid = intermediate_zeros + temp_list
        final_pivot_index = _find_pivot_index(final_grid, 2)
        final_grid = final_grid[:final_pivot_index] + value_block_elements + final_grid[final_pivot_index:]
        
    # 14. If block B was originally to the right of 2:
    else: # block_is_right
        # a. Insert block elements immediately after the pivot in temp_list.
        # b. Append intermediate zeros.
        # Use new_pivot_index found in temp_list *before* appending zeros.
        final_grid = temp_list[:new_pivot_index+1] + value_block_elements + temp_list[new_pivot_index+1:]
        final_grid = final_grid + intermediate_zeros

    # 15. Return the final constructed list.
    return final_grid