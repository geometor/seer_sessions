import math
import collections

def find_longest_nonzero_block(data):
    """
    Finds the start index and length of the longest contiguous block of non-zero numbers.

    Args:
        data: A list of numbers.

    Returns:
        A tuple (start_index, length) of the longest block. 
        Returns (-1, 0) if no non-zero numbers are found.
    """
    max_len = 0
    best_start = -1
    
    current_start = -1
    current_len = 0
    
    for i, x in enumerate(data):
        if x != 0:
            # If starting a new block
            if current_len == 0:
                current_start = i
            current_len += 1
        else:
            # If a block just ended
            if current_len > 0:
                # Check if this block is the new longest
                if current_len > max_len:
                    max_len = current_len
                    best_start = current_start
                # Reset current block tracking
                current_len = 0
                current_start = -1

    # Check the last block if the list ends with non-zero numbers
    if current_len > 0:
        if current_len > max_len:
            max_len = current_len
            best_start = current_start
            
    return best_start, max_len

def transform(input_grid):
    """
    Identifies the longest contiguous sequence of non-zero integers in the input list 
    and preserves it in the output list, setting all other elements to zero.
    
    Workflow:
    1. Initialize an output list of the same size as the input, filled with zeros.
    2. Find all contiguous blocks of non-zero numbers in the input list.
    3. Determine the block with the maximum length.
    4. If a longest block exists, copy its elements from the input list to the 
       corresponding positions in the output list.
    5. Return the output list.
    """
    
    n = len(input_grid)
    # 1. Initialize output_grid with zeros
    output_grid = [0] * n

    # 2 & 3. Find the longest non-zero block
    start_index, length = find_longest_nonzero_block(input_grid)

    # 4. Copy the longest block to the output grid if found
    if start_index != -1:
        for i in range(length):
            output_grid[start_index + i] = input_grid[start_index + i]

    # 5. Return the modified output grid
    return output_grid
