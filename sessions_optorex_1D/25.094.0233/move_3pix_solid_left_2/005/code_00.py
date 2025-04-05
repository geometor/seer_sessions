"""
Transforms an input sequence (list or NumPy array of 12 integers) by identifying the first contiguous block of a single non-zero digit and shifting this block three positions to the left. The space vacated by the shift is filled with zeros, and elements shifted beyond the left boundary (index < 0) are discarded. The digit value and length of the block are preserved.
"""

import numpy as np

# Helper function to find the non-zero block
def find_non_zero_block(sequence):
    """
    Finds the first contiguous block of a non-zero digit in a sequence.

    Args:
        sequence: A list or 1D numpy array of integers.

    Returns:
        A tuple (digit, start_index, length) if a block is found,
        otherwise (None, -1, 0). Returns (None, -1, 0) if sequence is empty.
    """
    if sequence is None or len(sequence) == 0: # Handle empty or None sequence case
        return None, -1, 0
        
    start_index = -1
    digit = None
    length = 0
    n = len(sequence)

    # Iterate through the sequence to find the start of the block
    for i in range(n):
        # Check if the element is non-zero (and handles potential numpy types)
        current_val = sequence[i]
        if current_val != 0:
            # Found the first non-zero digit
            digit = current_val
            start_index = i
            length = 1
            # Count the length of the contiguous block of the same digit
            for j in range(i + 1, n):
                if sequence[j] == digit:
                    length += 1
                else:
                    break # End of the block
            # Block found and measured, exit the outer loop
            break

    # Convert numpy number types to standard Python types if necessary for consistency
    if isinstance(digit, np.integer):
        digit = int(digit)
        
    return digit, start_index, length

def transform(input_sequence):
    """
    Applies the block-shifting transformation to a 1D sequence.

    Args:
        input_sequence: A list or 1D NumPy array of 12 integers.

    Returns:
        A 1D NumPy array of 12 integers representing the transformed sequence.
    """
    # Determine the length of the sequence
    # Assuming input is always length 12 based on examples, but using len for robustness
    n = len(input_sequence)
    if n == 0:
        return np.array([]) # Handle empty input case

    # Initialize the output sequence with zeros, same length as input
    # Use numpy array for output as it's common in such tasks and matches potential input type
    output_sequence = np.zeros(n, dtype=int) 

    # Find the details (digit, start index, length) of the non-zero block
    digit, start_index, length = find_non_zero_block(input_sequence)

    # Proceed only if a non-zero block was actually found
    if start_index != -1:
        # Calculate the target starting position for the block after shifting left by 3
        shift_amount = -3
        new_start_index = start_index + shift_amount

        # Copy the block (digit repeated 'length' times) to the output sequence
        # starting at the new calculated position.
        for i in range(length):
            # Calculate the index in the output sequence for the current part of the block
            current_output_index = new_start_index + i
            
            # Ensure the placement index is within the valid bounds of the output sequence (0 to n-1)
            # This handles cases where the shifted block partially or fully goes off the left edge.
            if 0 <= current_output_index < n:
                output_sequence[current_output_index] = digit

    # Return the newly constructed output sequence as a NumPy array
    return output_sequence