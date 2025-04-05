import math

def transform(input_sequence):
    """
    Transforms an input sequence of 0s and 2s into an output sequence of 0s, 2s, and 8s.
    The transformation identifies contiguous blocks of '2's in the input. For each block 
    of length L, the first floor(L / 2) elements ('2's) within that block are changed 
    to '8' in the output sequence. All other elements ('0's and the remaining '2's) 
    are copied directly to the output sequence at the same position.
    """

    # Initialize the output sequence as a copy of the input sequence (list).
    # This handles the '0's correctly and sets the initial state for '2's.
    output_sequence = list(input_sequence)
    n = len(input_sequence)
    i = 0 # Initialize the index for iterating through the sequence

    # Iterate through the sequence using a while loop to allow manual index advancement
    # when processing blocks of '2's.
    while i < n:
        # Check if the current element is the start of a potential block of '2's
        if output_sequence[i] == 2:
            # Record the starting index of the block
            start_index = i

            # Find the end of the contiguous block of '2's
            current_index = i
            while current_index < n and output_sequence[current_index] == 2:
                current_index += 1
            # end_index points to the element *after* the block
            end_index = current_index

            # Calculate the length of the block
            length = end_index - start_index

            # Calculate the number of '2's to change to '8' using integer division (floor)
            num_changes = length // 2

            # Apply the transformation: change the first 'num_changes' elements 
            # of the block in the output sequence to '8'.
            for j in range(num_changes):
                output_sequence[start_index + j] = 8
                
            # Advance the main loop index past the currently processed block
            # This prevents re-processing elements within the same block.
            i = end_index
        else:
            # If the element is '0', it's already correct in the output_sequence copy.
            # Simply move to the next element.
            i += 1

    # Return the transformed sequence
    return output_sequence