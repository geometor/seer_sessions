"""
Transforms an input sequence (represented as a 1xN grid) by shifting a 
contiguous block of identical non-zero digits within the single row to the right. 
The shift distance is equal to the length of the block. The rest of the 
sequence is filled with zeros. Returns the transformed sequence as a 1xN grid.
"""

# No external imports are necessary for this logic with standard lists.

def find_nonzero_block(sequence):
    """
    Finds the start index, value, and length of the first contiguous block of
    identical non-zero digits in the sequence.

    Args:
        sequence: A list of integers.

    Returns:
        A tuple (start_index, value, length) if a block is found.
        Returns (-1, None, 0) if no block is found.
    """
    start_index = -1
    value = None
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
                    # Block ends here as the value changed or end of sequence reached
                    break
            # Found the first block, no need to continue searching the sequence
            break

    # Return properties if a block was found, otherwise return indication of no block
    return start_index, value, length


def transform(input_grid):
    """
    Applies the block shifting transformation to the input grid.

    Args:
        input_grid: A list of lists of integers representing the input grid.
                    Expected to contain a single row (e.g., [[0, 0, 1, 1, 0]]).

    Returns:
        A list of lists of integers representing the transformed grid.
    """
    # Basic validation for grid structure (expecting 1xN)
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
         # Return an empty grid representation or handle error as appropriate
         # Returning format consistent with expected output type
         return [[]] 
         
    # Extract the single row sequence from the input grid
    input_sequence = input_grid[0]
    n = len(input_sequence) # Get the length (number of columns)

    # Initialize the output sequence with zeros
    output_sequence = [0] * n

    # Find the properties (start index, value, length) of the non-zero block
    input_start_index, block_value, block_length = find_nonzero_block(input_sequence)

    # Proceed only if a non-zero block was actually found
    if input_start_index != -1:
        # Calculate the starting index for the block in the output sequence
        # Rule: output_start_index = input_start_index + block_length
        output_start_index = input_start_index + block_length

        # Place the identified block into the output sequence at the calculated position
        # Iterate for the length of the block
        for i in range(block_length):
            # Calculate the target index in the output sequence for this element of the block
            current_output_index = output_start_index + i

            # Check if the calculated index is within the bounds of the output sequence
            if 0 <= current_output_index < n:
                # If within bounds, place the block's value at that index
                output_sequence[current_output_index] = block_value
            # else: If the block placement goes out of bounds (current_output_index >= n),
            #       that part of the block is effectively dropped. No explicit action needed.

    # Wrap the transformed sequence back into the grid format (list of lists)
    output_grid = [output_sequence]

    # Return the resulting output grid
    return output_grid