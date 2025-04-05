"""
Transforms an input sequence by shifting a contiguous block of identical non-zero digits to the right. The shift distance is equal to the length of the block. The rest of the sequence is filled with zeros.
"""

# No external imports are necessary for this logic with standard lists.

def find_nonzero_block(sequence):
    """
    Finds the start index, value, and length of the first contiguous block of
    identical non-zero digits in the sequence.

    Args:
        sequence: A list of integers.

    Returns:
        A tuple (start_index, value, length) if a block is found,
        otherwise (None, None, None).
    """
    start_index = -1
    value = 0
    length = 0
    n = len(sequence)

    # Iterate through the sequence to find the start of the block
    for i, element in enumerate(sequence):
        # Found the first non-zero element
        if element != 0:
            start_index = i
            value = element
            length = 1
            # Check subsequent elements to determine the block's length
            for j in range(i + 1, n):
                if sequence[j] == value:
                    length += 1
                else:
                    # Block ends here as the value changed
                    break 
            # Found the first block, no need to continue searching the sequence
            break 
            
    # Return None if no non-zero element was found
    if start_index == -1:
        return None, None, None
    else:
        return start_index, value, length

def transform(input_grid):
    """
    Applies the block shifting transformation to the input sequence (list).
    
    Args:
        input_grid: A list of integers representing the input sequence. 
                    Expected to be a flat list based on examples.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Ensure input is treated as a flat list
    if not isinstance(input_grid, list):
        # Basic check, might need more robust handling depending on actual input format
        raise TypeError("Input must be a list of integers.")
        
    # Determine the size of the grid/sequence
    n = len(input_grid)
    
    # Initialize output_grid with zeros of the same length as the input
    output_grid = [0] * n

    # Find the properties (start index, value, length) of the non-zero block
    input_start_index, block_value, block_length = find_nonzero_block(input_grid)

    # If no non-zero block is found, the output is already initialized to all zeros
    if input_start_index is None:
        return output_grid

    # Calculate the starting index for the block in the output sequence
    # The rule identified is: output_start_index = input_start_index + block_length
    output_start_index = input_start_index + block_length

    # Place the identified block into the output sequence at the calculated position
    for i in range(block_length):
        # Calculate the index in the output grid for the current part of the block
        current_output_index = output_start_index + i
        
        # Check if the calculated index is within the bounds of the output grid
        if 0 <= current_output_index < n: 
            output_grid[current_output_index] = block_value
        # else: 
            # If the block placement goes out of bounds based on the rule, 
            # those parts of the block are effectively dropped, matching example behavior.
            # No explicit action needed here.

    # Return the newly constructed output sequence
    return output_grid