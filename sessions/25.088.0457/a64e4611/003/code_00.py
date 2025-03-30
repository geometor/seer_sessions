"""
Transforms an input grid based on the following process:
1. Create a new grid, called the output grid, initially identical to the input grid.
2. Examine the input grid to find all columns where every pixel is white (color 0).
3. Identify all contiguous blocks (sequences) of these entirely white columns. Determine the width (number of columns) of each block.
4. Select the "target block" from these contiguous white blocks based on the following criteria:
    a. Choose the block(s) with the largest width.
    b. If there are multiple blocks with the same largest width, select the one that is furthest to the left (i.e., has the smallest starting column index).
5. If no entirely white columns were found in the input grid (and thus no target block was selected), the process stops, and the initial (unmodified) output grid is returned.
6. If a target block was selected (spanning from column `C_start` to `C_end`):
    a. Iterate through each row of the input grid, from top to bottom (row index `r`).
    b. For the current row `r`, check if *any* pixel across the *entire width* of the input grid in that row has a color other than white (i.e., color is 1 through 9).
    c. If such a non-white pixel exists in input row `r`, then in the output grid, change the color of all pixels in row `r` *within the columns of the target block* (from `C_start` to `C_end`) to green (color 3).
    d. If input row `r` contains only white pixels, then the corresponding segment in the output grid (row `r`, columns `C_start` to `C_end`) remains unchanged (it will be white).
7. After checking and potentially modifying all rows, return the final output grid. Pixels outside the target block's columns are unchanged from the input.
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
               of the selected block, or (None, None) if no empty columns are found.
    """
    height, width = grid.shape
    if height == 0 or width == 0: 
        return None, None
        
    # Determine which columns are entirely white (0)
    is_col_empty = [np.all(grid[:, c] == 0) for c in range(width)]

    max_len = 0
    best_start = -1
    current_start = -1
    current_len = 0

    # Iterate through columns to find contiguous blocks of white columns
    for c in range(width):
        if is_col_empty[c]:
            # If this is the start of a new block of white columns
            if current_len == 0: 
                current_start = c
            current_len += 1
        else: # End of a block (or not in one)
            if current_len > 0: # We just finished a block
                # Check if this block is the widest found so far
                # Note: ">" ensures that if a later block has the same width, 
                # the earlier (leftmost) one is kept.
                if current_len > max_len:
                    max_len = current_len
                    best_start = current_start
                # Reset for the next potential block
                current_len = 0 

    # After the loop, check if the grid ended with a white block
    if current_len > 0:
        if current_len > max_len:
            max_len = current_len
            best_start = current_start

    # If a block was found, return its start and end columns
    if best_start != -1:
        return best_start, best_start + max_len - 1
    else:
        # No white columns found
        return None, None

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation described in the module docstring.
    """
    # 1. Initialize output_grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 2, 3, 4. Find the widest, leftmost contiguous block of purely white columns.
    C_start, C_end = find_widest_leftmost_white_block(input_grid)

    # 5. If no such block exists, return the original grid copy.
    if C_start is None:
        return output_grid 

    # 6. Iterate through each row to determine if it should be filled within the block.
    for r in range(height):
        # 6b. Check if the *input* row 'r' contains any non-white pixel.
        if np.any(input_grid[r, :] != 0):
            # 6c. If yes, fill the segment in the *output* grid within the 
            # identified block [C_start, C_end] with green (3).
            # Python slicing is exclusive of the end index, so use C_end + 1.
            output_grid[r, C_start : C_end + 1] = 3
        # 6d. Else (input row 'r' is all white): Do nothing. 
        # The corresponding segment output_grid[r, C_start:C_end+1] remains 
        # white (0) because it was part of an identified white block in the 
        # input and copied initially.

    # 7. Return the modified grid.
    return output_grid