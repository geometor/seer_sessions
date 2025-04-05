```python
import re # Used for finding the block efficiently, though iteration also works

"""
Identify the contiguous block of non-zero integers in the input sequence. 
Shift this block 4 positions to the right. 
Fill the remaining positions with zeros to maintain the original sequence length.
"""

def find_non_zero_block(int_list):
    """
    Finds the start index, end index, and value of the first contiguous non-zero block.

    Args:
        int_list: A list of integers.

    Returns:
        A tuple (start_index, end_index, value) if a block is found,
        otherwise (None, None, None).
    """
    start_index = -1
    end_index = -1
    value = None
    for i, x in enumerate(int_list):
        if x != 0:
            if start_index == -1: # First non-zero found
                start_index = i
                value = x
            # Check if the value is consistent with the block
            elif x != value: 
                # This handles cases if there were multiple different non-zero blocks
                # Based on examples, we only expect one type. We stop at the first block end.
                break 
            end_index = i # Update end index as long as we see the same non-zero value
        elif start_index != -1: # We found a zero after starting a block
            break # End of the block
            
    if start_index != -1:
        return start_index, end_index, value
    else:
        return None, None, None


def transform(input_str):
    """
    Transforms the input sequence string by shifting the non-zero block.

    Args:
        input_str: A string representing a space-separated sequence of integers.

    Returns:
        A string representing the transformed space-separated sequence.
    """
    # Parse the input string into a list of integers.
    input_list = [int(x) for x in input_str.split()]
    n = len(input_list)

    # Initialize the output list with zeros.
    output_list = [0] * n

    # Identify the contiguous block of non-zero integers.
    start_index, end_index, value = find_non_zero_block(input_list)

    # If no block is found (e.g., all zeros), return the original (or all zeros)
    if start_index is None:
        # Based on examples, a block always exists. If not, returning 
        # the input as a string of zeros might be appropriate.
        # For now, stick to the pattern seen.
        return " ".join(map(str, output_list)) 

    # Calculate the length of the block.
    block_length = end_index - start_index + 1

    # Calculate the new starting index by adding 4.
    new_start_index = start_index + 4
    
    # Place the identified block into the new list at the shifted position.
    # Iterate for the length of the block starting from the new position.
    for i in range(block_length):
        current_output_index = new_start_index + i
        # Ensure we don't write past the end of the list
        if current_output_index < n:
            output_list[current_output_index] = value

    # Format the new list back into a space-separated string.
    output_str = " ".join(map(str, output_list))

    return output_str
```