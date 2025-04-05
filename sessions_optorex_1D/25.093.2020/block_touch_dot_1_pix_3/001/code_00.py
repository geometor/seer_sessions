import re

"""
The transformation rule identifies a single, stationary pivot digit '2' within a sequence of 12 digits. 
It then locates the first contiguous block of non-zero digits (excluding the pivot '2').
If this block is located entirely to the left of the pivot '2', and there is a '0' immediately to the right of the block, the block is shifted one position to the right, swapping places with that '0'.
If the block is located entirely to the right of the pivot '2', and there is a '0' immediately to the left of the block, the block is shifted one position to the left, swapping places with that '0'.
The pivot '2' and any other '0's remain in their positions unless directly involved in the swap.
The output is the modified sequence of digits, formatted as a space-separated string.
"""

def parse_input(input_str: str) -> list[int]:
    """Converts the space-separated input string into a list of integers."""
    return [int(d) for d in input_str.split()]

def format_output(output_list: list[int]) -> str:
    """Converts the list of integers back into a space-separated string."""
    return " ".join(map(str, output_list))

def find_pivot_index(grid: list[int]) -> int:
    """Finds the index of the pivot digit '2'."""
    try:
        return grid.index(2)
    except ValueError:
        # Should not happen based on problem description, but good practice
        return -1 

def find_movable_block(grid: list[int], pivot_index: int) -> tuple[int | None, int | None]:
    """
    Finds the start and end indices of the first contiguous block of 
    non-zero digits (excluding the pivot '2').
    Returns (None, None) if no such block is found.
    """
    start_index = None
    for i, digit in enumerate(grid):
        if digit != 0 and i != pivot_index:
            # Found the start of a potential block
            start_index = i
            # Find the end of this block
            end_index = i
            for j in range(i + 1, len(grid)):
                if grid[j] == 0 or j == pivot_index:
                    break # Block ends here
                end_index = j
            return start_index, end_index
        
    return None, None # No block found

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.
    
    1. Parses the input string into a list of integers.
    2. Finds the index of the pivot '2'.
    3. Finds the contiguous block of non-zero, non-'2' digits.
    4. Determines if the block is left or right of the pivot.
    5. Checks for an adjacent '0' in the appropriate direction for swapping.
    6. Performs the shift and swap if conditions are met.
    7. Formats the resulting list back into a string.
    """
    # 1. Parse input
    grid = parse_input(input_str)
    output_grid = list(grid) # Work on a copy

    # 2. Find pivot
    pivot_index = find_pivot_index(grid)
    if pivot_index == -1:
        # Handle error case if '2' is not found (though examples imply it's always there)
        return input_str 

    # 3. Find the block to move
    start_index, end_index = find_movable_block(grid, pivot_index)

    # 4. Determine direction and perform shift/swap if possible
    if start_index is not None and end_index is not None:
        block_content = grid[start_index : end_index + 1]
        
        # 4a. Block is to the left of the pivot
        if end_index < pivot_index:
            # Check if a swap to the right is possible
            swap_pos = end_index + 1
            if swap_pos < len(grid) and grid[swap_pos] == 0:
                # Perform right shift: place 0 at start, block at start+1
                output_grid[start_index] = 0
                output_grid[start_index + 1 : end_index + 2] = block_content
                
        # 4b. Block is to the right of the pivot
        elif start_index > pivot_index:
            # Check if a swap to the left is possible
            swap_pos = start_index - 1
            if swap_pos >= 0 and grid[swap_pos] == 0:
                 # Perform left shift: place 0 at end, block at start-1
                 output_grid[end_index] = 0
                 output_grid[start_index - 1 : end_index] = block_content

    # 7. Format output
    return format_output(output_grid)
