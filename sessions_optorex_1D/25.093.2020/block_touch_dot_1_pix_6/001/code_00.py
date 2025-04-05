import re

"""
Identifies the unique pivot digit '2'. Finds contiguous blocks of identical non-zero digits. 
If a block is found adjacent to a '0' on the side away from the pivot ('2'), 
the block shifts one position towards the pivot, replacing the adjacent '0' with the block's digit 
and leaving a '0' at the trailing edge of the original block position. 
Only one such shift occurs per transformation. If no block meets the shift condition, 
the input remains unchanged.
"""

def parse_input(input_str):
    """Converts the input string "0 1 1 0 2" to a list [0, 1, 1, 0, 2]."""
    return [int(d) for d in input_str.split()]

def format_output(output_list):
    """Converts the list [0, 1, 1, 0, 2] to the output string "0 1 1 0 2"."""
    return " ".join(map(str, output_list))

def find_pivot(grid):
    """Finds the index of the pivot element '2'."""
    try:
        return grid.index(2)
    except ValueError:
        return -1 # Pivot not found

def find_blocks(grid):
    """Finds contiguous blocks of identical non-zero digits."""
    blocks = []
    n = len(grid)
    i = 0
    while i < n:
        if grid[i] != 0 and grid[i] != 2:
            digit = grid[i]
            start_index = i
            j = i
            while j < n and grid[j] == digit:
                j += 1
            end_index = j - 1
            blocks.append({'start': start_index, 'end': end_index, 'digit': digit})
            i = j # Continue scan after the block
        else:
            i += 1
    return blocks

def transform(input_str):
    """
    Applies the block shifting transformation based on the pivot '2'.

    Args:
        input_str: A string representing the 1D sequence of digits separated by spaces.

    Returns:
        A string representing the transformed 1D sequence, or the original
        string if no transformation occurs.
    """
    # Parse the input string into a list of integers
    input_grid = parse_input(input_str)
    output_grid = list(input_grid) # Start with a copy
    n = len(output_grid)

    # 1. Identify the position of the unique digit '2'
    pivot_index = find_pivot(output_grid)
    if pivot_index == -1:
        # No pivot found, return original grid (as per observed behavior)
        return input_str 

    # 2. Scan the sequence to find all contiguous blocks of identical non-zero digits
    blocks = find_blocks(output_grid)

    target_block = None
    shift_direction = None # 'left' or 'right'

    # 3. For each block found, check if it can be shifted
    for block in blocks:
        start, end, digit = block['start'], block['end'], block['digit']

        # a. Determine if the block is to the left or right of '2'
        if start > pivot_index:
            # b. Block is to the right of '2'
            # Check if the cell immediately preceding the block contains a '0'
            if start > 0 and output_grid[start - 1] == 0:
                target_block = block
                shift_direction = 'left' # Shift towards the pivot
                break # Only one shift allowed
        elif end < pivot_index:
             # c. Block is to the left of '2'
             # Check if the cell immediately following the block contains a '0'
             if end < n - 1 and output_grid[end + 1] == 0:
                 target_block = block
                 shift_direction = 'right' # Shift towards the pivot
                 break # Only one shift allowed

    # 4. If a target block for shifting was identified, perform the shift
    if target_block:
        start, end, digit = target_block['start'], target_block['end'], target_block['digit']
        if shift_direction == 'left':
            # a. Shift block left (towards pivot)
            output_grid[start - 1] = digit # Replace '0' before the block
            output_grid[end] = 0           # Leave '0' at the original end
        elif shift_direction == 'right':
            # b. Shift block right (towards pivot)
            output_grid[end + 1] = digit   # Replace '0' after the block
            output_grid[start] = 0         # Leave '0' at the original start

    # 5. If no target block was identified, output_grid remains the same as input_grid

    # Format the list back into a space-separated string
    return format_output(output_grid)