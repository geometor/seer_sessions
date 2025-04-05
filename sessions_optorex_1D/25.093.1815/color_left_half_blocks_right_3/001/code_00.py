import math

"""
Transforms a sequence of digits based on the following rule:
Iterate through the input sequence. Identify contiguous blocks of the digit '2'. 
For each block of '2's that starts either at the beginning of the sequence or immediately follows a '0', 
calculate the length 'L' of the block. Change the first 'floor(L / 2)' digits 
in that block from '2' to '8' in the output sequence. All other digits ('0's and 
'2's not part of the modified segment of such a block) remain unchanged.
"""

def parse_input(input_str: str) -> list[int]:
    """Converts a space-separated string of digits into a list of integers."""
    return [int(digit) for digit in input_str.split()]

def format_output(output_list: list[int]) -> str:
    """Converts a list of integers back into a space-separated string."""
    return " ".join(map(str, output_list))

def find_block_end(input_list: list[int], start_index: int, value_to_find: int) -> int:
    """Finds the index after the end of a contiguous block of a specific value."""
    current_index = start_index
    while current_index < len(input_list) and input_list[current_index] == value_to_find:
        current_index += 1
    return current_index

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input sequence string.
    """
    input_list = parse_input(input_str)
    n = len(input_list)
    # Initialize output_list as a copy of input_list
    output_list = list(input_list)
    
    i = 0
    while i < n:
        # Check if the current element is '2'
        if input_list[i] == 2:
            # Check if it's the start of a potentially transformable block
            # (either at the beginning of the list or preceded by a '0')
            is_start_of_block = (i == 0) or (input_list[i-1] == 0)
            
            if is_start_of_block:
                # Find the end of the contiguous block of '2's
                block_end_index = find_block_end(input_list, i, 2)
                
                # Calculate the length of the block
                block_length = block_end_index - i
                
                # Calculate the number of '2's to change to '8's
                num_to_change = block_length // 2  # Integer division for floor(L/2)
                
                # Change the first 'num_to_change' elements of the block to '8' in the output
                for j in range(i, i + num_to_change):
                    output_list[j] = 8
                    
                # Advance the main loop index past the processed block
                i = block_end_index
            else:
                # If it's a '2' but not the start of a relevant block, just move to the next element
                # The '2' itself was already copied to output_list during initialization
                i += 1
        else:
            # If the element is '0', just move to the next element
            # The '0' was already copied to output_list during initialization
            i += 1
            
    # Format the output list back into a string
    return format_output(output_list)
