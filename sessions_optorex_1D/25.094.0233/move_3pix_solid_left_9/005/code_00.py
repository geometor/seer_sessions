import numpy as np

"""
Transforms an input grid (expected 1x12 NumPy array) containing a sequence of 12 single-digit integers. 
It identifies a single contiguous block of identical non-zero digits within the sequence. 
This block is then shifted 3 positions to the left (towards index 0) in the output sequence. 
The output sequence is initialized with zeros, and only the positions corresponding to the shifted block are updated with the block's value. 
Positions outside the shifted block remain zero. The length and value of the block are preserved.
"""


def find_block_properties(sequence):
    """
    Finds the start index, length, and value of the first contiguous non-zero block.

    Args:
        sequence: A 1D list or numpy array of integers.

    Returns:
        A tuple (start_index, block_length, block_value) or (-1, 0, 0) if no block is found.
        start_index = -1 indicates no block found.
    """
    start_index = -1
    block_value = 0
    block_length = 0
    in_block = False

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


def transform(input_grid: np.ndarray) -> list:
    """
    Applies the block shift transformation to the input grid.

    Args:
        input_grid: A 1x12 NumPy array of integers.

    Returns:
        A list of 12 integers representing the transformed sequence.
    """
    # Define constants for the transformation
    sequence_length = 12
    shift_amount = 3
    background_value = 0

    # --- Step 1 & 2: Extract the 1D sequence from the input grid ---
    # Validate input shape (optional but good practice)
    if not isinstance(input_grid, np.ndarray) or input_grid.shape != (1, sequence_length):
         # Attempt to handle list-of-lists input if needed, or raise error
         # For now, assume correct input or try to reshape/extract if possible
         try:
             input_grid = np.array(input_grid) # Try converting potential list-of-lists
             if input_grid.shape == (sequence_length,): # If it was already 1D list
                  input_grid = input_grid.reshape(1, sequence_length) # Make it 2D
             elif input_grid.shape != (1, sequence_length):
                   raise ValueError(f"Input grid must be reshapeable to (1, {sequence_length}), but got shape {input_grid.shape}")
         except Exception as e:
             raise ValueError(f"Invalid input format: {e}")

    input_sequence = input_grid[0] # Extract the first (and only) row as a 1D sequence

    # --- Step 4: Initialize the output sequence ---
    output_sequence = [background_value] * sequence_length

    # --- Step 3: Identify the non-zero block ---
    start_index, block_length, block_value = find_block_properties(input_sequence)

    # --- Step 5: Calculate shift and place the block (if found) ---
    if start_index != -1: # Check if a block was found
        # 5a: Calculate the new starting index
        new_start_index = start_index - shift_amount

        # 5b: Place the block into the output sequence
        for i in range(block_length):
            # 5bi: Calculate the target index
            target_index = new_start_index + i
            # 5bii: Check bounds and place the value
            if 0 <= target_index < sequence_length:
                output_sequence[target_index] = block_value

    # --- Step 6 is implicit: non-filled positions remain background_value ---

    # --- Step 7: Return the constructed output sequence ---
    return output_sequence