import math
import numpy as np
import collections

"""
Transforms a sequence of integers based on the position of the first non-zero element.

The transformation follows two main rules:
1. If the first non-zero element is not at the beginning (index > 0), it is swapped 
   with the element immediately preceding it (which is expected to be zero based on examples).
2. If the first non-zero element is at the beginning (index 0):
   a. Find the end index of the initial contiguous block of this non-zero number.
   b. Find the start index of the *next* block of any non-zero number occurring 
      after the end of the first block.
   c. If such a next block exists and the element immediately preceding it (at index 
      next_start_index - 1) is zero, swap the element at the end of the first block 
      with this zero.
3. If the sequence contains only zeros, it remains unchanged.
"""

# Helper function to find the index of the first non-zero element
def find_first_nonzero_index(grid):
    """Finds the index of the first non-zero element in the list."""
    for i, val in enumerate(grid):
        if val != 0:
            return i
    return -1 # Indicate not found

# Helper function to find the end index of a contiguous block of the same value
def find_block_end(grid, start_index):
    """Finds the end index (inclusive) of a contiguous block of the same value 
       starting at start_index."""
    val = grid[start_index]
    end_index = start_index
    # Iterate from the next element onwards
    for i in range(start_index + 1, len(grid)):
        if grid[i] == val:
            end_index = i  # Update the end index if the value matches
        else:
            break # Stop when a different value or the end of the grid is encountered
    return end_index

# Helper function to find the start index of the next non-zero block
def find_next_block_start(grid, search_start_index):
    """Finds the start index of the next non-zero block (any non-zero value) 
       occurring after the search_start_index."""
    # Iterate from the element after the search_start_index
    for i in range(search_start_index + 1, len(grid)):
        if grid[i] != 0:
            # Found the start of the next non-zero block
            return i
    return -1 # Indicate not found

def transform(input_grid):
    """
    Applies the transformation rule to the input grid (list of integers).
    """
    # Ensure input is a list and create a mutable copy
    output_grid = list(input_grid)
    n = len(output_grid)

    # Find the index of the first non-zero element
    first_nz_idx = find_first_nonzero_index(output_grid)

    # Handle case: no non-zero elements found (or empty grid)
    if first_nz_idx == -1:
        return output_grid # Return unchanged grid

    # Case 1: First non-zero element is NOT at the beginning (index > 0)
    if first_nz_idx > 0:
        # Swap the first non-zero element with its preceding element
        swap_idx1 = first_nz_idx
        swap_idx2 = first_nz_idx - 1
        output_grid[swap_idx1], output_grid[swap_idx2] = output_grid[swap_idx2], output_grid[swap_idx1]

    # Case 2: First non-zero element IS at the beginning (index 0)
    elif first_nz_idx == 0:
        # Find the end index of the first block (starting at index 0)
        end_idx = find_block_end(output_grid, 0)

        # Find the start index of the next non-zero block occurring after end_idx
        next_block_start_idx = find_next_block_start(output_grid, end_idx)

        # Check if a next block was found
        if next_block_start_idx != -1:
            # Calculate the index immediately before the next block
            zero_idx = next_block_start_idx - 1
            
            # Check if this preceding index is valid and contains a zero
            if zero_idx >= 0 and output_grid[zero_idx] == 0:
                 # Swap the element at the end of the first block with the zero preceding the next block
                 swap_idx1 = end_idx
                 swap_idx2 = zero_idx
                 output_grid[swap_idx1], output_grid[swap_idx2] = output_grid[swap_idx2], output_grid[swap_idx1]
        # If no next block is found, or the element before it isn't zero, no swap occurs in this case.

    # Return the modified sequence
    return output_grid