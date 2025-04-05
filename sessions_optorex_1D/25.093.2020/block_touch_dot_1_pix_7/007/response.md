```python
import numpy as np
import copy

"""
Transforms an input sequence (1D NumPy array of 12 integers) based on the 
position of the integer '2'. Contiguous blocks of non-zero integers 
(excluding '2') are identified. Blocks located before '2' and not immediately 
adjacent to it are shifted one position to the right in a copy of the sequence. 
Blocks located after '2' and not immediately adjacent to it are shifted one 
position to the left. The position vacated by a shift (the original start for a 
right shift, the original end for a left shift) is filled with '0'. The integer 
'2' itself and any blocks immediately adjacent to it remain unchanged.
"""

def _find_integer_2(grid):
    """
    Finds the index of the first occurrence of the integer 2 in the grid.

    Args:
        grid: A 1D NumPy array of integers.

    Returns:
        The index of the integer 2, or -1 if not found.
    """
    # Use np.where to find indices where the value is 2
    indices = np.where(grid == 2)[0]
    # Return the first index if found, otherwise -1
    if len(indices) > 0:
        return indices[0]
    else:
        return -1

def _find_blocks(grid, index_of_2):
    """
    Finds contiguous blocks of non-zero integers (excluding the integer 2)
    in the grid. Uses standard Python iteration.

    Args:
        grid: A 1D NumPy array of integers.
        index_of_2: The index of the integer 2 in the grid, or -1 if not present.

    Returns:
        A list of tuples, where each tuple represents a block and contains
        its (start_index, end_index).
    """
    blocks = []
    n = len(grid)
    i = 0
    while i < n:
        # Check if the current element is the start of a potential block
        # It must be non-zero and not be the marker '2' (if '2' exists)
        is_start_of_block = (grid[i] != 0) and (i != index_of_2)
        
        if is_start_of_block:
            start_index = i
            # Extend the block: move 'i' forward as long as elements 
            # are non-zero, not '2', and within bounds.
            # Check i+1 < n *before* accessing grid[i+1]
            while (i + 1 < n) and (grid[i + 1] != 0) and ((i + 1) != index_of_2):
                i += 1
            # The block ends at the current index 'i'
            end_index = i
            blocks.append((start_index, end_index))
        # Move to the next potential start position
        i += 1
    return blocks

def transform(input_grid):
    # Ensure input is a NumPy array for consistency
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid, dtype=int) 

    # Create a modifiable copy of the input sequence to store the output
    output_grid = np.copy(input_grid)
    n = len(input_grid) # Length of the sequence

    # Find the index (position) of the integer '2' in the original input sequence
    index_of_2 = _find_integer_2(input_grid)

    # If '2' is not found, the transformation rules don't apply; return the original grid copy
    if index_of_2 == -1:
        return output_grid 

    # Identify all contiguous blocks of non-zero integers (not '2') in the *original input* sequence
    # This ensures shifts of one block don't affect the identification/position of others
    blocks = _find_blocks(input_grid, index_of_2)

    # Iterate through each identified block (defined by start and end index)
    for start_index, end_index in blocks:
        
        # Check if the block is immediately adjacent to '2'
        # Adjacent if it ends right before '2' OR starts right after '2'
        is_adjacent_before = (end_index == index_of_2 - 1)
        is_adjacent_after = (start_index == index_of_2 + 1)

        # If the block is adjacent, make no changes for this block; continue to the next block
        if is_adjacent_before or is_adjacent_after:
            continue
        else:
            # Block is not adjacent. Determine its relative location.
            # Check if the block is located entirely before '2'
            block_is_before_2 = (end_index < index_of_2)
            # Check if the block is located entirely after '2'
            block_is_after_2 = (start_index > index_of_2)

            if block_is_before_2:
                # Shift right: check if the shifted block fits within the grid bounds
                if end_index + 1 < n:
                    # Extract block content from the *original* input grid
                    block_content = input_grid[start_index : end_index + 1]
                    # Place block content in the new shifted position in the *output_grid*
                    output_grid[start_index + 1 : end_index + 2] = block_content
                    # Set the original starting position (vacated space) to 0 in the *output_grid*
                    output_grid[start_index] = 0
            elif block_is_after_2:
                # Shift left: check if the shifted block fits within the grid bounds
                if start_index - 1 >= 0:
                    # Extract block content from the *original* input grid
                    block_content = input_grid[start_index : end_index + 1]
                    # Place block content in the new shifted position in the *output_grid*
                    output_grid[start_index - 1 : end_index] = block_content
                    # Set the original ending position (vacated space) to 0 in the *output_grid*
                    output_grid[end_index] = 0

    # Return the final modified output sequence
    return output_grid
```