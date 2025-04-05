import math
import re

"""
Transforms a sequence of digits by finding the first contiguous block of non-zero digits, 
shifting this block 3 positions to the left (or to the beginning if the shift exceeds the boundary), 
and padding the remaining positions with zeros. The sequence length remains constant.
"""

def _find_first_non_zero_block(sequence):
    """
    Finds the start and end indices of the first contiguous block of non-zero numbers.

    Args:
        sequence: A list of integers.

    Returns:
        A tuple (start_index, end_index) if a block is found, otherwise (None, None).
        end_index is the index *after* the last non-zero digit in the block.
    """
    start_index = -1
    # Find the start of the block
    for i, digit in enumerate(sequence):
        if digit != 0:
            start_index = i
            break
            
    # If no non-zero digit was found
    if start_index == -1:
        return None, None
        
    # Find the end of the block (the first zero *after* the start, or end of list)
    end_index = len(sequence) # Default to end of list if no zero follows
    for i in range(start_index + 1, len(sequence)):
        if sequence[i] == 0:
            end_index = i
            break
            
    return start_index, end_index

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string sequence of digits.

    Args:
        input_str: A space-separated string of digits.

    Returns:
        A space-separated string of digits representing the transformed sequence.
    """
    # 1. Identify the input sequence of digits.
    # Convert string to list of integers
    input_list = [int(d) for d in input_str.split()]
    n = len(input_list)
    
    # 2. Locate the starting index of the first non-zero digit.
    # 3. Locate the ending index of the contiguous block.
    start_index, end_index = _find_first_non_zero_block(input_list)
    
    # If no non-zero digits exist, the sequence remains unchanged.
    if start_index is None:
        return input_str # Or " ".join(['0'] * n) if guaranteed output format needed

    # 4. Extract this contiguous block of non-zero digits.
    non_zero_block = input_list[start_index:end_index]
    
    # 5. Calculate the target starting index for this block in the output sequence.
    # Subtract 3 from its original starting index. 
    # If the result is negative, use 0 as the target starting index.
    target_start_index = max(0, start_index - 3)
    
    # 6. Construct the output sequence.
    # Initialize the output sequence with all zeros.
    output_list = [0] * n
    
    # Place the extracted non-zero block into the output sequence.
    block_len = len(non_zero_block)
    # Ensure the block doesn't write past the end of the list (though it shouldn't with fixed length)
    target_end_index = min(n, target_start_index + block_len)
    # Adjust block if placement would exceed list bounds (only relevant if target_end_index calculation was different)
    block_to_place = non_zero_block[:target_end_index - target_start_index] 
    
    output_list[target_start_index:target_end_index] = block_to_place
    
    # 7. Format the resulting sequence of digits into a space-separated string.
    output_str = " ".join(map(str, output_list))
    
    return output_str
