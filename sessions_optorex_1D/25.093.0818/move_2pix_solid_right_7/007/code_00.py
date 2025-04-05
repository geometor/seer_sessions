import numpy as np

"""
Transforms an input sequence of digits, represented as a 1D NumPy array.
The transformation identifies the single contiguous block of identical non-zero 
digits within the sequence and shifts this block exactly two positions to the 
right. The resulting sequence maintains the original length, with positions 
not occupied by the shifted block filled with zeros. The output is returned 
as a space-separated string.
"""

def find_non_zero_block(sequence: np.ndarray) -> tuple | None:
    """
    Finds the first contiguous block of identical non-zero digits in a sequence.

    Args:
        sequence: A 1D numpy array of integers representing the input sequence.

    Returns:
        A tuple (block_digit, start_index, end_index) if a block is found, 
        where start_index and end_index are inclusive. Returns None if no 
        such block is found.
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

    # No non-zero block found
    return None

def transform(input_grid: np.ndarray) -> str:
    """
    Applies the transformation rule to the input numpy array.

    Args:
        input_grid: A 1D numpy array of integers.

    Returns:
        A string containing the transformed space-separated digits.
    """
    # --- Get Input Sequence Properties ---
    # Assume input_grid is already a numpy array
    input_sequence = input_grid 
    n = len(input_sequence) # Determine the length of the sequence

    # --- Initialize Output ---
    # Create an output numpy array of the same length, initialized with zeros.
    output_sequence = np.zeros(n, dtype=int)

    # --- Find the Block ---
    # Use the helper function to find the non-zero block and its properties.
    block_info = find_non_zero_block(input_sequence)

    # --- Apply Transformation ---
    # Proceed only if a valid block was found.
    if block_info:
        block_digit, start_index, end_index = block_info
        block_length = end_index - start_index + 1 # Calculate the length of the block

        # Calculate the new starting position for the block (shift right by 2).
        new_start_index = start_index + 2

        # Calculate the new ending boundary for placing the block in the output.
        # This is the index *after* the last element of the shifted block.
        # Ensure the boundary does not exceed the sequence length.
        new_end_boundary = min(new_start_index + block_length, n)

        # Place the block into the output sequence if the new start index is valid.
        # Check if the *start* of the shifted block is within the bounds.
        if new_start_index < n:
            # Use numpy slicing to assign the block_digit to the target range.
            # The slice output_sequence[start:end] affects indices from start up to (but not including) end.
            output_sequence[new_start_index:new_end_boundary] = block_digit

    # --- Format Output ---
    # Convert the output numpy array back to a list of strings.
    output_list_str = [str(digit) for digit in output_sequence]
    # Join the list elements with spaces to create the final output string.
    output_str = " ".join(output_list_str)

    return output_str