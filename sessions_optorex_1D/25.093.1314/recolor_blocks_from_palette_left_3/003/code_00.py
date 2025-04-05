import math # common libraries available
import re # common libraries available

"""
Transforms an input sequence of 12 integers. It identifies the first two 
contiguous blocks of the integer '5' within the first 10 elements (indices 0-9). 
The first block found is replaced element-wise by the value at index 10 of the input sequence. 
The second block found (if any) is replaced element-wise by the value at index 11 of the input sequence. 
Elements outside these blocks or outside the first 10 indices remain unchanged, 
including the values at indices 10 and 11.
"""

def find_contiguous_blocks(sequence, target, length):
    """
    Finds contiguous blocks of the target value within the specified length of the sequence.

    Args:
        sequence: The list of integers to search within.
        target: The integer value to find blocks of.
        length: The number of elements from the start of the sequence to search (exclusive index).

    Returns:
        A list of tuples, where each tuple represents a block and contains
        the (start_index, end_index_exclusive) of the block. Blocks are ordered
        by their start_index. Returns an empty list if no blocks are found.
    """
    blocks = []
    in_block = False
    start_index = -1
    # Iterate through the specified prefix of the sequence
    for i in range(length):
        is_target = sequence[i] == target
        
        # Detect the start of a new block of the target value
        if is_target and not in_block:
            in_block = True
            start_index = i
        # Detect the end of the current block (when a non-target is found after being in a block)
        elif not is_target and in_block:
            in_block = False
            blocks.append((start_index, i)) # end index is exclusive
            start_index = -1 # Reset start index for the next potential block

    # If a block was still ongoing when the loop finished (i.e., ended at the 'length' boundary)
    if in_block:
        blocks.append((start_index, length)) # The end index is the exclusive boundary 'length'

    return blocks

def transform(input_list):
    """
    Applies the transformation rule to the input list.

    Args:
        input_list: A list of 12 integers.

    Returns:
        A new list of 12 integers with block replacements applied, or the original 
        list if the input is not a list of length 12.
    """
    
    # --- Configuration ---
    list_length = 12
    target_value = 5
    modification_range_end_exclusive = 10
    replacement_value_1_index = 10
    replacement_value_2_index = 11

    # --- Input Validation ---
    if not isinstance(input_list, list) or len(input_list) != list_length:
        # Consider raising an error or returning None depending on requirements
        print(f"Warning: Input must be a list of {list_length} integers.")
        return input_list # Return original input if invalid

    # --- Initialization ---
    # Create a copy of the input sequence to serve as the working output sequence.
    output_list = list(input_list) 

    # --- Extract Replacement Values ---
    # Identify the first replacement value (val1) from the element at index 10.
    replacement_value_1 = input_list[replacement_value_1_index]
    # Identify the second replacement value (val2) from the element at index 11.
    replacement_value_2 = input_list[replacement_value_2_index]

    # --- Find Target Blocks ---
    # Scan the sequence within the modification range [0, modification_range_end_exclusive) 
    # to find all contiguous blocks of the target_value.
    blocks_found = find_contiguous_blocks(output_list, target_value, modification_range_end_exclusive)

    # --- Apply Replacements ---
    # If one or more blocks were found:
    if len(blocks_found) >= 1:
        # Select the first block found.
        start_index_1, end_index_1 = blocks_found[0]
        # Replace all elements within this first block's index range with replacement_value_1.
        for i in range(start_index_1, end_index_1):
            output_list[i] = replacement_value_1

    # If two or more blocks were found:
    if len(blocks_found) >= 2:
        # Select the second block found.
        start_index_2, end_index_2 = blocks_found[1]
        # Replace all elements within this second block's index range with replacement_value_2.
        for i in range(start_index_2, end_index_2):
            output_list[i] = replacement_value_2
            
    # --- Return Result ---
    # Return the modified output sequence.
    return output_list