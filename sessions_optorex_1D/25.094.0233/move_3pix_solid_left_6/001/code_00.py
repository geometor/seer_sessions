"""
Transforms an input sequence of digits by identifying a contiguous block of non-zero digits and shifting this block 3 positions to the left. The sequence length remains constant, and positions outside the newly placed block are filled with zeros.
"""

import math # Using math as a placeholder for potential future needs, not used currently.
# No specific complex libraries needed for this task.

def find_nonzero_block(seq):
    """
    Finds the contiguous block of non-zero digits in a sequence.

    Args:
        seq: A list of integers.

    Returns:
        A tuple containing:
        - list: The block of non-zero digits.
        - int: The starting index of the block in the original sequence.
               Returns -1 if no non-zero block is found.
    """
    start_index = -1
    block = []
    in_block = False
    for i, val in enumerate(seq):
        if val != 0:
            if not in_block:
                start_index = i
                in_block = True
            block.append(val)
        elif in_block:
            # Found a zero after the block started, so the block ends here.
            break
    # If the loop finishes while still in_block, the block goes to the end.
    
    # If no non-zero element was ever found, start_index remains -1
    if not in_block:
        start_index = -1
        
    return block, start_index

def transform(input_str):
    """
    Applies the block-shifting transformation to the input string.

    Args:
        input_str: A string representing a space-separated sequence of digits.

    Returns:
        A string representing the transformed space-separated sequence of digits.
    """
    # 1. Parse the input string into a list of integers.
    input_list = [int(x) for x in input_str.split()]
    n = len(input_list)

    # 2. Find the non-zero block and its starting position.
    block, start_index = find_nonzero_block(input_list)

    # Handle the case where no non-zero block is found (though not present in examples)
    # If no block is found, return the original string or an appropriately formatted zero string.
    # Based on examples, a block always exists.
    if start_index == -1:
        # Assuming default behavior is to return all zeros if no block found,
        # matching the output structure.
         return " ".join(['0'] * n) 

    # 3. Calculate the new starting index for the block (shift left by 3).
    new_start_index = start_index - 3

    # 4. Initialize the output list with zeros.
    output_list = [0] * n

    # 5. Place the identified block into the output list at the new position.
    # Iterate through the elements of the found block.
    for i in range(len(block)):
        # Calculate the target index in the output list.
        output_index = new_start_index + i
        
        # Place the block element only if the target index is within the bounds of the list.
        # Elements shifted beyond the start (index < 0) are effectively dropped.
        if 0 <= output_index < n:
            output_list[output_index] = block[i]
        # Elements that would extend beyond the end if the block started near the end 
        # would also be dropped, but the shift is leftwards, making this less likely 
        # unless the original block itself was very long and started near the beginning.

    # 6. Format the output list back into a space-separated string.
    output_str = " ".join(map(str, output_list))

    return output_str