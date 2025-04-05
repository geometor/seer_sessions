import copy

"""
Transforms a 1D sequence (represented as a list of integers) based on a pivot '2'. 
It identifies the unique pivot digit '2' and the single contiguous block of identical non-zero digits 
(excluding '2'). If this block is found adjacent to a '0' on the side *away* from the pivot ('2'), 
the block shifts one position towards the pivot. This shift involves replacing the adjacent '0' with 
the block's digit and setting the cell at the original trailing edge of the block 
(leftmost for a right shift, rightmost for a left shift) to '0'. If no block is 
found, the pivot is missing, or the adjacency condition is not met, the input 
sequence remains unchanged. The function returns the transformed list.
"""

# Helper functions

def find_pivot(grid_list):
    """Finds the index of the pivot element '2' in a list."""
    try:
        # Use list.index() method
        return grid_list.index(2)
    except ValueError:
        return -1 # Pivot not found

def find_block(grid_list):
    """
    Finds the single contiguous block of identical non-zero, non-pivot digits in a list.
    Returns a dictionary {'start': int, 'end': int, 'digit': int} or None.
    Assumes only one such block exists based on examples.
    """
    n = len(grid_list)
    found_block = None
    i = 0
    while i < n:
        # Check for a digit that is not 0 and not the pivot 2
        if grid_list[i] != 0 and grid_list[i] != 2:
            digit = grid_list[i]
            start_index = i
            j = i
            # Find the end of the contiguous block of this digit
            while j < n and grid_list[j] == digit:
                j += 1
            end_index = j - 1
            # Store block info - assuming only one block needs to be found
            found_block = {'start': start_index, 'end': end_index, 'digit': digit}
            break # Stop searching after finding the first block
        else:
            i += 1
    return found_block

# Main transformation function

def transform(input_grid):
    """
    Applies the block shifting transformation based on the pivot '2'.

    Args:
        input_grid: A list of integers representing the 1D sequence.

    Returns:
        A list representing the transformed sequence, or a copy of
        the original sequence (as a list) if no transformation occurs.
    """
    # Initialize output_grid as a deep copy of the input list
    output_grid = copy.deepcopy(input_grid)
    n = len(output_grid)

    # 1. Identify Pivot: Find the index (position) of the unique digit '2'.
    pivot_index = find_pivot(output_grid)
    
    # If '2' is not found, the sequence remains unchanged.
    if pivot_index == -1:
        return output_grid

    # 2. Identify Block: Scan the sequence to find the single contiguous block.
    block = find_block(output_grid)
    
    # If no such block is found, the sequence remains unchanged.
    if not block:
        return output_grid

    # Extract block details
    start, end, digit = block['start'], block['end'], block['digit']

    # 3. Check Shift Condition: Determine block position relative to pivot and check adjacency.
    
    # a. Determine if the block is to the left or right of the pivot.
    
    # b. Handle block to the right of the pivot
    if start > pivot_index:
        # Check if the cell immediately to the *left* (away from pivot) is '0'.
        if start > 0 and output_grid[start - 1] == 0:
            # 4. Perform Transformation (Leftward Shift)
            # i. Change the value at `start_index - 1` to the block's digit.
            output_grid[start - 1] = digit 
            # ii. Change the value at the block's original `end_index` to '0'.
            output_grid[end] = 0           
            
    # c. Handle block to the left of the pivot
    elif end < pivot_index:
        # Check if the cell immediately to the *right* (away from pivot) is '0'.
        if end < n - 1 and output_grid[end + 1] == 0:
            # 4. Perform Transformation (Rightward Shift)
            # i. Change the value at `end_index + 1` to the block's digit.
            output_grid[end + 1] = digit   
            # ii. Change the value at the block's original `start_index` to '0'.
            output_grid[start] = 0         

    # 5. No Transformation: If neither shift condition was met, output_grid remains unchanged.
    
    # 6. Return Output: Return the final (potentially modified) output list.
    return output_grid