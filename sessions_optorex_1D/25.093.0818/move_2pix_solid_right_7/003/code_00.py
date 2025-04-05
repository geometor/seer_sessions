import numpy as np

"""
Identifies the single contiguous block of identical non-zero digits within the 
input sequence string and shifts this block two positions to the right. The output 
sequence has the same length as the input, padded with zeros where the block 
is not present, and is returned as a space-separated string.
"""

def find_non_zero_block(sequence: np.ndarray) -> tuple | None:
    """
    Finds the first contiguous block of identical non-zero digits.

    Args:
        sequence: A numpy array of integers.

    Returns:
        A tuple (block_digit, start_index, end_index) if found, otherwise None.
            block_digit: The non-zero digit forming the block.
            start_index: The starting index of the block.
            end_index: The ending index (inclusive) of the block.
    """
    start_index = -1
    block_digit = 0

    # Iterate through the sequence to find the block start and end
    for i, digit in enumerate(sequence):
        # Found the start of a potential non-zero block
        if digit != 0 and start_index == -1:
            start_index = i
            block_digit = digit
        # Found the end of the block (either a different digit or a zero)
        # This condition is met when we are *past* the block's end
        elif start_index != -1 and digit != block_digit:
            end_index = i - 1 # The previous index was the end of the block
            return block_digit, start_index, end_index
        # Continue if inside the block or still searching for the start

    # Handle case where the block extends to the very end of the sequence
    if start_index != -1:
        end_index = len(sequence) - 1 # The last element is the end
        return block_digit, start_index, end_index

    # No non-zero block found (should not happen based on provided examples)
    return None

def transform(input_str: str) -> str:
    """
    Transforms the input digit sequence string.

    Args:
        input_str: A string containing space-separated digits (e.g., "0 0 6 6 6 0").

    Returns:
        A string containing the transformed space-separated digits.
    """
    # -- Step 1 & 2: Parse Input String to Integer Sequence --
    # Convert the input string into a numpy array of integers for easier processing.
    try:
        input_sequence = np.array([int(d) for d in input_str.split()], dtype=int)
        n = len(input_sequence) # Get the length of the sequence
    except ValueError:
        # Handle cases where input might not be valid numbers or format
        # For this specific problem, assume valid input based on examples.
        # In a more robust scenario, add error handling here.
        print(f"Error parsing input string: {input_str}")
        return "" # Or raise an exception

    # -- Step 3: Initialize Output Sequence --
    # Create an output array of the same size, filled with zeros.
    output_sequence = np.zeros(n, dtype=int)

    # -- Step 4 & 5: Find the Non-Zero Block --
    # Use the helper function to locate the non-zero block and its properties.
    block_info = find_non_zero_block(input_sequence)

    # Proceed only if a block was actually found
    if block_info:
        block_digit, start_index, end_index = block_info
        block_length = end_index - start_index + 1

        # -- Step 6 & 7: Calculate New Position --
        # Determine the new starting position by adding the shift amount (2).
        new_start_index = start_index + 2
        # Calculate the effective end boundary for placement in the output,
        # ensuring it doesn't exceed the array bounds.
        # The slice end is exclusive, so we use new_start + length.
        new_end_boundary = min(new_start_index + block_length, n)

        # -- Step 8: Place Shifted Block --
        # Check if the *start* of the shifted block is within the grid bounds.
        if new_start_index < n:
            # Place the block digit into the calculated slice of the output sequence.
            # Numpy's slicing assignment handles placing the 'block_digit'
            # value into all elements of the specified range [new_start_index, new_end_boundary).
            output_sequence[new_start_index:new_end_boundary] = block_digit

    # -- Step 9 & 10: Format Output --
    # Convert the output numpy array back to a list of strings, then join them
    # with spaces to match the required output format.
    output_str = " ".join(map(str, output_sequence))

    # -- Step 11: Return Result --
    return output_str
