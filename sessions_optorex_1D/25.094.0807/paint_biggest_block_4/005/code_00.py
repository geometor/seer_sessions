"""
Transforms an input sequence of integers by identifying the longest contiguous block
of non-zero numbers (selecting the earliest one based on start index in case of ties)
and changing all numbers within that specific block to 1. Zeros and numbers in other
non-zero blocks remain unchanged. The input can be a list or a 1D NumPy array, 
and the output is returned in the same format.
"""

import numpy as np

# Helper function to find non-zero blocks
def find_nonzero_blocks(int_list):
    """
    Identifies contiguous blocks of non-zero numbers in a list or 1D array.

    Args:
        int_list: A list or 1D NumPy array of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        with keys 'start', 'end', 'length'. Returns an empty list if
        no non-zero numbers are found or the input is empty.
    """
    blocks = []
    if not len(int_list): # Handle empty input
        return blocks
        
    in_block = False
    start_index = -1
    # Ensure processing as a list for consistent indexing and iteration
    processed_list = list(int_list)
    list_len = len(processed_list)

    for i, num in enumerate(processed_list):
        # Ensure the element is treated as an integer, default to 0 if conversion fails
        try:
            current_num = int(num)
        except (ValueError, TypeError):
            current_num = 0 # Treat non-integers/conversion errors as 0

        if current_num != 0 and not in_block:
            # Start of a new block
            in_block = True
            start_index = i
        elif (current_num == 0 or i == list_len - 1) and in_block:
            # End of the current block (either a zero is encountered or it's the end of the list)
            end_index = i - 1 if current_num == 0 else i # Adjust end index based on cause
            # Check for valid block indices before appending
            if start_index <= end_index :
                 blocks.append({
                    'start': start_index,
                    'end': end_index,
                    'length': end_index - start_index + 1
                 })
            in_block = False
            # No need to reset start_index here, handled by the start condition

    return blocks

# Helper function to select the target block
def find_target_block(blocks):
    """
    Selects the target block based on maximum length, then earliest start index.

    Args:
        blocks: A list of block dictionaries (from find_nonzero_blocks).

    Returns:
        The dictionary representing the target block, or None if blocks is empty.
    """
    if not blocks:
        return None

    # Find the maximum length using max() with a generator expression
    try:
        max_length = max(block['length'] for block in blocks)
    except ValueError: # Should only happen if blocks is unexpectedly empty after the initial check
        return None

    # Filter blocks with maximum length
    max_length_blocks = [block for block in blocks if block['length'] == max_length]

    # Find the block among the longest ones with the minimum start index
    # Using min() with a key function is efficient
    target_block = min(max_length_blocks, key=lambda x: x['start'])

    return target_block

def transform(input_grid):
    """
    Applies the transformation logic to the input sequence.
    """
    # Determine input type to return the same type later
    is_numpy = isinstance(input_grid, np.ndarray)
    original_dtype = input_grid.dtype if is_numpy else None

    # Work with a mutable list copy for modifications
    if is_numpy:
        output_list = input_grid.tolist()
    else:
        # Ensure it's a list and make a copy to avoid modifying the original input
        output_list = list(input_grid) 

    # Step 1: Identify all contiguous blocks of non-zero numbers
    blocks = find_nonzero_blocks(output_list) # Pass the list copy

    # Step 2 & 3: Find and Select the Target Block (longest, then earliest)
    target_block = find_target_block(blocks)

    # Step 4 & 5: Modify the output list based on the target block
    if target_block:
        # Get the start and end indices of the target block
        start = target_block['start']
        end = target_block['end']
        
        # Iterate through the indices within the target block
        for i in range(start, end + 1):
            # Change the value at this position in the output list to 1
            output_list[i] = 1
    
    # Step 6: Convert back to NumPy array if the input was a NumPy array, preserving dtype
    if is_numpy:
        output_grid = np.array(output_list, dtype=original_dtype)
    else:
        # Otherwise, the modified list is the result
        output_grid = output_list

    # Step 7: Return the final transformed grid
    return output_grid