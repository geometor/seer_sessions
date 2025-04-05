import math
import numpy as np
import collections

"""
Transforms a sequence of integers based on the position and grouping of non-zero elements.

The transformation follows two main rules determined by the index of the first non-zero element:

1.  **Rule 1 (First non-zero element's index `i` > 0):**
    a.  Identify the contiguous block of the same non-zero value starting at index `i`. Let this block end at index `j`.
    b.  Shift this entire block (from `i` to `j`) one position to the left, occupying indices `i-1` to `j-1`.
    c.  The original element at index `i-1` (which is expected to be 0) is moved to index `j`.

2.  **Rule 2 (First non-zero element's index `i` == 0):**
    a.  Identify the contiguous block of the starting non-zero value, ending at index `j`.
    b.  Find the start index `k` of the *next* block of *any* non-zero number occurring after index `j`.
    c.  If such a next block exists (k != -1) and the element immediately preceding it (at index `k-1`) is 0, swap the element at index `j` (the end of the first block) with the element at index `k-1` (the zero before the next block).

3.  If the sequence contains only zeros or is empty, it remains unchanged.
"""

# === Helper Functions ===

def find_first_nonzero_index(grid):
    """Finds the index of the first non-zero element in the list."""
    for i, val in enumerate(grid):
        if val != 0:
            return i
    return -1 # Indicate not found

def find_block_end(grid, start_index):
    """
    Finds the end index (inclusive) of a contiguous block of the *same* value
    that starts at start_index.
    """
    if start_index < 0 or start_index >= len(grid):
        return -1 # Invalid start index
    
    val = grid[start_index]
    if val == 0: # Cannot have a block of zeros by definition here
        return start_index 
        
    end_index = start_index
    # Iterate from the next element onwards
    for i in range(start_index + 1, len(grid)):
        if grid[i] == val:
            end_index = i  # Update the end index if the value matches
        else:
            break # Stop when a different value or the end of the grid is encountered
    return end_index

def find_next_nonzero_block_start(grid, search_start_index):
    """
    Finds the start index of the next non-zero block (any non-zero value)
    occurring strictly after the search_start_index.
    """
    # Iterate from the element *after* the search_start_index
    for i in range(search_start_index + 1, len(grid)):
        if grid[i] != 0:
            # Found the start of the next non-zero block
            return i
    return -1 # Indicate not found

# === Main Transformation Function ===

def transform(input_grid):
    """
    Applies the transformation rule to the input grid (list of integers).
    """
    # Ensure input is a list and create a mutable copy
    if not isinstance(input_grid, list):
      # If input is numpy array or other sequence, convert to list
       output_grid = list(input_grid)
    else:
       output_grid = list(input_grid) # Make a copy

    n = len(output_grid)

    # Handle empty grid case
    if n == 0:
        return output_grid

    # Find the index of the first non-zero element
    first_nz_idx = find_first_nonzero_index(output_grid)

    # Handle case: no non-zero elements found
    if first_nz_idx == -1:
        return output_grid # Return unchanged grid

    # --- Apply Transformation Rules ---

    # Case 1: First non-zero element is NOT at the beginning (index > 0)
    if first_nz_idx > 0:
        # Find the end index of the block starting at first_nz_idx
        block_start_idx = first_nz_idx
        block_end_idx = find_block_end(output_grid, block_start_idx)

        # Ensure the element before the block is indeed 0 as expected
        if block_start_idx > 0 and output_grid[block_start_idx - 1] == 0:
             # Store the zero that will be moved
            zero_to_move = output_grid[block_start_idx - 1] 
            
            # Perform the left shift of the block
            for i in range(block_start_idx, block_end_idx + 1):
                output_grid[i - 1] = output_grid[i]
                
            # Place the stored zero at the end of the shifted block's original position
            output_grid[block_end_idx] = zero_to_move
        # If the preceding element isn't zero, the examples don't cover this,
        # so we assume no change based on observed patterns.

    # Case 2: First non-zero element IS at the beginning (index 0)
    elif first_nz_idx == 0:
        # Find the end index of the first block (starting at index 0)
        first_block_end_idx = find_block_end(output_grid, 0)

        # Find the start index of the next non-zero block occurring after the first block
        next_block_start_idx = find_next_nonzero_block_start(output_grid, first_block_end_idx)

        # Check if a next block was found
        if next_block_start_idx != -1:
            # Calculate the index immediately before the next block
            zero_idx_before_next = next_block_start_idx - 1

            # Check if this preceding index is valid (>=0, although implicitly true if next_block_start_idx > first_block_end_idx >= 0)
            # and importantly, check if it contains a zero
            if output_grid[zero_idx_before_next] == 0:
                 # Perform the swap: element at the end of the first block swaps
                 # with the zero preceding the next block.
                 swap_idx1 = first_block_end_idx
                 swap_idx2 = zero_idx_before_next
                 output_grid[swap_idx1], output_grid[swap_idx2] = output_grid[swap_idx2], output_grid[swap_idx1]
        # If no next block is found, or the element before it isn't zero, no swap occurs in this case.

    # Return the modified sequence
    return output_grid