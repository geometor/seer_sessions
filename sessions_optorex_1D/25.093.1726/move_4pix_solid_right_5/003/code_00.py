"""
Accepts a 1D NumPy array of 12 integers. Finds the unique contiguous block of 
identical non-zero digits within the input array. Creates a new 1D NumPy array 
of length 12, initialized to zeros. Calculates the target starting position 
for the block by adding 4 to its original starting position. Copies the block 
(same value and length) into the new array at the target position, respecting 
array boundaries. Returns the new array.
"""

import numpy as np

def find_contiguous_block(data: np.ndarray):
    """
    Finds the first contiguous block of identical non-zero digits in a 1D NumPy array.

    Args:
        data: The input 1D NumPy array of integers.

    Returns:
        A tuple containing (start_index, length, value) of the block.
        Returns (-1, 0, 0) if no such block is found or the array is empty.
        start_index is -1 if no block is found.
    """
    start_index = -1
    length = 0
    value = 0
    if data.size == 0: # Handle empty array case
        return start_index, length, value

    in_block = False
    for i, digit in enumerate(data):
        # Use .item() to get Python scalar for comparison if needed,
        # though direct numpy comparison often works. Assuming direct comparison is ok.
        if not in_block and digit != 0:
            # Start of a potential block
            start_index = i
            value = digit
            length = 1
            in_block = True
        elif in_block:
            if digit == value:
                # Continue the block
                length += 1
            else:
                # End of the block found before end of array
                return start_index, length, value # Return immediately when block ends

    # Handle case where block goes to the end of the list or no block found
    if in_block:
        return start_index, length, value
    else:
        # No block found throughout the array
        return -1, 0, 0


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Shifts a contiguous block of identical non-zero digits 4 positions to the right.

    Args:
        input_grid: A 1D NumPy array of 12 integers containing zeros and one 
                    contiguous block of identical non-zero digits.

    Returns:
        A new 1D NumPy array of 12 integers where the block has been shifted 
        4 positions to the right, and other positions are filled with zeros.
    """
    # Get the size of the input array
    grid_length = input_grid.shape[0]

    # Initialize output_grid with zeros, matching input size and type
    output_grid = np.zeros_like(input_grid)

    # Find the contiguous block in the input grid
    start_index, length, value = find_contiguous_block(input_grid)

    # Proceed only if a valid block was found (start_index is not -1)
    if start_index != -1:
        # Calculate the new starting index for the block by adding 4
        new_start_index = start_index + 4

        # Place the block into the output grid at the new position
        # Loop through the length of the identified block
        for i in range(length):
            # Calculate the target index in the output grid
            target_index = new_start_index + i
            
            # Check if the target index is within the valid bounds of the output grid
            if 0 <= target_index < grid_length:
                # Assign the block's value to the corresponding position in the output grid
                output_grid[target_index] = value

    # Return the modified output grid
    return output_grid