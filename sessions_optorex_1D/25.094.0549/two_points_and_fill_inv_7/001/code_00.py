import copy

def find_blocks(sequence):
    """
    Identifies contiguous blocks of identical non-zero numbers in a sequence.

    Args:
        sequence: A list of integers.

    Returns:
        A list of tuples, where each tuple represents a block:
        (value, start_index, end_index).
    """
    blocks = []
    if not sequence:
        return blocks

    start_index = None
    current_value = None

    for i, value in enumerate(sequence):
        if value != 0:
            if start_index is None:
                # Start of a potential new block
                start_index = i
                current_value = value
            elif value != current_value:
                # End of the previous block, start of a new one
                blocks.append((current_value, start_index, i - 1))
                start_index = i
                current_value = value
        elif start_index is not None:
            # End of the current block due to encountering a zero
            blocks.append((current_value, start_index, i - 1))
            start_index = None
            current_value = None

    # Handle the case where a block extends to the end of the sequence
    if start_index is not None:
        blocks.append((current_value, start_index, len(sequence) - 1))

    return blocks

def transform(input_sequence):
    """
    Transforms a sequence of integers by preserving only the first and last
    elements of contiguous blocks of identical non-zero numbers longer than 
    two elements, changing the middle elements of such blocks to zero. 
    Zeros and blocks of length 1 or 2 remain unchanged.
    """
    
    # Initialize the output sequence as a copy of the input sequence.
    # We modify this copy directly.
    output_sequence = copy.deepcopy(input_sequence)

    # Iterate through the input sequence to identify contiguous blocks
    # of identical non-zero numbers.
    blocks = find_blocks(input_sequence)

    # For each identified block:
    for value, start_index, end_index in blocks:
        # Calculate block length
        block_length = end_index - start_index + 1
        
        # a. If the block length is greater than 2:
        if block_length > 2:
            # i. Iterate from the index immediately after the start index 
            #    up to (but not including) the end index.
            for i in range(start_index + 1, end_index):
                # ii. Set the value at each of these intermediate indices 
                #     in the *output* sequence to 0.
                output_sequence[i] = 0
                
    # Return the modified output sequence. 
    # (Zeros and blocks of length 1 or 2 were already correct 
    # due to initialization and the conditional modification).
    return output_sequence