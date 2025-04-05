import math
import numpy as np # Import numpy as the environment might pass arrays

"""
Transforms an input list (or NumPy array) of 12 integers by identifying the first 
contiguous block of identical non-zero digits. This block is then shifted to the 
left by a number of positions equal to its own length. The resulting list is 
filled with zeros except for the shifted block.
"""

def find_non_zero_block(input_list: list[int]) -> tuple[int, int, int]:
    """
    Finds the first contiguous block of identical non-zero numbers in a list.

    Args:
        input_list: The list of integers to search within.

    Returns:
        A tuple containing:
        - start_index (int): The starting index of the block (-1 if no block found).
        - block_length (int): The length of the block (0 if no block found).
        - block_value (int): The value of the elements in the block (0 if no block found).
    """
    start_index = -1
    block_length = 0
    block_value = 0

    # Iterate through the list to find the block
    for i, val in enumerate(input_list):
        # Look for the start of a potential block (first non-zero)
        if val != 0 and start_index == -1:
            start_index = i
            block_value = val
            block_length = 1
        # If we are already in a block, check if the current element continues it
        elif start_index != -1:
            if val == block_value:
                block_length += 1
            # If the element is different (zero or another non-zero), the block ends
            else:
                break # Found the end of the block, stop searching

    # Return details, handling the case where no block was found
    if start_index != -1:
        return start_index, block_length, block_value
    else:
        return -1, 0, 0

def transform(input_grid) -> list[int]:
    """
    Applies the block-shifting transformation to the input grid.

    Args:
        input_grid: A list or NumPy array of integers representing the input state.

    Returns:
        A new list of integers with the non-zero block shifted according to the rule.
    """
    # Step 1: Ensure input is a standard Python list for consistent processing.
    if isinstance(input_grid, np.ndarray):
        # Convert NumPy array to list if necessary
        input_list = input_grid.tolist()
    else:
        # Assume it's already list-like (e.g., a list), ensure it's a mutable list
        input_list = list(input_grid) 

    list_length = len(input_list) # Should always be 12 based on examples
    
    # Step 2: Initialize output_grid: Create a new list filled with zeros.
    output_grid = [0] * list_length

    # Step 3: Identify Block & Record Properties: Find the non-zero block details using the helper function.
    start_index, block_length, block_value = find_non_zero_block(input_list)

    # Step 4: Check if a block was found. If not, the all-zero grid is returned.
    if start_index != -1:
        # Step 5: Calculate New Position: Determine the target start index for the shifted block.
        # The shift amount is equal to the block's length.
        new_start_index = start_index - block_length

        # Step 6: Place Block: Copy the block to the new position in the output grid.
        # Iterate through the length of the block to place each element.
        for i in range(block_length):
            target_index = new_start_index + i
            # Ensure the target index is within the valid bounds of the output list [0, list_length-1].
            if 0 <= target_index < list_length:
                output_grid[target_index] = block_value
            # Elements that would be shifted outside the list bounds (index < 0 or >= list_length) 
            # are implicitly handled as they are not written to the output_grid.

    # Step 7: Finalize: Return the resulting grid.
    return output_grid