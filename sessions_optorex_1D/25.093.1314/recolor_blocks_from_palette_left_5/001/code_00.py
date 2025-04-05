"""
Transforms an input sequence (list of 12 integers) based on the following rules:

1. Identify the two replacement values: R1 is the element at index 10, and R2 is the element at index 11.
2. Find all contiguous blocks of the number 5 within the first 10 elements (indices 0-9) of the input sequence.
3. If exactly one block of 5s is found, replace all the 5s within that block with the value R2.
4. If exactly two blocks of 5s are found, replace all the 5s in the first block with R1 and all the 5s in the second block with R2.
5. Leave all other numbers (non-5s in the first 10 elements, and the elements at indices 10 and 11) unchanged.
"""

import collections

def find_contiguous_blocks(sequence, target_value, start_index, end_index_exclusive):
    """
    Finds contiguous blocks of a target value within a slice of a sequence.

    Args:
        sequence: The input list or tuple.
        target_value: The value to search for blocks of.
        start_index: The starting index of the slice (inclusive).
        end_index_exclusive: The ending index of the slice (exclusive).

    Returns:
        A list of tuples, where each tuple represents a block
        as (start_index, end_index_exclusive).
    """
    blocks = []
    in_block = False
    block_start = -1
    for i in range(start_index, end_index_exclusive):
        is_target = (sequence[i] == target_value)
        if is_target and not in_block:
            # Start of a new block
            in_block = True
            block_start = i
        elif not is_target and in_block:
            # End of the current block
            in_block = False
            blocks.append((block_start, i))
            block_start = -1

    # Check if a block extends to the very end of the searched range
    if in_block:
        blocks.append((block_start, end_index_exclusive))

    return blocks

def transform(input_list):
    """
    Applies the transformation rule to the input list.

    Args:
        input_list: A list of 12 integers.

    Returns:
        A new list of 12 integers representing the transformed output.
    """
    # Ensure input is a list (or make a mutable copy)
    if not isinstance(input_list, list):
        input_list = list(input_list) # Make sure we have a list

    # initialize output_grid by copying the input
    output_list = list(input_list)

    # Define the target value and the range to search within
    target_value = 5
    search_start_index = 0
    search_end_index = 10 # Exclusive, so indices 0-9

    # Get the replacement values from the end of the input list
    if len(input_list) >= 12:
        replacement_value_1 = input_list[10]
        replacement_value_2 = input_list[11]
    else:
        # Handle potential errors if the input list is too short, though
        # examples suggest it's always length 12.
        # For now, let's raise an error or return input, depending on desired behavior.
        # Returning input might be safer for this specific task context.
        print("Warning: Input list has fewer than 12 elements.")
        return output_list # Or raise ValueError("Input list must have at least 12 elements.")


    # Find blocks of the target value (5)
    five_blocks = find_contiguous_blocks(
        input_list, target_value, search_start_index, search_end_index
    )

    # Apply replacement logic based on the number of blocks found
    num_blocks = len(five_blocks)

    if num_blocks == 1:
        # Replace the single block with R2
        start, end = five_blocks[0]
        for i in range(start, end):
            output_list[i] = replacement_value_2
    elif num_blocks == 2:
        # Replace the first block with R1
        start1, end1 = five_blocks[0]
        for i in range(start1, end1):
            output_list[i] = replacement_value_1
        # Replace the second block with R2
        start2, end2 = five_blocks[1]
        for i in range(start2, end2):
            output_list[i] = replacement_value_2

    # Elements not in the blocks, and elements at index 10 and 11,
    # remain as they were in the initial copy.

    return output_list