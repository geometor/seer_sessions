"""
Transforms an input sequence (potentially a 1D list, 1D NumPy array, or 2D (1, N) NumPy array of 12 integers) by identifying the first contiguous block of a single non-zero digit and shifting this block three positions to the left. The space vacated by the shift is filled with zeros, and elements shifted beyond the left boundary (index < 0) are discarded. The digit value and length of the block are preserved.
"""

import numpy as np

# Helper function to find the non-zero block
def find_non_zero_block(sequence):
    """
    Finds the first contiguous block of a non-zero digit in a 1D sequence.

    Args:
        sequence: A 1D list or numpy array of integers.

    Returns:
        A tuple (digit, start_index, length) if a block is found,
        otherwise (None, -1, 0). Returns (None, -1, 0) if sequence is empty or None.
    """
    if sequence is None or len(sequence) == 0: # Handle empty or None sequence case
        return None, -1, 0
        
    start_index = -1
    digit = None
    length = 0
    n = len(sequence)

    # Iterate through the sequence to find the start of the block
    for i in range(n):
        current_val = sequence[i]
        # Check if the element is non-zero 
        # (explicitly convert to standard int for comparison if numpy type)
        if int(current_val) != 0: 
            # Found the first non-zero digit
            digit = int(current_val) # Store as standard int
            start_index = i
            length = 1
            # Count the length of the contiguous block of the same digit
            for j in range(i + 1, n):
                if int(sequence[j]) == digit: # Compare as standard ints
                    length += 1
                else:
                    break # End of the block
            # Block found and measured, exit the outer loop
            break
        
    return digit, start_index, length

def transform(input_grid):
    """
    Applies the block-shifting transformation to the input sequence/grid.

    Args:
        input_grid: A list, 1D NumPy array, or 2D NumPy array (shape (1, 12)) 
                    of 12 integers.

    Returns:
        A 1D NumPy array of 12 integers representing the transformed sequence.
    """
    
    # 1. Handle Input Format: Ensure we have a 1D sequence
    sequence = np.array(input_grid) # Convert to numpy array first
    if sequence.ndim == 2 and sequence.shape[0] == 1:
        # If it's a 2D array with one row, flatten it to 1D
        sequence = sequence.flatten()
    elif sequence.ndim > 1:
        # Handle unexpected dimensions if necessary, or raise an error
        # For now, assume valid input or flatten might work
        sequence = sequence.flatten() # Attempt flatten for other cases too

    # Check if flattening resulted in a 1D array
    if sequence.ndim != 1:
         raise ValueError(f"Input could not be converted to a 1D sequence. Shape was {input_grid.shape if hasattr(input_grid, 'shape') else 'N/A'}")

    # 2. Get Sequence Length
    n = len(sequence)
    if n == 0:
        return np.array([], dtype=int) # Handle empty sequence case

    # Ensure length is 12 as per problem description (optional but good practice)
    # if n != 12:
    #    print(f"Warning: Input sequence length is {n}, expected 12.")
        # Decide how to handle: error, pad, truncate, or proceed? 
        # Proceeding for now.

    # 3. Initialize Output Sequence
    output_sequence = np.zeros(n, dtype=int) 

    # 4. Find the Non-Zero Block
    digit, start_index, length = find_non_zero_block(sequence)

    # 5. Shift Block if Found
    if start_index != -1: # Check if a block was actually found
        # a. Calculate the new starting index (shift left by 3)
        shift_amount = -3
        new_start_index = start_index + shift_amount

        # b. Copy the block to the output sequence at the new position
        for i in range(length):
            # Calculate the target index in the output sequence
            target_index = new_start_index + i

            # Check if the target index is within the valid bounds (0 to n-1)
            if 0 <= target_index < n:
                # Place the digit at the valid target index
                output_sequence[target_index] = digit

    # 6. Return the constructed output sequence
    return output_sequence