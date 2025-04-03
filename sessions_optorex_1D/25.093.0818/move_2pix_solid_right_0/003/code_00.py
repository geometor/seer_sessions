import numpy as np # Import numpy although not strictly required by the core logic, it handles potential array inputs gracefully.

"""
Shifts the single contiguous block of identical non-zero digits 
found in the input sequence exactly two positions to the right. 
Positions originally occupied by the block become zeros unless 
overwritten by the shifted block. Returns the transformed 
sequence as a space-separated string.
"""

def find_non_zero_block(sequence):
    """
    Finds the first contiguous block of a non-zero digit in the sequence.

    Args:
        sequence: A list or array of integers.

    Returns:
        A tuple (block_value, start_index, end_index) if a block is found,
        otherwise (None, -1, -1). Returns -1 for indices if no block is found.
    """
    start_index = -1
    end_index = -1
    block_value = None

    # Iterate through the sequence to find the start of the block
    for i, val in enumerate(sequence):
        if val != 0:
            start_index = i
            block_value = val
            break # Found the start, break the loop

    # If a starting non-zero value was found, find the end of the block
    if start_index != -1:
        end_index = start_index # Initialize end_index
        # Continue from the element *after* the start index
        for i in range(start_index + 1, len(sequence)):
            if sequence[i] == block_value:
                end_index = i # Extend the block
            else:
                break # Block ended (different value or zero)
                
    return block_value, start_index, end_index


def transform(input_sequence):
    """
    Applies the block shifting transformation.

    Args:
        input_sequence: A list or numpy array of integers representing the input.

    Returns:
        A string representing the transformed sequence with elements separated by spaces.
    """
    # Determine the length of the input sequence
    n = len(input_sequence)

    # Initialize output_sequence with zeros of the same length
    output_sequence = [0] * n

    # Find the non-zero block in the input sequence
    block_value, start_index, end_index = find_non_zero_block(input_sequence)

    # If a block was found, proceed to shift it
    if block_value is not None and start_index != -1:
        # Calculate the new starting position for the block (shift right by 2)
        new_start_index = start_index + 2
        
        # Calculate the length of the block
        block_length = end_index - start_index + 1

        # Place the block in the output sequence at the new position
        # Iterate for the length of the block
        for i in range(block_length):
            # Calculate the target index in the output sequence
            new_index = new_start_index + i
            # Check bounds: Ensure the new index is within the sequence limits
            if 0 <= new_index < n:
                # Assign the block's value to the output sequence at the new index
                output_sequence[new_index] = block_value

    # Convert the output list of integers to a space-separated string
    output_sequence_str = " ".join(map(str, output_sequence))
    
    # Return the final string representation
    return output_sequence_str