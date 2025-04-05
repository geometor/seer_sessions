import numpy as np
import copy

def find_first_trigger_pattern(grid_arr):
    """
    Finds the coordinates (row, col) of the top-left corner of the first 
    horizontal [6, 6] pattern where row > 0 and col > 0.

    Args:
        grid_arr (np.array): The input grid as a NumPy array.

    Returns:
        tuple: (row, col) of the pattern start, or None if not found.
    """
    H, W = grid_arr.shape
    for r in range(1, H):  # Start search from row 1
        for c in range(1, W - 1): # Start search from col 1
            if grid_arr[r, c] == 6 and grid_arr[r, c + 1] == 6:
                return r, c
    return None

def transform(input_grid):
    """
    Transforms the input grid based on the observed rules:
    1. Default behavior: Mirror the left half of the grid onto the right half.
    2. Conditional override: If a horizontal [6, 6] pattern is found 
       at (pr, pc) where pr > 0 and pc > 0, copy a specific block 
       from the input grid to a calculated position in the output grid, 
       overwriting the mirrored content.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed output grid.
    """
    # Convert input to NumPy array for easier manipulation
    input_arr = np.array(input_grid, dtype=int)
    H, W = input_arr.shape
    
    # Initialize output grid with zeros
    output_arr = np.zeros_like(input_arr)
    
    # --- Step 1: Default mirroring ---
    mid = W // 2 # Integer division to find the midpoint column index
    
    # Copy the left half (columns 0 to mid-1) from input to output
    left_half = input_arr[:, :mid]
    output_arr[:, :mid] = left_half
    
    # Determine how much of the left half can be mirrored into the right half
    mirrored_width = min(mid, W - mid) # Handles both even and odd widths
    
    # Mirror the left half into the columns starting from 'mid'
    output_arr[:, mid : mid + mirrored_width] = left_half[:, :mirrored_width]
    
    # --- Step 2: Conditional Block Copy ---
    
    # Find the trigger pattern [6, 6] where r > 0 and c > 0
    pattern_coords = find_first_trigger_pattern(input_arr)
    
    if pattern_coords:
        pr, pc = pattern_coords
        
        # Define source block boundaries based on pattern location (pr, pc)
        # As observed in train_2: src starts at (2, 0), ends relative to (pr, pc)
        src_row_start = 2
        src_col_start = 0
        src_row_end = pr + 6 # exclusive end row index
        src_col_end = pc     # exclusive end col index

        # Define destination top-left corner based on pattern location
        dest_row_start = pr + 2
        dest_col_start = pc
        
        # Check if source block is valid within input dimensions
        if src_row_start < src_row_end and src_col_start < src_col_end and \
           src_row_end <= H and src_col_end <= W:
           
            # Extract the source block
            source_block = input_arr[src_row_start:src_row_end, src_col_start:src_col_end]
            block_h, block_w = source_block.shape
            
            # Check if destination placement is valid within output dimensions
            if dest_row_start + block_h <= H and dest_col_start + block_w <= W:
                # Copy the block to the destination in the output grid
                output_arr[dest_row_start : dest_row_start + block_h, 
                           dest_col_start : dest_col_start + block_w] = source_block

    # Convert the final NumPy array back to a list of lists
    output_grid = output_arr.tolist()
    
    return output_grid
