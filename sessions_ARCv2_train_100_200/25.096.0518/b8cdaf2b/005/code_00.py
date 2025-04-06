import numpy as np
import copy

"""
Projects a symmetrical pattern upwards from a source element identified in the 
bottom row, coloring only background cells (0). The source element is the central 
cell of the contiguous horizontal block of non-zero cells in the bottom row 
that is closest to the grid's horizontal center. The projection pattern's shape 
depends on the length (L) of this source block: if L=1, the horizontal distance 
(d) from the source column equals the vertical distance (k) from the source row 
minus 1 (d = k - 1); if L>1, d equals k (d = k). The projection starts two rows 
above the source row (k=2) and continues upwards. Only background cells 
(color 0) are modified.
"""

def find_source_block(bottom_row: list[int], grid_width: int) -> tuple[int | None, int | None, int | None]:
    """
    Finds the centrally located contiguous block of non-zero cells in the bottom row.

    Args:
        bottom_row: A list of integers representing the bottom row of the grid.
        grid_width: The width of the grid.

    Returns:
        A tuple (length, center_col_index, center_color) for the identified source block,
        or (None, None, None) if no suitable block is found.
    """
    width = len(bottom_row)
    blocks = []
    in_block = False
    start_col = -1

    # Iterate through the row to find all contiguous non-zero blocks
    for c in range(width):
        is_non_zero = bottom_row[c] != 0
        is_last_col = c == width - 1

        if is_non_zero and not in_block:
            # Start of a new block
            in_block = True
            start_col = c
        
        # End condition: (current cell is zero OR it's the last column) AND we are inside a block
        if (not is_non_zero or is_last_col) and in_block:
            in_block = False
            # Determine the correct end column index
            end_col = c - 1 if not is_non_zero else c 
            length = end_col - start_col + 1
            
            # Calculate the index of the central cell within the block
            center_col_idx = start_col + (length - 1) // 2
            center_color = bottom_row[center_col_idx]
            
            # Calculate the geometric center coordinate of the block for comparison
            block_geometric_center = (start_col + end_col) / 2.0
            
            blocks.append({
                'start': start_col,
                'end': end_col,
                'length': length,
                'center_col_index': center_col_idx,
                'center_color': center_color,
                'geometric_center': block_geometric_center
            })
            # Reset start_col shouldn't be needed here as loop continues

    if not blocks:
        # No non-zero blocks found
        return None, None, None 

    # Calculate the horizontal center coordinate of the entire grid
    grid_center_coord = (grid_width - 1) / 2.0

    # Find the block whose geometric center is closest to the grid's center
    # min() with a key function finds the minimum based on the key's return value
    closest_block = min(blocks, key=lambda b: abs(b['geometric_center'] - grid_center_coord))

    # Return properties of the closest block
    return closest_block['length'], closest_block['center_col_index'], closest_block['center_color']


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # Convert input to a numpy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # Handle edge case: grid height must be at least 2 for a bottom row and a row above
    if height < 2:
        # Return copy of input if grid is too small
        return output_np.tolist() 

    # Identify the bottom row and its index
    bottom_row_index = height - 1
    bottom_row_list = input_np[bottom_row_index, :].tolist()

    # Find the source block properties (length L, center column C, color X)
    source_length, source_col, source_color = find_source_block(bottom_row_list, width)

    # If no source block is found, return the initial copy
    if source_length is None:
        return output_np.tolist()

    # Determine the projection rule based on source block length L
    # d = horizontal distance, k = vertical distance from source row
    if source_length == 1:
        # Rule: d = k - 1
        get_d = lambda k: k - 1
    else: # source_length > 1
        # Rule: d = k
        get_d = lambda k: k
        
    # Perform the projection upwards from the source row
    # Iterate through vertical distances (k) starting from k=2 (two rows above source)
    # up to k=height (which corresponds to the top row, index 0, when k=height-1)
    # Note: k = bottom_row_index - target_row
    for k in range(2, height): 
        # Calculate target row index
        target_row = bottom_row_index - k
        
        # Calculate horizontal distance 'd' based on 'k' and the rule
        d = get_d(k)
        
        # If d becomes negative (can happen for k=0/1 with d=k-1, but k starts at 2), skip this k
        if d < 0:
            continue

        # Calculate target column indices
        target_col_left = source_col - d
        target_col_right = source_col + d

        # Project point to the left, checking bounds and background color
        if 0 <= target_col_left < width: # Check column bounds
            # Check if the target cell is currently background color (0)
            if output_np[target_row, target_col_left] == 0:
                output_np[target_row, target_col_left] = source_color

        # Project point to the right, checking bounds and background color
        # Avoid double-painting if d=0 (source_col == target_col_left == target_col_right)
        if d != 0 and 0 <= target_col_right < width: # Check column bounds
             # Check if the target cell is currently background color (0)
            if output_np[target_row, target_col_right] == 0:
                output_np[target_row, target_col_right] = source_color

    # Convert the final numpy array back to a list of lists and return
    return output_np.tolist()