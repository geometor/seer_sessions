import typing

def find_non_zero_block(sequence: typing.List[int]) -> typing.Tuple[typing.Optional[int], int, int]:
    """
    Finds the first contiguous block of a non-zero digit in the sequence.

    Args:
        sequence: The input list of integers.

    Returns:
        A tuple containing:
        - The non-zero digit found (or None if no non-zero digit exists).
        - The starting index of the block (-1 if not found).
        - The length of the block (0 if not found).
    """
    digit = None
    start_index = -1
    length = 0

    for i, value in enumerate(sequence):
        if value != 0:
            # Found the start of a potential block
            if digit is None:
                digit = value
                start_index = i
                length = 1
            # Continue counting if it's the same digit
            elif value == digit:
                length += 1
            # If a different non-zero digit is found, the first block ended
            else:
                break
        elif digit is not None:
            # Found a zero after the block started, so the block ended
            break
            
    # Handle case where only zeros were found after finding the start
    if digit is not None and length == 0 and start_index != -1:
        length = 1 # It was a single digit block
        
    # Handle case where loop finished while counting
    # No specific action needed here, length is already correct.

    # If no non-zero digit was ever found
    if digit is None:
        return None, -1, 0
        
    return digit, start_index, length

def transform(input_grid: typing.List[int]) -> typing.List[int]:
    """
    Transforms the input sequence by finding the single contiguous block 
    of a non-zero digit and shifting it left by a distance equal to its length. 
    The rest of the sequence is filled with zeros.
    """
    
    # Get the total length of the input sequence
    sequence_length = len(input_grid)
    
    # Initialize the output sequence with zeros
    output_grid = [0] * sequence_length

    # Find the non-zero block details: its digit, starting index, and length
    digit, start_index, block_length = find_non_zero_block(input_grid)

    # If no non-zero block is found (e.g., input is all zeros), return the zero-filled output
    if digit is None:
        return output_grid # Or potentially handle as an error, but based on examples return zeros

    # Calculate the shift amount (equal to the block length)
    shift_amount = block_length

    # Calculate the new starting index for the block in the output sequence
    # New Start = Original Start - Shift Amount
    new_start_index = start_index - shift_amount

    # Ensure the new start index is within bounds (although examples suggest it always is)
    if new_start_index < 0:
        # This case is not represented in the examples, but handle defensively
        # Option 1: Clamp to 0 (might lose part of the block)
        # Option 2: Raise an error 
        # Option 3: Based on examples, assume this won't happen.
        # Let's proceed assuming valid shifts based on provided examples.
        pass 

    # Place the non-zero block into the output sequence at the new position
    for i in range(block_length):
        # Calculate the index in the output grid
        output_index = new_start_index + i
        # Check if the output index is within the bounds of the grid
        if 0 <= output_index < sequence_length:
            output_grid[output_index] = digit
        else:
            # This part of the block would fall outside the grid after shifting.
            # Based on examples, this doesn't seem to happen.
            pass

    # Return the transformed sequence
    return output_grid