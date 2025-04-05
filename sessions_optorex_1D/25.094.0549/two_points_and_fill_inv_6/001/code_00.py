import re

"""
Transforms a sequence of digits based on contiguous blocks of identical non-zero digits.
If a block's length is greater than 2, only the first and last elements of the block 
are kept, and the elements between them are changed to 0. Blocks of length 1 or 2, 
and all zero elements, remain unchanged.
"""

def transform(input_str: str) -> str:
    """
    Applies the block transformation rule to the input sequence.

    Args:
        input_str: A string of space-separated integers.

    Returns:
        A string of space-separated integers representing the transformed sequence.
    """
    # Parse the input string into a list of integers
    input_list = list(map(int, input_str.split()))
    n = len(input_list)
    
    # Initialize output_list as a copy of the input list
    # The transformation will modify this list in place based on blocks found in the input
    output_list = list(input_list) 

    # Iterate through the input list to find blocks of identical non-zero numbers
    i = 0
    while i < n:
        current_val = input_list[i]
        
        # Check if the current element is non-zero
        if current_val != 0:
            # Found the potential start of a block
            start_index = i
            
            # Find the end of the contiguous block of the same non-zero value
            j = i
            while j + 1 < n and input_list[j + 1] == current_val:
                j += 1
            end_index = j
            
            # Calculate the length of the block
            block_length = end_index - start_index + 1
            
            # Apply the transformation rule based on block length
            if block_length > 2:
                # If block length is greater than 2, zero out the middle elements in the output list
                for k in range(start_index + 1, end_index):
                    output_list[k] = 0
            # Else (block_length <= 2): No change needed, as output_list was initialized as a copy.
            
            # Advance the main loop index past the processed block
            i = end_index + 1
        else:
            # If the current element is 0, just move to the next element
            i += 1
            
    # Format the output list back into a space-separated string
    output_str = ' '.join(map(str, output_list))
    
    return output_str
