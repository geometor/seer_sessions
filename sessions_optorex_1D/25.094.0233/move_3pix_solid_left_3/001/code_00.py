import math

def transform(input_list):
    """
    Transforms an input list by shifting a contiguous block of identical non-zero 
    digits three positions to the left, preserving the block's value and length, 
    and padding with zeros elsewhere.

    1. Initialize an output list of the same length as the input list, filled with zeros.
    2. Scan the input list to find the first non-zero element. Record its index 
       (start_index) and its value.
    3. Determine the length of the contiguous block of this non-zero value 
       starting at start_index.
    4. Calculate the new starting index for the block in the output list by 
       subtracting 3 from start_index.
    5. Copy the contiguous block of non-zero numbers from the input into the 
       output list, starting at the calculated new index.
    """

    n = len(input_list)
    output_list = [0] * n  # 1. Initialize output list with zeros

    # Helper function to find the block
    def find_block(data):
        start_index = -1
        block_value = 0
        block_length = 0
        for i, val in enumerate(data):
            if val != 0:
                if start_index == -1: # Found the start of the block
                    start_index = i
                    block_value = val
                    block_length = 1
                elif val == block_value: # Continuing the block
                    block_length += 1
                else: # Should not happen based on task description, but handles unexpected inputs
                    break 
            elif start_index != -1: # Found the end of the block
                break
        return start_index, block_value, block_length

    # 2 & 3. Find the block in the input list
    start_index, block_value, block_length = find_block(input_list)

    # If no block is found, return the list of zeros (though examples always have one)
    if start_index == -1:
        return output_list

    # 4. Calculate the new starting index
    new_start_index = start_index - 3

    # 5. Copy the block to the output list at the new position
    # Ensure indices stay within bounds (although examples don't require explicit checks)
    for i in range(block_length):
        output_index = new_start_index + i
        if 0 <= output_index < n: # Basic boundary check
             output_list[output_index] = block_value

    return output_list