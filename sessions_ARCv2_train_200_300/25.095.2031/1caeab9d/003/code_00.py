import numpy as np
import statistics
import math

"""
Identifies contiguous rectangular blocks of height 2 with the same non-zero color in the input grid.
Determines a target top row (r_target) for placement in the output grid based on the input grid's height (H) and the median starting row of the identified blocks:
- If H >= 10, r_target = floor(H / 2).
- If H < 10, r_target = median_low of the starting rows of all blocks.
Rearranges the identified blocks into the output grid. Each block is placed in rows r_target and r_target + 1, maintaining its original horizontal column position (leftmost column index 'c' and width 'w').
The output grid has the same dimensions as the input grid, with all cells not covered by the placed blocks set to 0.
"""

def find_blocks_height2(grid: np.ndarray) -> list[dict]:
    """
    Finds all contiguous rectangular blocks of exactly height 2 with the same non-zero color.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        with keys: 'color', 'r' (top row), 'c' (left col), 'w' (width).
    """
    H, W = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []

    # Iterate rows up to H-2 (inclusive) to find blocks starting at row r and ending at r+1
    for r in range(H - 1):
        for c in range(W):
            # Check for the start of a potential block:
            # - Non-zero color
            # - Not yet visited
            # - Cell below has the same non-zero color
            if grid[r, c] > 0 and not visited[r, c] and grid[r + 1, c] == grid[r, c] and not visited[r+1,c]:
                color = grid[r, c]
                
                # Found a potential top-left corner (r, c) of a block. Determine its width.
                width = 0
                # Scan columns to the right starting from c
                for c_offset in range(W - c):
                    current_c = c + c_offset
                    # Check if the block continues horizontally in both rows r and r+1
                    if (grid[r, current_c] == color and not visited[r, current_c] and
                        grid[r + 1, current_c] == color and not visited[r+1, current_c]):
                        # Increment width and mark cells as visited
                        width += 1
                        visited[r, current_c] = True
                        visited[r + 1, current_c] = True
                    else:
                        # Stop scanning horizontally if the block ends or changes color
                        break 

                # If a valid block (width > 0) was found, add its properties to the list
                if width > 0:
                    blocks.append({
                        'color': int(color), # Store as standard int
                        'r': int(r),       # Store as standard int
                        'c': int(c),       # Store as standard int
                        'w': int(width)    # Store as standard int
                        # Height is implicitly 2
                    })
            
            # Important: Mark any unvisited non-zero cell as visited *after* checking for block start.
            # This prevents single non-zero cells or parts of already found blocks from being reconsidered.
            # It also handles cells that might be part of a block but weren't the top-left starting point
            # found in this specific (r, c) iteration.
            if grid[r, c] > 0 and not visited[r, c]:
                visited[r, c] = True
            if grid[r + 1, c] > 0 and not visited[r+1, c]: # Also mark the cell below if non-zero and unvisited
                 visited[r+1, c] = True


    return blocks


def determine_target_row(grid_height: int, block_start_rows: list[int]) -> int:
    """
    Determines the target top row for placing blocks in the output grid.

    Args:
        grid_height: The height (H) of the input grid.
        block_start_rows: A list of the starting row indices ('r') of all identified blocks.

    Returns:
        The calculated target top row index (r_target).
    """
    if grid_height >= 10:
        # For taller grids, target row is the middle row (floor division)
        r_target = grid_height // 2
    else:
        # For shorter grids, target row is the median_low of the block start rows
        # Ensure the list is sorted for median calculation
        sorted_start_rows = sorted(block_start_rows)
        r_target = statistics.median_low(sorted_start_rows)
        
    return r_target

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid according to the specified rules.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape

    # Initialize output grid with the background color (0)
    output_grid = np.zeros_like(input_np)

    # --- Step 1: Identify all 2-row high blocks ---
    blocks = find_blocks_height2(input_np)

    # If no blocks are found, return the empty (all zeros) output grid
    if not blocks:
        return output_grid.tolist()

    # --- Step 2: Determine the target row for placement ---
    # Collect the starting row ('r') of each identified block
    start_rows = [b['r'] for b in blocks]
    # Calculate the target top row based on grid height and median start row
    r_target = determine_target_row(H, start_rows)
    
    # Ensure target rows are within grid bounds (should be, but good practice)
    if r_target + 1 >= H: 
        # This case indicates an issue, maybe only 1 row grid or unexpected median.
        # Handle appropriately, e.g., adjust or log error. For now, cap it.
        print(f"Warning: Target rows {r_target}, {r_target+1} may exceed grid height {H}. Adjusting.")
        # If r_target is the last row, we can only write to r_target.
        # But the rule implies height 2, so this shouldn't happen with valid input/logic.
        # Let's proceed assuming r_target and r_target+1 are valid.
        pass # Or adjust r_target if needed, e.g. r_target = max(0, H-2) if len(blocks)>0

    # --- Step 3: Place blocks individually in the output grid ---
    # Iterate through the list of identified blocks (order doesn't matter for placement)
    for block in blocks:
        color = block['color']
        c = block['c']  # Original starting column
        w = block['w']  # Original width
        
        # Define the column slice for the block's original horizontal position
        # Ensure the slice does not exceed the grid width
        col_start = c
        col_end = min(c + w, W) # Prevent writing past the grid width
        col_slice = slice(col_start, col_end)
        
        # Copy the block's color into the output grid at the target rows (r_target, r_target+1)
        # and its original columns (col_slice)
        output_grid[r_target, col_slice] = color
        # Check if r_target+1 is still within bounds before writing
        if r_target + 1 < H:
            output_grid[r_target + 1, col_slice] = color
        # Else: block is height 2 but target is last row - only top half gets written if bounds strictly enforced.

    # Convert the final numpy array back to a list of lists before returning
    return output_grid.tolist()