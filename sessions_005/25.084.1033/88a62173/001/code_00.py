import numpy as np
from collections import Counter

"""
Transformation Rule:
1. Identify the horizontal row in the input grid composed entirely of white pixels (0), which acts as a separator.
2. Extract four specific 2x2 blocks from the input grid:
    a. Top-Left (ATL): Rows 0-1, Columns 0-1.
    b. Top-Right (ATR): Rows 0-1, Columns (width-2)-(width-1).
    c. Below-Top-Left (BTL): Rows (separator_row+1)-(separator_row+2), Columns 0-1.
    d. Below-Top-Right (BTR): Rows (separator_row+1)-(separator_row+2), Columns (width-2)-(width-1).
3. Compare these four 2x2 blocks. Three of them will be identical, and one will be unique.
4. The unique 2x2 block is the output grid.
"""

def find_separator_row(grid):
    """Finds the index of the first row consisting entirely of zeros."""
    height = grid.shape[0]
    width = grid.shape[1]
    for r in range(height):
        if np.all(grid[r, :] == 0):
            return r
    return -1 # Should not happen based on task description

def extract_block(grid, row_start, col_start, height, width):
    """Extracts a subgrid (block) from the grid."""
    return grid[row_start:row_start+height, col_start:col_start+width]

def grids_to_tuples(grids):
    """Converts a list of NumPy arrays (grids) into a list of tuples for hashable comparison."""
    return [tuple(map(tuple, grid)) for grid in grids]

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape

    # 1. Find the separator row
    separator_row_index = find_separator_row(grid_np)
    if separator_row_index == -1:
        # Handle error case where no separator is found, though examples suggest it always exists
        # For now, return an empty grid or raise an error
        print("Error: Separator row not found.")
        return [] 

    # 2. Define and extract the four candidate 2x2 blocks
    # Ensure dimensions are sufficient (at least 5x5 based on examples)
    if height < separator_row_index + 3 or width < 2:
         print(f"Error: Grid dimensions ({height}x{width}) insufficient for extraction around separator row {separator_row_index}.")
         return []

    block_atl = extract_block(grid_np, 0, 0, 2, 2)
    block_atr = extract_block(grid_np, 0, width - 2, 2, 2)
    block_btl = extract_block(grid_np, separator_row_index + 1, 0, 2, 2)
    block_btr = extract_block(grid_np, separator_row_index + 1, width - 2, 2, 2)

    candidate_blocks = [block_atl, block_atr, block_btl, block_btr]

    # 3. Compare the blocks to find the unique one
    # Convert NumPy arrays to tuples of tuples to make them hashable for Counter
    candidate_tuples = grids_to_tuples(candidate_blocks)
    
    # Count the occurrences of each distinct block pattern
    block_counts = Counter(candidate_tuples)

    unique_block_tuple = None
    for block_tuple, count in block_counts.items():
        if count == 1:
            unique_block_tuple = block_tuple
            break
            
    # 4. The unique block is the output
    if unique_block_tuple is not None:
        # Convert the unique tuple back to a list of lists
        output_grid = [list(row) for row in unique_block_tuple]
    else:
        # Handle error case where no unique block is found (shouldn't happen based on examples)
        print("Error: No unique block found.")
        output_grid = [] # Or raise an error

    return output_grid