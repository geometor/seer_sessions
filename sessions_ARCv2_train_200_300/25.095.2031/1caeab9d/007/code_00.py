import numpy as np
import statistics
import math

"""
Transforms an input grid based on the following rules:

1. Identifies all contiguous rectangular blocks that are exactly 2 rows high 
   and composed of a single, identical non-zero digit (color).
2. Determines the height (H) of the input grid.
3. Applies one of two placement strategies based on H:
    a. If H >= 10 (Adjacent Placement):
        - Calculates the target top row: r_target = H // 2.
        - Sorts the identified blocks by their original leftmost column index (c).
        - Finds the minimum leftmost column index (c_min) among all blocks.
        - Places the sorted blocks horizontally adjacent to each other in the 
          output grid, starting at row r_target and column c_min. The block 
          colors fill rows r_target and r_target + 1.
    b. If H < 10 (Original Position Placement):
        - Collects the original top row indices (r) of all identified blocks.
        - Calculates the target top row: r_target = median_low of the sorted 
          list of these starting rows (using the lower median if the count is even).
        - Places each identified block in the output grid at rows r_target 
          and r_target + 1, maintaining its original horizontal position 
          (original leftmost column c and original width w).
4. Initializes the output grid with the same dimensions as the input, filled 
   with zeros (background). Cells covered by the placed blocks receive the 
   block's color.
5. If no 2-row high blocks are found, returns the zero-filled output grid.
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
            # - Non-zero color in both rows (r, r+1) at column c
            # - Same color in both cells
            # - Neither cell has been visited yet (part of a previously found block)
            if (grid[r, c] > 0 and 
                grid[r + 1, c] == grid[r, c] and 
                not visited[r, c] and 
                not visited[r + 1, c]):
                
                color = grid[r, c]
                
                # Found a potential top-left corner (r, c) of a block. Determine its width.
                width = 0
                # Scan columns to the right starting from c
                for c_offset in range(W - c):
                    current_c = c + c_offset
                    # Check if the block continues horizontally in both rows r and r+1
                    # with the same color and hasn't been visited
                    if (current_c < W and # Boundary check
                        grid[r, current_c] == color and not visited[r, current_c] and
                        grid[r + 1, current_c] == color and not visited[r+1, current_c]):
                        # Increment width and mark cells as visited
                        width += 1
                        visited[r, current_c] = True
                        visited[r + 1, current_c] = True
                    else:
                        # Stop scanning horizontally if the block ends, changes color, hits visited cells, or goes out of bounds
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
            
            # Mark cells as visited if they are non-zero and haven't been visited yet,
            # even if they weren't the start of a detected block in this pass.
            # This prevents single cells or parts of blocks from being re-evaluated incorrectly.
            if grid[r, c] > 0 and not visited[r, c]:
                visited[r, c] = True
            if grid[r + 1, c] > 0 and not visited[r + 1, c]:
                visited[r + 1, c] = True

    # Ensure any non-zero cells in the last row (if grid height > 0) are marked visited
    # if they weren't part of a block identified above.
    if H > 0:
       for c in range(W):
            if grid[H-1, c] > 0 and not visited[H-1, c]:
                visited[H-1, c] = True
                
    return blocks


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules to the input grid.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape

    # Initialize output grid with the background color (0)
    output_grid = np.zeros_like(input_np)

    # Step 1: Identify all 2-row high blocks
    blocks = find_blocks_height2(input_np)

    # Step 2: Check if any blocks were found
    if not blocks:
        # If no blocks, return the empty (all zeros) output grid
        return output_grid.tolist()

    # Step 3 & 4: Check Grid Height and Apply Conditional Placement Logic
    if H >= 10:
        # --- Adjacent Placement Logic ---
        
        # Calculate the target top row
        r_target = H // 2
        
        # Sort blocks by their original leftmost column index
        blocks.sort(key=lambda b: b['c'])
        
        # Determine the starting column for the combined strip (minimum 'c' of sorted blocks)
        c_start = blocks[0]['c'] 
        
        # Place blocks adjacently
        current_c = c_start
        for block in blocks:
            color = block['color']
            w = block['w']
            
            # Define the horizontal slice for the current block in the output
            # Ensure the slice does not exceed the grid width
            col_end = min(current_c + w, W)
            col_slice = slice(current_c, col_end)
            
            # Check if target rows are valid before writing
            if r_target < H:
                 output_grid[r_target, col_slice] = color
            if r_target + 1 < H:
                 output_grid[r_target + 1, col_slice] = color
            
            # Update the starting column for the next block
            current_c += w # Assumes blocks fit horizontally based on examples

    else: # H < 10
        # --- Original Position Placement Logic ---
        
        # Collect the original top row indices ('r') of all identified blocks
        start_rows = [b['r'] for b in blocks]
        
        # Calculate the target top row using median_low
        # Handle single block case explicitly for median function
        if len(start_rows) == 1:
            r_target = start_rows[0]
        elif len(start_rows) > 1:
            sorted_start_rows = sorted(start_rows)
            r_target = statistics.median_low(sorted_start_rows)
        else: # Should not happen if blocks list is not empty, but handle defensively
            r_target = 0 

        # Place each block individually at its original column position in the target rows
        for block in blocks:
            color = block['color']
            c = block['c']  # Original starting column
            w = block['w']  # Original width
            
            # Define the column slice for the block's original horizontal position
            # Ensure the slice does not exceed the grid width
            col_end = min(c + w, W)
            col_slice = slice(c, col_end)
            
            # Check if target rows are valid before writing
            if r_target < H:
                 output_grid[r_target, col_slice] = color
            if r_target + 1 < H:
                 output_grid[r_target + 1, col_slice] = color

    # Step 5: Return Output
    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()