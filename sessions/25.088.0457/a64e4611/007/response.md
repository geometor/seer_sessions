```python
"""
Transforms an input grid based on the following process:
1. Create a copy of the input grid to serve as the initial output grid.
2. Examine each column of the input grid. Identify all columns where every pixel is white (color 0).
3. Group adjacent "all-white" columns into contiguous blocks. Record the start column index and end column index for each block.
4. If no "all-white" columns were found (and thus no blocks exist), return the unmodified output grid (the copy of the input).
5. If one or more blocks were found, select the "target block" which is the one that appears furthest to the left (i.e., the block with the smallest starting column index). Disregard the width of the blocks for selection purposes.
6. Modify the output grid: Change the color of all pixels located within the column range of the target block (from its start column index to its end column index, inclusive) and covering all rows (from row 0 to the grid height minus 1) to green (color 3). Pixels outside this rectangular region remain unchanged from the initial copy.
7. Return the modified output grid.
"""

import numpy as np

def find_leftmost_white_block(grid: np.ndarray) -> tuple[int | None, int | None]:
    """
    Finds the start and end column indices of the leftmost contiguous block 
    of columns that contain only white pixels (0).

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: A tuple (start_col, end_col) representing the inclusive indices 
               of the leftmost block, or (None, None) if no all-white columns are found.
    """
    height, width = grid.shape
    if height == 0 or width == 0: 
        return None, None
        
    # Step 2: Determine which columns are entirely white (0)
    is_col_white = [np.all(grid[:, c] == 0) for c in range(width)]

    leftmost_start_col = None
    leftmost_end_col = None
    
    # Step 3 & 5: Iterate through columns to find the *first* block
    for c in range(width):
        if is_col_white[c]:
            # This is the start of the leftmost block
            leftmost_start_col = c
            # Find the end of this block
            leftmost_end_col = c
            while leftmost_end_col + 1 < width and is_col_white[leftmost_end_col + 1]:
                leftmost_end_col += 1
            # Once the first block is found, we can stop
            break 
            
    # Return the indices of the leftmost block found, or None if none exist
    return leftmost_start_col, leftmost_end_col

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation: Finds the leftmost block of all-white 
    columns and fills it entirely green.
    """
    # Step 1: Initialize output_grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    
    # Steps 2, 3, 5: Find the leftmost contiguous block of purely white columns.
    C_start, C_end = find_leftmost_white_block(input_grid)

    # Step 4: If no such block exists, return the original grid copy.
    if C_start is None:
        return output_grid 

    # Step 6: Modify the output grid: fill the target block with green (3).
    # Use numpy slicing: all rows (':'), columns from C_start up to (and not including) C_end + 1.
    output_grid[:, C_start : C_end + 1] = 3
        
    # Step 7: Return the modified grid.
    return output_grid
```