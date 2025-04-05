import math

def find_nonzero_blocks(int_list):
    """
    Identifies contiguous blocks of non-zero numbers in a list.

    Args:
        int_list: A list of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        with keys 'start', 'end', 'length'. Returns an empty list if
        no non-zero numbers are found.
    """
    blocks = []
    in_block = False
    start_index = -1
    for i, num in enumerate(int_list):
        if num != 0 and not in_block:
            # Start of a new block
            in_block = True
            start_index = i
        elif num == 0 and in_block:
            # End of the current block
            end_index = i - 1
            blocks.append({
                'start': start_index,
                'end': end_index,
                'length': end_index - start_index + 1
            })
            in_block = False
            start_index = -1
    # Handle case where a block runs to the end of the list
    if in_block:
        end_index = len(int_list) - 1
        blocks.append({
            'start': start_index,
            'end': end_index,
            'length': end_index - start_index + 1
        })
    return blocks

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

    # Find the maximum length
    max_length = 0
    for block in blocks:
        if block['length'] > max_length:
            max_length = block['length']

    # Filter blocks with maximum length
    max_length_blocks = [block for block in blocks if block['length'] == max_length]

    # If only one block has max length, return it
    if len(max_length_blocks) == 1:
        return max_length_blocks[0]

    # If multiple blocks share max length, find the one with the smallest start index
    target_block = max_length_blocks[0]
    for block in max_length_blocks[1:]:
        if block['start'] < target_block['start']:
            target_block = block
    
    return target_block

def transform(input_str):
    """
    Transforms the input sequence by identifying the longest contiguous block
    of non-zero numbers (selecting the earliest one in case of ties) and
    changing all numbers within that block to 1. Zeros and numbers in other
    non-zero blocks remain unchanged.

    Args:
        input_str: A string of space-separated single-digit integers.

    Returns:
        A string of space-separated single-digit integers representing the
        transformed sequence.
    """
    # --- Step 0: Parse input ---
    # Convert the input string into a list of integers
    input_list = [int(x) for x in input_str.split()]

    # --- Step 1: Identify non-zero blocks ---
    # Find all contiguous blocks of non-zero numbers
    blocks = find_nonzero_blocks(input_list)

    # --- Step 2 & 3: Find and Select Target Block ---
    # Determine the target block (longest, then earliest)
    target_block = find_target_block(blocks)

    # --- Step 4 & 5: Modify Output ---
    # Initialize the output list as a copy of the input
    output_list = list(input_list)

    # If a target block was found, modify the output list
    if target_block:
        start = target_block['start']
        end = target_block['end']
        # Iterate through the indices of the target block
        for i in range(start, end + 1):
            # Change the value at this position to 1
            output_list[i] = 1

    # --- Step 6 & 7: Format and Return Output ---
    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))
    return output_str
