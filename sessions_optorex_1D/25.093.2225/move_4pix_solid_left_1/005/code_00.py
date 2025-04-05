"""
Identifies a single contiguous block of identical non-zero digits within an input sequence of 12 integers. Shifts this block 4 positions to the left, placing it into an output sequence of the same length (12) initialized with zeros. Positions outside the shifted block remain zero. Elements are only placed within the valid bounds (0-11) of the output sequence.
"""

# No external libraries needed for this logic, basic list operations suffice.
# import numpy as np # Not strictly required, but useful if input is guaranteed numpy

def find_object(sequence):
    """
    Finds the first contiguous block of identical non-zero digits.

    Args:
        sequence: A list or array-like structure of integers.

    Returns:
        A tuple (value, start_index, length) if an object is found,
        otherwise (None, -1, 0). Returns the first such block found.
    """
    start_index = -1
    value = None
    length = 0

    # Iterate through the sequence with index
    for i, digit in enumerate(sequence):
        # Convert element to standard Python int just in case it's a numpy type
        current_digit = int(digit)

        if start_index == -1:
            # State: Looking for the start of a block
            if current_digit != 0:
                # Found the start of a potential block
                start_index = i
                value = current_digit
                length = 1
        else:
            # State: Inside a potential block, check if it continues
            if current_digit == value:
                # Block continues, increment length
                length += 1
            else:
                # Block ended because the current digit is different
                # Return the details of the block found
                return value, start_index, length

    # After the loop, check if a block was found and ended exactly at the sequence end
    if start_index != -1:
        return value, start_index, length

    # If the loop finished and no block was ever started (e.g., all zeros or empty)
    return None, -1, 0

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: An iterable (list, tuple, numpy array) of 12 integers.

    Returns:
        A list of 12 integers representing the transformed sequence.
    """
    # Ensure input is a standard Python list to avoid potential type issues
    input_list = list(map(int, input_grid)) 
    n = len(input_list) # Expected to be 12

    # Initialize an output sequence of n zeros.
    output_grid = [0] * n

    # Scan the input sequence to find the first contiguous block of identical non-zero digits.
    # Record its digit value, its starting index, and its length.
    value, start_index, length = find_object(input_list)

    # If no such block is found (e.g., the input is all zeros), the output remains all zeros.
    # The function proceeds only if a block was found (value is not None).
    if value is not None:
        # Calculate its new starting index by subtracting 4 from its original starting index.
        new_start_index = start_index - 4

        # Iterate 'length' times, corresponding to each digit in the identified block:
        for i in range(length):
            # Calculate the target index in the output sequence for the current digit.
            target_index = new_start_index + i

            # If the target index is valid (between 0 and n-1, inclusive),
            # place the block's digit value at that position in the output sequence.
            if 0 <= target_index < n:
                output_grid[target_index] = value
            # Otherwise (if target_index is out of bounds), the element is effectively dropped.

    # Return the modified output sequence.
    return output_grid