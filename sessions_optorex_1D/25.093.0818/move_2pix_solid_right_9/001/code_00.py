import re # Using regex can simplify finding the block

"""
Identifies a contiguous block of identical non-zero integers within an input sequence 
and shifts this block two positions to the right, filling the vacated positions and 
any other positions with zeros, maintaining the original sequence length.
"""

def find_non_zero_block(int_list):
    """
    Finds the start index, end index, and value of the first contiguous 
    block of identical non-zero numbers in a list.

    Args:
        int_list: A list of integers.

    Returns:
        A tuple (start_index, end_index, value) if a block is found,
        otherwise (-1, -1, 0).
    """
    start_index = -1
    end_index = -1
    value = 0
    in_block = False

    for i, num in enumerate(int_list):
        if num != 0:
            if not in_block:
                # Start of a potential block
                start_index = i
                value = num
                end_index = i # Initialize end index
                in_block = True
            elif num == value:
                # Continue the current block
                end_index = i
            else:
                 # Found a different non-zero number, stop (shouldn't happen per examples)
                 # Or could be the start of a *new* block if requirements change
                 break 
        elif in_block:
            # Found a zero after starting a block, the block ends at the previous index
            break
            
    if start_index != -1:
        return start_index, end_index, value
    else:
        # No non-zero block found
        return -1, -1, 0

def transform(input_str):
    """
    Transforms the input sequence string by shifting the non-zero block.

    Args:
        input_str: A string representing a space-separated sequence of integers.

    Returns:
        A string representing the transformed space-separated sequence.
    """
    # Parse the input string into a list of integers
    try:
        input_list = [int(x) for x in input_str.split()]
    except ValueError:
        # Handle potential errors if input is not formatted correctly
        print("Error: Input string contains non-integer values.")
        return "" # Or raise an exception

    list_len = len(input_list)
    
    # Initialize the output list with zeros
    output_list = [0] * list_len

    # Find the non-zero block in the input list
    start_index, end_index, value = find_non_zero_block(input_list)

    # If a block was found, proceed with the shift
    if start_index != -1:
        # Calculate the length of the block
        block_length = end_index - start_index + 1
        
        # Calculate the new starting position for the block
        new_start_index = start_index + 2

        # Place the block into the output list at the new position
        for i in range(block_length):
            target_index = new_start_index + i
            # Ensure the target index is within the bounds of the list
            if 0 <= target_index < list_len:
                output_list[target_index] = value
            # If the shift pushes part of the block beyond the end, it's truncated (based on examples)

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))

    return output_str
