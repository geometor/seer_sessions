```python
import re

def find_non_zero_block(data_list):
    """
    Finds the start and end indices of the first contiguous block of 
    identical non-zero digits.

    Args:
        data_list: A list of strings representing digits.

    Returns:
        A tuple (start_index, end_index) if a block is found, otherwise None.
        Returns (-1, -1) if the block starts at index 0.
    """
    start_index = -1
    end_index = -1
    block_digit = None

    for i, digit in enumerate(data_list):
        if digit != '0':
            # Found the start of a potential block
            if start_index == -1:
                 # Check if block starts at the very beginning
                if i == 0:
                    return -1, -1 # Indicate block starts at index 0
                start_index = i
                block_digit = digit
            # Continue the block if the digit matches
            elif digit == block_digit:
                end_index = i
            # Found a different digit, block ended previously or it's a single digit
            else:
                if end_index == -1: # Handle single non-zero digit case
                    end_index = start_index
                break # Found the end of the first block
        elif start_index != -1:
            # Found a zero after the block started
            if end_index == -1: # Handle single non-zero digit case
                end_index = start_index
            break # End of block

    # Handle case where block goes to the end of the list
    if start_index != -1 and end_index == -1:
        # This handles blocks of size 1 at the end, or longer blocks ending at the list end.
        # Find the actual end of the block if not already set
        current_end = start_index
        for j in range(start_index + 1, len(data_list)):
            if data_list[j] == block_digit:
                current_end = j
            else:
                break
        end_index = current_end


    if start_index != -1 and end_index != -1:
        return start_index, end_index
    elif start_index != -1: # Handles a single non-zero digit not at the start
         return start_index, start_index
    else:
        return None # No non-zero block found


def transform(input_str):
    """
    Transforms the input string by finding the first contiguous block of 
    identical non-zero digits and swapping it with the single zero 
    immediately preceding it. If the block is already at the beginning 
    or no non-zero block exists, the original string is returned.
    """
    # Parse the input string into a list of digit strings.
    input_list = input_str.split(' ')

    # Find the start and end indices of the non-zero block.
    block_indices = find_non_zero_block(input_list)

    # If no block found, return original string
    if block_indices is None:
        return input_str

    start_index, end_index = block_indices

    # If block starts at index 0, return original string
    if start_index == -1:
        return input_str
        
    # Ensure the element before the block is actually '0' (as per pattern)
    # Although find_non_zero_block implies it, good to be explicit/safe
    if start_index == 0 or input_list[start_index - 1] != '0':
         # This case covers blocks starting at index 0 or blocks not preceded by '0'
         # Based on examples, blocks are always preceded by '0' unless at index 0
        return input_str


    # Extract the parts of the list for rearrangement
    prefix = input_list[:start_index - 1]
    preceding_zero = [input_list[start_index - 1]] # Keep as list for concatenation
    non_zero_block = input_list[start_index : end_index + 1]
    suffix = input_list[end_index + 1:]

    # Construct the output list by swapping the preceding zero and the block
    output_list = prefix + non_zero_block + preceding_zero + suffix

    # Join the elements of the output list with spaces
    output_str = ' '.join(output_list)

    return output_str
```