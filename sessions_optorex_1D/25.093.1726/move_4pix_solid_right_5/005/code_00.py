"""
Transforms a 1D sequence of 12 integers by identifying a contiguous block of 
identical non-zero digits and shifting this block 4 positions to the right. 
The rest of the sequence is filled with zeros.
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
        start_index is -1 if no block was found.
    """
    start_index = -1
    length = 0
    value = 0
    if data.size == 0: # Handle empty array case
        return start_index, length, value

    in_block = False
    # Iterate through the elements of the 1D array
    for i, digit in enumerate(data):
        # Ensure 'digit' is treated as a scalar
        current_digit = digit.item() if isinstance(digit, np.generic) else digit

        if not in_block and current_digit != 0:
            # Start of a potential block
            start_index = i
            value = current_digit
            length = 1
            in_block = True
        elif in_block:
            # Check if the current digit continues the block
            if current_digit == value:
                length += 1
            else:
                # End of the block found before the end of the array
                # Return the properties of the block found
                return start_index, length, value

    # If the loop finishes, check if we were in a block that extended to the end
    if in_block:
        return start_index, length, value
    else:
        # No block was found throughout the array
        return -1, 0, 0


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Shifts a contiguous block of identical non-zero digits 4 positions to the right
    within a 1D NumPy array.

    Args:
        input_grid: A 1D NumPy array of 12 integers containing zeros and potentially 
                    one contiguous block of identical non-zero digits.

    Returns:
        A new 1D NumPy array of 12 integers where the block has been shifted 
        4 positions to the right, and other positions are filled with zeros.
    """
    # Ensure input is a 1D array
    if input_grid.ndim != 1:
        # Handle error or unexpected input dimension appropriately
        # For now, assume it will be 1D based on examples
        # Or raise an error: raise ValueError("Input grid must be 1D")
        pass # Or return input_grid, or an empty array etc. based on desired handling

    # Get the size of the input array
    grid_length = input_grid.shape[0]

    # Initialize output_grid with zeros, matching input size and data type
    output_grid = np.zeros_like(input_grid)

    # Find the contiguous block in the input grid
    start_index, length, value = find_contiguous_block(input_grid)

    # Proceed only if a valid block was found (start_index is not -1)
    if start_index != -1:
        # Calculate the new starting index for the block by adding 4
        new_start_index = start_index + 4

        # Place the block into the output grid at the new position
        # Iterate through the length of the identified block
        for i in range(length):
            # Calculate the target index in the output grid for the current element of the block
            target_index = new_start_index + i
            
            # Check if the target index is within the valid bounds of the output grid
            if 0 <= target_index < grid_length:
                # Assign the block's value to the corresponding position in the output grid
                output_grid[target_index] = value

    # Return the modified output grid
    return output_grid