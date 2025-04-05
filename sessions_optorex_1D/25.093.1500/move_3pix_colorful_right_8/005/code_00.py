import numpy as np

"""
Transforms an input sequence of 12 digits by identifying the single contiguous block 
of non-zero digits (1-9) and shifting this block 3 positions to the right. 
The output sequence is also 12 digits long, padded with zeros in positions 
not occupied by the shifted block. Handles input as list, 1D NumPy array, or 
2D NumPy array with one row. If no non-zero block exists, returns a sequence of 
12 zeros.
"""

def _standardize_input(input_data):
    """
    Ensures the input data is a flat list of integers.

    Args:
        input_data: Can be a list, 1D NumPy array, or 2D NumPy array (1 row).

    Returns:
        A flat list of integers.
    """
    if isinstance(input_data, np.ndarray):
        # Flatten the array in case it's 2D (e.g., [[1, 2, 3]]) and convert to list
        return input_data.flatten().tolist()
    elif isinstance(input_data, list):
        # Check if it's a list of lists (like [[1, 2, 3]])
        if input_data and isinstance(input_data[0], list):
            # Flatten the list of lists
            return [item for sublist in input_data for item in sublist]
        else:
            # Already a flat list (or assumed to be)
            return list(input_data) # Ensure it's a mutable list copy
    else:
        raise TypeError("Input data must be a list or NumPy array.")


def _find_nonzero_block(int_list):
    """
    Finds the start index and the values of the first contiguous block of non-zero digits.

    Args:
        int_list: A list of integers.

    Returns:
        A tuple (start_index, block_values) or (None, []) if no non-zero digits are found.
        start_index: The index of the first non-zero digit.
        block_values: A list containing the non-zero digits in the block.
    """
    start_index = -1
    block_values = []
    n = len(int_list)

    # Find the first non-zero digit
    for i, val in enumerate(int_list):
        if val != 0:
            start_index = i
            break

    # If no non-zero digit found, return early
    if start_index == -1:
        return None, []

    # Collect values from the start index until a zero or the end is reached
    for i in range(start_index, n):
        if int_list[i] != 0:
            block_values.append(int_list[i])
        else:
            # Stop as soon as a zero is encountered after the block started
            break

    return start_index, block_values


def transform(input_grid):
    """
    Applies the transformation rule to the input sequence.
    """
    # Standardize the input into a flat list of 12 integers
    input_list = _standardize_input(input_grid)
    n = 12 # Expected length based on examples

    if len(input_list) != n:
        # Handle potential inconsistencies if needed, though examples suggest fixed length
        # For now, proceed assuming length is 12 or handle error
         print(f"Warning: Input length is {len(input_list)}, expected {n}. Proceeding with actual length.")
         n = len(input_list) # Adjust n based on actual input if flexible length is allowed


    # Initialize output_grid with zeros
    output_grid = [0] * n

    # Find the contiguous block of non-zero digits in the input
    start_index, block_values = _find_nonzero_block(input_list)

    # If a block was found, calculate its new position and place it
    if start_index is not None:
        # Define the shift amount
        shift_amount = 3

        # Calculate the new starting position for the block in the output
        new_start_index = start_index + shift_amount

        # Place the block values into the output grid at the new position
        # Iterate through the values found in the block
        for i, value in enumerate(block_values):
            # Calculate the target index in the output grid
            output_index = new_start_index + i
            # Check if the target index is within the bounds of the grid (0 to n-1)
            if 0 <= output_index < n:
                output_grid[output_index] = value

    # Return the transformed grid as a list
    return output_grid