import math  # Standard math library, potentially useful though not directly used here.

"""
Shift a contiguous block of identical non-zero numbers leftwards within a 
fixed-length sequence (length 12) of numbers. The magnitude of the leftward 
shift is equal to the length of the block itself. The input might be a list
or a NumPy array, and the output should be a standard Python list of integers.
"""

def find_non_zero_block(sequence):
    """
    Finds the first contiguous block of identical non-zero numbers in a sequence.

    Args:
        sequence: A list or list-like object of numbers.

    Returns:
        A tuple (value, start_index, length) if a block is found,
        otherwise None.
        - value: The non-zero scalar value of the block elements.
        - start_index: The 0-based index where the block begins.
        - length: The number of elements in the block.
    """
    start_index = -1
    block_value = 0
    length = 0
    in_block = False

    # Iterate through the sequence to find the block
    for i, val in enumerate(sequence):
        # Ensure we are comparing scalar values, potentially handling numpy types implicitly
        # by comparing with standard Python integers (0).
        current_val = val # Use the element directly

        if not in_block and current_val != 0:
            # Start of a potential block
            in_block = True
            start_index = i
            block_value = current_val # Store the value found
            length = 1
        elif in_block:
            # Check if the current element continues the block
            # Comparison should work correctly between compatible numeric types
            if current_val == block_value:
                # Continue the block
                length += 1
            else:
                # End of the block (hit a different value or zero)
                # Assuming only one block per sequence based on examples
                break 
    
    # Return block details if found
    if start_index != -1:
        # Ensure the returned value is a standard Python int if needed downstream
        # Although comparison worked, final value might need casting depending on usage
        # For this task, returning the original type (like np.int64) is fine if it was input.
        return block_value, start_index, length
    else:
        # No non-zero block found
        return None

def transform(input_sequence):
    """
    Transforms the input sequence by shifting the non-zero block leftwards
    by a distance equal to its length.

    Args:
        input_sequence: A list or list-like object (e.g., NumPy array) of numbers.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Ensure input is treated as a sequence and get its length
    # Using list() handles potential iterables like numpy arrays
    input_list = list(input_sequence)
    n = len(input_list)
    
    # Initialize the output sequence as a list of standard Python integers (0)
    output_sequence = [0] * n

    # Find the contiguous block of non-zero numbers using the helper function
    block_info = find_non_zero_block(input_list)

    # Proceed only if a block was found
    if block_info:
        block_value, start_index, block_length = block_info

        # Calculate the shift distance (equal to block length)
        shift_distance = block_length

        # Calculate the new starting index for the block in the output
        # Use max(0, ...) to prevent negative indices if start_index < shift_distance
        new_start_index = max(0, start_index - shift_distance)

        # Place the block into the output sequence at the new position
        for i in range(block_length):
            # Calculate the target index in the output sequence
            target_index = new_start_index + i
            # Ensure the target index is within the bounds of the sequence
            if target_index < n:
                 # Ensure the value placed in the output list is a standard Python int
                 # This addresses potential downstream compatibility issues if block_value
                 # was a numpy type.
                output_sequence[target_index] = int(block_value)

    # Return the modified output sequence as a list of integers
    return output_sequence