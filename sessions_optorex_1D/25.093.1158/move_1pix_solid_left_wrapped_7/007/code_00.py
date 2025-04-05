import math
import numpy as np
import collections

"""
Transforms a sequence of integers based on the position and grouping of non-zero elements.

The transformation follows two main rules determined by the index of the first non-zero element:

1.  **Rule 1 (First non-zero element's index `i` > 0):**
    a.  Identify the contiguous block of the same non-zero value starting at index `i`. Let this block end at index `j`.
    b.  If the element at index `i-1` is 0, shift this entire block (from `i` to `j`) one position to the left, occupying indices `i-1` to `j-1`.
    c.  The original element at index `i-1` (the 0) is moved to index `j`.

2.  **Rule 2 (First non-zero element's index `i` == 0):**
    a.  Identify the contiguous block of the starting non-zero value, ending at index `j`.
    b.  Find the start index `k` of the *next* block of *any* non-zero number occurring after index `j`.
    c.  If such a next block exists (k != -1) and the element immediately preceding it (at index `k-1`) is 0, swap the element at index `j` (the end of the first block) with the element at index `k-1` (the zero before the next block).

3.  If the sequence contains only zeros or is empty, it remains unchanged.
"""

# === Helper Functions ===

def parse_input(input_data):
    """Parses the input string into a list of integers."""
    if isinstance(input_data, str):
        return [int(digit) for digit in input_data.split()]
    elif isinstance(input_data, (list, tuple, np.ndarray)): # Handle list/tuple/array inputs
        return [int(x) for x in input_data]
    else:
        raise TypeError("Input must be a string, list, tuple, or numpy array of digits/numbers.")


def find_first_nonzero_index(grid):
    """Finds the index of the first non-zero element in the list."""
    for i, val in enumerate(grid):
        if val != 0:
            return i
    return -1 # Indicate not found

def find_block_end(grid, start_index):
    """
    Finds the end index (inclusive) of a contiguous block of the *same* value
    that starts at start_index. Returns start_index if it's a zero or out of bounds.
    """
    if start_index < 0 or start_index >= len(grid):
        return start_index # Or -1 maybe, but start_index seems safer if called later

    val = grid[start_index]
    if val == 0: # Cannot have a block of zeros based on logic calling this
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
    Applies the transformation rule to the input grid.
    Input can be a string of space-separated digits or a list/tuple/array of numbers.
    Returns a list of integers.
    """
    # Parse the input into a list of integers
    parsed_grid = parse_input(input_grid)

    # Create a mutable copy
    output_grid = list(parsed_grid)
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

        # Check if the element before the block exists and is 0
        if block_start_idx > 0 and output_grid[block_start_idx - 1] == 0:
             # Store the zero that will be moved
            zero_to_move = output_grid[block_start_idx - 1]

            # Perform the left shift of the block
            # Move elements from block_start_idx to block_end_idx one step left
            for i in range(block_start_idx, block_end_idx + 1):
                output_grid[i - 1] = output_grid[i]

            # Place the stored zero at the original end position of the block
            output_grid[block_end_idx] = zero_to_move
        # Else (element before isn't 0 or index 0), no change based on examples.

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

            # Check if this preceding index is valid (implicitly true if next_block_start found)
            # and importantly, check if it contains a zero
            # Also ensure there's actually a gap (zero_idx is after first_block_end)
            if zero_idx_before_next >= 0 and zero_idx_before_next > first_block_end_idx and output_grid[zero_idx_before_next] == 0:
                 # Perform the swap: element at the end of the first block swaps
                 # with the zero preceding the next block.
                 swap_idx1 = first_block_end_idx
                 swap_idx2 = zero_idx_before_next
                 output_grid[swap_idx1], output_grid[swap_idx2] = output_grid[swap_idx2], output_grid[swap_idx1]
        # If no next block is found, or the element before it isn't zero, or no gap, no swap occurs in this case.

    # Return the modified sequence
    return output_grid