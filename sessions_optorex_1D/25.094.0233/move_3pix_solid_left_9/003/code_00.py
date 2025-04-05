import numpy as np # Import numpy for potential array handling, although lists are primary

"""
Transforms an input sequence (list or array of 12 integers) by identifying a 
contiguous block of identical non-zero digits and shifting it 3 positions to the left. 
Positions outside the shifted block in the output sequence are filled with zeros.
"""

def find_block_properties(sequence):
    """
    Finds the start index, length, and value of the first contiguous non-zero block.

    Args:
        sequence: A list or 1D numpy array of integers.

    Returns:
        A tuple (start_index, block_length, block_value) or (-1, 0, 0) if no block is found.
        start_index = -1 indicates no block found.
    """
    start_index = -1
    block_value = 0
    block_length = 0
    in_block = False

    # Handle numpy array input by converting to list if necessary
    # Or just iterate directly if it supports indexing and iteration
    if isinstance(sequence, np.ndarray):
        # Ensure it's 1D before converting or iterating
        if sequence.ndim > 1:
             raise ValueError("Input sequence must be 1-dimensional")
        # Iteration works directly on numpy arrays
        pass # No conversion needed for iteration
    elif not isinstance(sequence, list):
         raise TypeError(f"Input sequence must be a list or 1D numpy array, got {type(sequence)}")

    # Scan the input sequence to find the block
    for i, val in enumerate(sequence):
        # Start of a new block
        if val != 0 and not in_block:
            start_index = i
            block_value = val
            block_length = 1
            in_block = True
        # Continue the current block
        elif in_block:
            if val == block_value:
                 block_length += 1
            # End of block (either zero or different non-zero)
            else:
                 break
        # else: val is 0 and not in_block, continue searching

    # If no non-zero value was ever found, start_index will remain -1
    if start_index == -1:
        return -1, 0, 0

    return start_index, block_length, block_value


def transform(input_grid):
    """
    Applies the block shift transformation to the input sequence.

    Args:
        input_grid: A list or 1D numpy array of 12 integers.

    Returns:
        A list of 12 integers representing the transformed sequence.
    """
    sequence_length = 12
    shift_amount = 3
    background_value = 0

    # 1. Initialize a new output sequence of 12 integers, filled with zeros.
    output_grid = [background_value] * sequence_length

    # 2. Scan the input sequence to find the block properties.
    #    (Steps 3, 4, 5 from NLP are handled by this helper function)
    start_index, block_length, block_value = find_block_properties(input_grid)

    # 3. If no non-zero block is found, return the initialized zero sequence.
    if start_index == -1:
        return output_grid # Return the sequence of zeros

    # 4. Calculate the new starting index for the block in the output sequence. (NLP Step 6)
    new_start_index = start_index - shift_amount

    # 5. Place the block into the output sequence at the new position. (NLP Step 7)
    for i in range(block_length):
        # a. Calculate the target index in the output sequence. (NLP Step 7a)
        target_index = new_start_index + i
        # b. If target_index is within valid bounds, place the block value. (NLP Step 7b)
        if 0 <= target_index < sequence_length:
            output_grid[target_index] = block_value

    # 6. Return the constructed output sequence. (NLP Step 8)
    return output_grid