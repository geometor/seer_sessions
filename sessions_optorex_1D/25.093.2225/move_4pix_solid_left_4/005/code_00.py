"""
Transforms an input sequence (assumed to be a 1D list or array of 12 integers, potentially nested within a list) by identifying the first contiguous block of non-zero digits and shifting it 4 positions to the left. The sequence length remains 12, padded with zeros. Elements shifted outside the left boundary (index < 0) are omitted. If the input contains only zeros, the output is also all zeros.
"""

import numpy as np

def find_first_non_zero_block(sequence):
    """
    Finds the first contiguous block of non-zero elements and its start index.

    Args:
        sequence: A 1D list or NumPy array of integers.

    Returns:
        A tuple containing:
        - list: The block of non-zero integers.
        - int: The starting index of the block in the sequence.
        Returns (None, -1) if no non-zero block is found.
    """
    start_index = -1
    block = []
    in_block = False

    # Iterate through the sequence to find the block
    for i, val in enumerate(sequence):
        # Find the start of the block
        if not in_block and val != 0:
            start_index = i
            in_block = True
            block.append(val)
        # Continue adding to the block
        elif in_block and val != 0:
            block.append(val)
        # Detect the end of the block (hit a zero after being in a block)
        elif in_block and val == 0:
            break # Found the end of the first block

    # Handle case where no block was found
    if not block:
        return None, -1

    return block, start_index

def transform(input_grid):
    """
    Applies the block shifting transformation to the input grid.

    Args:
        input_grid: A list or array representing the input sequence.
                    Expected to contain 12 integers, potentially as [[...]].

    Returns:
        A list of 12 integers representing the transformed sequence.
    """
    # Define constants for the transformation
    sequence_length = 12
    shift_amount = -4 # Negative value indicates a left shift

    # --- Step 1: Ensure input is treated as a 1D sequence ---
    # Handle potential nesting like [[...]] by taking the first element if it looks 2D
    # or just using the input if it's already 1D.
    if isinstance(input_grid, (list, np.ndarray)) and len(input_grid) > 0 and isinstance(input_grid[0], (list, np.ndarray)):
         # Check if it looks like a grid/nested list and take the first row
         if len(np.array(input_grid).shape) > 1:
              sequence = list(np.array(input_grid)[0])
         else: # It might be a list of objects, treat as 1D
              sequence = list(np.array(input_grid))
    else: # Assume it's already a 1D list or array-like
        sequence = list(np.array(input_grid))

    # Ensure the sequence has the expected length, padding/truncating if necessary (optional, based on strictness)
    # For this problem, assume input always has length 12 based on examples.
    if len(sequence) != sequence_length:
        # Handle error or adjust sequence length if necessary
        # For now, assume correct length based on problem description
        pass 

    # --- Step 2: Initialize the output grid with zeros ---
    output_grid = np.zeros(sequence_length, dtype=int)

    # --- Step 3: Find the non-zero block and its starting position ---
    block, start_index = find_first_non_zero_block(sequence)

    # --- Step 4: Handle case where no block is found ---
    # If find_block returns None, the input was all zeros (or empty after handling).
    # The initialized zero grid is the correct output.
    if block is None:
        return output_grid.tolist() # Return as list

    # --- Step 5: Calculate the new starting index for the block ---
    new_start_index = start_index + shift_amount

    # --- Step 6: Place the block into the output grid at the new position ---
    # Iterate through the elements of the identified block
    for i, block_element in enumerate(block):
        # Calculate the target index in the output grid for this element
        target_index = new_start_index + i

        # Check if the target index is within the valid bounds of the output grid (0 to 11)
        if 0 <= target_index < sequence_length:
            # Place the block element into the output grid at the valid target index
            output_grid[target_index] = block_element
        # Elements whose target_index falls outside the bounds (e.g., < 0) are implicitly dropped

    # --- Step 7: Return the result ---
    # Convert NumPy array back to a list to match the typical output format
    return output_grid.tolist()