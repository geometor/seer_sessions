import numpy as np

"""
Identifies the single contiguous block of identical non-zero digits within the 
input sequence and shifts this block two positions to the right. The output 
sequence has the same length as the input, padded with zeros where the block 
is not present.
"""

def find_non_zero_block(sequence):
    """
    Finds the first contiguous block of identical non-zero digits.

    Args:
        sequence: A list or numpy array of integers.

    Returns:
        A tuple (block_digit, start_index, end_index) if found, otherwise None.
            block_digit: The non-zero digit forming the block.
            start_index: The starting index of the block.
            end_index: The ending index (inclusive) of the block.
    """
    start_index = -1
    block_digit = 0

    # Iterate through the sequence to find the block start
    for i, digit in enumerate(sequence):
        # Found the start of a non-zero block
        if digit != 0 and start_index == -1:
            start_index = i
            block_digit = digit
        # Found the end of the block (either a different digit or a zero)
        # This condition is met when we are *past* the block
        elif start_index != -1 and digit != block_digit:
            end_index = i - 1 # The previous index was the end
            return block_digit, start_index, end_index
        # Continue if inside the block or still looking for the start

    # Handle case where the block extends to the very end of the sequence
    if start_index != -1:
        end_index = len(sequence) - 1 # The last element is the end
        return block_digit, start_index, end_index

    # No non-zero block found (should not happen based on provided examples)
    return None


def transform(input_str: str) -> str:
    """
    Transforms the input digit sequence string by finding the single contiguous 
    block of non-zero digits and shifting it right by 2 positions.

    Args:
        input_str: A string containing space-separated digits.

    Returns:
        A string containing the transformed space-separated digits.
    """
    # -- Parse Input --
    # Convert the input string into a numpy array of integers for easier processing
    input_sequence = np.array([int(d) for d in input_str.split()], dtype=int)
    n = len(input_sequence) # Get the length of the sequence

    # -- Find the Block --
    # Use the helper function to locate the non-zero block and its properties
    block_info = find_non_zero_block(input_sequence)

    # -- Initialize Output --
    # Create an output array of the same size, filled with zeros
    output_grid = np.zeros(n, dtype=int)

    # Proceed only if a block was actually found
    if block_info:
        block_digit, start_index, end_index = block_info
        block_length = end_index - start_index + 1

        # -- Calculate New Position --
        # Determine the new starting position by adding the shift amount
        new_start_index = start_index + 2
        # Calculate the effective end index for placement in the output, 
        # ensuring it doesn't exceed the array bounds.
        new_end_boundary = min(new_start_index + block_length, n)

        # -- Place Shifted Block --
        # Check if the *start* of the shifted block is within the grid bounds
        if new_start_index < n:
            # Place the block digit into the calculated slice of the output grid.
            # Numpy's slicing assignment handles placing the 'block_digit' 
            # value into all elements of the specified range.
            # Example: output_grid[5:12] = 6 assigns 6 to indices 5 through 11.
            output_grid[new_start_index:new_end_boundary] = block_digit

    # -- Format Output --
    # Convert the output numpy array back to a list of strings, then join them
    # with spaces to match the required output format.
    output_str = " ".join(map(str, output_grid))

    return output_str