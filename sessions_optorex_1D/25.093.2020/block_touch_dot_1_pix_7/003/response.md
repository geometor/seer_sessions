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
    indices = np.where(grid == 2)[0]
    if len(indices) > 0:
        return indices[0]
    else:
        return -1

def _find_blocks(grid, index_of_2):
    """
    Finds contiguous blocks of non-zero integers (excluding the integer 2)
    in the grid.

    Args:
        grid: A 1D NumPy array of integers.
        index_of_2: The index of the integer 2 in the grid.

    Returns:
        A list of tuples, where each tuple represents a block and contains
        its (start_index, end_index).
    """
    blocks = []
    n = len(grid)
    i = 0
    while i < n:
        # Start of a potential block: non-zero and not the '2' itself
        if grid[i] != 0 and i != index_of_2:
            start_index = i
            # Extend the block as long as elements are non-zero and not '2'
            while i + 1 < n and grid[i + 1] != 0 and (i + 1) != index_of_2:
                i += 1
            end_index = i
            blocks.append((start_index, end_index))
        i += 1
    return blocks

def transform(input_grid):
    # Ensure input is a NumPy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid) # Convert if necessary

    # Create a modifiable copy of the input sequence
    output_grid = np.copy(input_grid)
    n = len(input_grid)

    # Find the index (position) of the integer '2'
    index_of_2 = _find_integer_2(input_grid)

    # If '2' is not found, return the original grid unmodified
    if index_of_2 == -1:
        return output_grid 

    # Identify all contiguous blocks of non-zero integers (not '2') in the *input* sequence
    blocks = _find_blocks(input_grid, index_of_2)

    # Iterate through each identified block and apply shifts if necessary
    for start_index, end_index in blocks:
        # Check if the block is immediately adjacent to '2'
        is_adjacent_before = (end_index == index_of_2 - 1)
        is_adjacent_after = (start_index == index_of_2 + 1)

        # If the block is adjacent, make no changes for this block
        if is_adjacent_before or is_adjacent_after:
            continue
        else:
            # Determine if the block is located entirely before '2'
            block_is_before_2 = (end_index < index_of_2)
            # Determine if the block is located entirely after '2'
            block_is_after_2 = (start_index > index_of_2)

            if block_is_before_2:
                # Check if shifting right is possible (within array bounds)
                if end_index + 1 < n:
                    # Extract block content from the *original* grid
                    block_content = input_grid[start_index : end_index + 1]
                    # Place block content in the new position in *output_grid*
                    output_grid[start_index + 1 : end_index + 2] = block_content
                    # Set the original starting position to 0 in *output_grid*
                    output_grid[start_index] = 0
            elif block_is_after_2:
                # Check if shifting left is possible (within array bounds)
                if start_index - 1 >= 0:
                    # Extract block content from the *original* grid
                    block_content = input_grid[start_index : end_index + 1]
                    # Place block content in the new position in *output_grid*
                    output_grid[start_index - 1 : end_index] = block_content
                    # Set the original ending position to 0 in *output_grid*
                    output_grid[end_index] = 0

    # Return the modified output sequence
    return output_grid
```