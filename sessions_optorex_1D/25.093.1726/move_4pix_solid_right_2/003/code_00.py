import collections

"""
Identifies the single contiguous block of identical non-zero digits in a 
12-element input list and shifts this block exactly 4 positions to the right 
to create the output list. All other positions in the output list are zeros.
"""

# No external imports needed beyond standard Python collections/types if necessary.

def find_non_zero_block(input_list):
    """
    Helper function to find the first contiguous block of identical non-zero digits.

    Args:
        input_list: The list of integers to search within.

    Returns:
        A tuple (block_val, start_index, block_length) if a block is found,
        otherwise (None, -1, 0).
    """
    start_index = -1
    block_val = 0
    block_length = 0
    n = len(input_list)

    # Search for the start of the first non-zero sequence
    for i in range(n):
        if input_list[i] != 0:
            start_index = i
            block_val = input_list[i]
            block_length = 1
            # Continue checking for the same value to find the length/end of the block
            for j in range(i + 1, n):
                if input_list[j] == block_val:
                    block_length += 1
                else:
                    # Block ends here as the value changed or became zero
                    break
            # Found the first block, so we can stop the outer search
            break 
            
    if start_index != -1:
        # A block was found
        return block_val, start_index, block_length
    else:
        # No non-zero block found in the input list
        return None, -1, 0

def transform(input_grid):
    """
    Transforms the input grid (list of 12 integers) by identifying the 
    contiguous block of non-zero identical digits and shifting it 4 positions 
    to the right.

    Args:
        input_grid: A list of 12 integers.

    Returns:
        A list of 12 integers representing the transformed grid.
    """
    # Define the fixed parameters based on observations
    sequence_length = 12 
    shift_distance = 4

    # Initialize the output grid with zeros
    output_grid = [0] * sequence_length

    # Step 1: Find the non-zero block in the input grid
    block_val, start_index, block_length = find_non_zero_block(input_grid)

    # Step 2: If a block was successfully found, proceed to shift it
    if block_val is not None: 
        
        # Step 3: Calculate the new starting index for the block in the output grid
        new_start_index = start_index + shift_distance
        
        # Step 4: Place the identified block into the output sequence at the new position
        # Iterate for the determined length of the block
        for i in range(block_length):
            # Calculate the target index in the output grid for the current element of the block
            target_index = new_start_index + i
            
            # Ensure the target index is within the bounds of the output grid
            # (Although based on examples, the shifted block always fits)
            if 0 <= target_index < sequence_length:
                 output_grid[target_index] = block_val
            # else: # Handle edge case if block shifts out of bounds (not observed here)
                 # pass 

    # Step 5: Return the resulting output sequence
    # If no block was found in Step 1, the output_grid remains all zeros, which is correct.
    return output_grid