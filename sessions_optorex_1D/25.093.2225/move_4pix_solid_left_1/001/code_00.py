import math

def find_object(sequence):
    """
    Finds the first contiguous block of identical non-zero digits.

    Args:
        sequence: A list of integers.

    Returns:
        A tuple (value, start_index, length) if an object is found,
        otherwise (None, -1, 0).
    """
    start_index = -1
    value = None
    length = 0

    for i, digit in enumerate(sequence):
        if start_index == -1:
            # Look for the start of a block
            if digit != 0:
                start_index = i
                value = digit
                length = 1
        else:
            # We are inside a potential block
            if digit == value:
                length += 1
            else:
                # Block ended
                return value, start_index, length

    # Check if the block ended exactly at the end of the sequence
    if start_index != -1:
        return value, start_index, length

    # No non-zero block found
    return None, -1, 0

def transform(input_str):
    """
    Identifies a contiguous block of identical non-zero numbers in the input sequence,
    shifts this block 4 positions to the left, placing it into an output sequence
    of the same length (12) initialized with zeros. Positions vacated by the shift
    or outside the shifted block are filled with zeros.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_str.split()]
    n = len(input_list) # Should always be 12 based on examples

    # Initialize the output grid (list) with zeros
    output_list = [0] * n

    # Find the contiguous block of non-zero numbers
    value, start_index, length = find_object(input_list)

    # If an object was found, place it in the shifted position
    if value is not None:
        # Calculate the new starting position (shift left by 4)
        new_start_index = start_index - 4

        # Place the object into the output list at the new position
        for i in range(length):
            target_index = new_start_index + i
            # Ensure the target index is within the bounds of the list
            if 0 <= target_index < n:
                output_list[target_index] = value

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))
    return output_str
