"""
Transforms an input grid based on the following process:
1. Create a copy of the input grid to serve as the initial output grid.
2. Examine each column of the input grid. Identify all columns where every pixel is white (color 0).
3. Group adjacent "all-white" columns into contiguous blocks. Record the start column index, end column index, and width for each block.
4. If no "all-white" columns were found (and thus no blocks exist), return the unmodified output grid (the copy of the input).
5. If blocks were found, determine the maximum width among all identified blocks.
6. Select the "target block":
    a. Consider only the blocks that have the maximum width found in the previous step.
    b. Among these maximum-width blocks, choose the one that appears furthest to the left (i.e., the one with the smallest starting column index).
7. Modify the output grid: Change the color of all pixels located within the column range of the target block (from its start column index to its end column index, inclusive) and covering all rows (from row 0 to the grid height minus 1) to green (color 3). Pixels outside this rectangular region remain unchanged from the initial copy.
8. Return the modified output grid.
"""

import numpy as np

def find_widest_leftmost_white_block(grid: np.ndarray) -> tuple[int | None, int | None]:
    """
    Finds the start and end column indices of the widest contiguous block 
    of columns that contain only white pixels (0). If there's a tie in width,
    it selects the leftmost block.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: A tuple (start_col, end_col) representing the inclusive indices 
               of the selected block, or (None, None) if no all-white columns are found.
    """
    height, width = grid.shape
    if height == 0 or width == 0: 
        return None, None
        
    # Step 2: Determine which columns are entirely white (0)
    is_col_white = [np.all(grid[:, c] == 0) for c in range(width)]

    max_width = 0
    best_start_col = -1
    
    current_start_col = -1
    current_width = 0

    # Step 3: Iterate through columns to find contiguous blocks of white columns
    for c in range(width):
        if is_col_white[c]:
            # If this is the start of a new block of white columns
            if current_width == 0: 
                current_start_col = c
            current_width += 1
        else: # End of a block (or not in one)
            if current_width > 0: # We just finished a block
                # Step 5 & 6: Check if this block is the widest found so far.
                # The ">" comparison ensures that if a later block has the same width, 
                # the earlier (leftmost) one is kept.
                if current_width > max_width:
                    max_width = current_width
                    best_start_col = current_start_col
                # Reset for the next potential block
                current_width = 0 
                current_start_col = -1

    # After the loop, check if the grid ended with a white block
    if current_width > 0:
        if current_width > max_width:
            max_width = current_width
            best_start_col = current_start_col

    # Step 4 (implicit): If a block was found, return its start and end columns
    if best_start_col != -1:
        # Calculate end column based on start and width
        best_end_col = best_start_col + max_width - 1
        return best_start_col, best_end_col
    else:
        # No all-white columns found
        return None, None

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation described in the module docstring.
    Finds the widest, leftmost block of all-white columns and fills it entirely green.
    """
    # Step 1: Initialize output_grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    
    # Steps 2, 3, 5, 6: Find the widest, leftmost contiguous block of purely white columns.
    C_start, C_end = find_widest_leftmost_white_block(input_grid)

    # Step 4: If no such block exists, return the original grid copy.
    if C_start is None:
        return output_grid 

    # Step 7: Modify the output grid: fill the target block with green (3).
    # Use numpy slicing: all rows (':'), columns from C_start up to (but not including) C_end + 1.
    output_grid[:, C_start : C_end + 1] = 3
        
    # Step 8: Return the modified grid.
    return output_grid