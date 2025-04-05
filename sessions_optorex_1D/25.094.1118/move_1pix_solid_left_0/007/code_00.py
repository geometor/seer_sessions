import numpy as np # Although list operations suffice, numpy can be useful for array manipulations if needed later.

"""
Transforms an input sequence (list of integers) by identifying the first contiguous block
of identical non-zero integers. If this block starts at an index greater than 0,
it is shifted one position to the left. This shift is achieved by creating a new
zero-filled list of the same length and placing the block at the shifted position.
Zeros naturally fill the remaining positions, including the one appended implicitly at the end.
If no non-zero block is found, or if the block starts at index 0, the original
sequence is returned unchanged (as a new list).
"""

def find_non_zero_block_indices(data_list):
    """
    Finds the start and end indices of the first contiguous block of
    identical non-zero numbers.

    Args:
        data_list: A list of numbers.

    Returns:
        A tuple (start_index, end_index) if a block is found,
        otherwise returns (None, None). end_index is exclusive.
    """
    start_index = -1
    end_index = -1
    block_value = None

    for i, val in enumerate(data_list):
        if val != 0:
            # Found a non-zero value
            if start_index == -1:
                # This is the start of the block
                start_index = i
                block_value = val
            # Ensure the value is the same as the block's start value
            # (This handles potential adjacent blocks of different non-zeros,
            # though examples don't show this)
            elif val != block_value:
                # Found a different non-zero, the block ended *before* this index.
                end_index = i
                return start_index, end_index # Return the first block found

        elif start_index != -1:
            # Found a zero after starting a block. The block ends here.
            end_index = i
            # Return the found indices
            return start_index, end_index

    # If the loop finishes and we were in a block, it means the block extends to the end
    if start_index != -1:
        end_index = len(data_list)
        # Return the found indices
        return start_index, end_index

    # No non-zero block was found at all
    return None, None


def transform(input_list):
    # Ensure working with a list and make a copy to avoid modifying original external lists
    current_list = list(input_list)
    list_len = len(current_list)

    # Find the start and end indices of the non-zero block
    start_index, end_index = find_non_zero_block_indices(current_list)

    # Check if a block was found and if it can be shifted left (i.e., not starting at index 0)
    if start_index is not None and start_index > 0:
        # Calculate the length of the block
        block_length = end_index - start_index
        # Calculate the new starting position for the block
        new_start_index = start_index - 1

        # Initialize the output list with all zeros
        output_list = [0] * list_len

        # Extract the block from the original list
        block = current_list[start_index:end_index]

        # Place the block into the output list at the new position
        # output_list[new_start_index : new_start_index + block_length] = block[:] # Slice assignment
        for i in range(block_length):
             output_list[new_start_index + i] = block[i]


        # Return the newly constructed list with the shifted block
        return output_list
    else:
        # If no block found, or block starts at index 0, return the original list (as a copy)
        return current_list