"""
Identifies a contiguous block of identical non-zero integers in the input list.
Shifts this block to the right by a distance equal to its length.
The original positions of the block are replaced with zeros.
The output list has the same length as the input list.
"""

# No external libraries are required for this transformation.

def transform(input_list):
    """
    Transforms the input list by shifting a contiguous block of non-zero numbers.

    Args:
        input_list: A list of integers, expected to contain zeros and one
                    contiguous block of identical non-zero integers.

    Returns:
        A new list of integers representing the transformed state, or a copy
        of the input list if no non-zero block is found.
    """

    # Initialize variables to track the block properties
    start_index = -1
    block_value = 0
    block_length = 0
    list_len = len(input_list) # Cache list length for efficiency

    # --- Step 1: Identify the Object ---
    # Iterate through the input list to find the contiguous block of non-zero integers.
    # Record its starting index, value, and length.
    for i, val in enumerate(input_list):
        if val != 0:
            # Found a non-zero value
            if start_index == -1:
                # This is the first non-zero element found, marking the start of the block
                start_index = i
                block_value = val
                block_length = 1
            elif val == block_value:
                # This non-zero value matches the block's value, extend the block length
                block_length += 1
            else:
                 # Found a non-zero value different from the current block.
                 # Based on the problem constraints (single block), this signifies the end.
                 # Break here assumes the block definition is strict.
                break
        elif start_index != -1:
            # Found a zero after the block has started. This marks the end of the block.
            break
        # If val is 0 and start_index is -1, continue scanning for the block's start.

    # Handle the case where no non-zero block is found in the input list.
    if start_index == -1:
        # Return a copy of the original list as there is nothing to transform.
        return list(input_list)

    # --- Step 2: Calculate Shift Distance ---
    # The distance the block needs to shift is equal to its length.
    shift_distance = block_length

    # --- Step 3: Create Output Sequence ---
    # Initialize a new list of the same size as the input, filled with zeros.
    output_list = [0] * list_len

    # --- Step 4: Place Shifted Object ---
    # Calculate the starting index for the block in the output list.
    new_start_index = start_index + shift_distance

    # Copy the block's value into the output list at the calculated new position.
    # Iterate 'block_length' times to place each element of the block.
    for i in range(block_length):
        # Calculate the target index in the output list for the current element.
        write_index = new_start_index + i

        # Check if the target index is within the bounds of the output list.
        if write_index < list_len:
            # Place the block's value at the valid target index.
            output_list[write_index] = block_value
        # If write_index is out of bounds (>= list_len), the element is shifted
        # off the end of the list and is effectively dropped, which matches
        # the behavior implicitly shown in the examples (no wrap-around).

    # --- Step 5: Return Output ---
    # Return the newly constructed list containing the shifted block.
    return output_list