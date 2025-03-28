import numpy as np
from typing import List, Dict, Tuple

def find_blocks(grid: np.ndarray) -> List[Dict]:
    """
    Identifies solid rectangular blocks of non-white color in the grid.

    Args:
        grid: The input numpy array representing the grid.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        and contains 'color', 'top', 'left', 'height', 'width'.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []

    for r in range(height):
        for c in range(width):
            # Check for non-white pixel that hasn't been visited
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                
                # --- Find potential width ---
                current_w = 1
                while c + current_w < width and grid[r, c + current_w] == color and not visited[r, c + current_w]:
                    current_w += 1
                
                # --- Find potential height ---
                current_h = 1
                is_solid = True
                while r + current_h < height:
                    row_solid = True
                    for col_offset in range(current_w):
                        if c + col_offset >= width or grid[r + current_h, c + col_offset] != color or visited[r + current_h, c + col_offset]:
                            row_solid = False
                            break
                    if row_solid:
                        current_h += 1
                    else:
                        # If the row below is not solid or has different color/visited cells, stop height expansion
                        break
                
                # --- Verify if the entire block is solid and matches initial width/height assumptions ---
                # This double check ensures irregular shapes starting like rectangles aren't misidentified
                actual_w = current_w 
                actual_h = current_h
                
                # Re-verify width for all rows in the potential block
                for row_idx in range(r, r + actual_h):
                     temp_w = 0
                     while c + temp_w < width and grid[row_idx, c + temp_w] == color:
                         temp_w += 1
                     actual_w = min(actual_w, temp_w) # Smallest width determines the actual rectangular width

                # Re-verify height for all cols in the potential block (less critical if width check is good)
                # For simplicity, we trust the initial height expansion combined with width adjustment

                # Check if all cells within final bounds are the correct color
                is_truly_solid_rectangle = True
                for i in range(r, r + actual_h):
                    for j in range(c, c + actual_w):
                         if i >= height or j >= width or grid[i, j] != color or visited[i,j]:
                             # This condition should ideally not be met if logic above is perfect,
                             # but acts as a safeguard. If we hit this frequently, find_blocks logic needs refinement.
                             # If we find a visited cell here, it means overlapping detections, needs debug.
                             # For now, we invalidate the block if it's not perfectly solid or already visited.
                             is_truly_solid_rectangle = False
                             break
                    if not is_truly_solid_rectangle:
                        break
                        
                # If block is valid and solid
                if is_truly_solid_rectangle and actual_w > 0 and actual_h > 0:
                     # Mark cells as visited
                     visited[r:r + actual_h, c:c + actual_w] = True
                     
                     # Store block info
                     blocks.append({
                         'color': color,
                         'top': r,
                         'left': c,
                         'height': actual_h,
                         'width': actual_w
                     })
                # If not a valid block (e.g., L-shape), mark only the starting cell visited
                # so other parts can be potentially picked up later if they form valid blocks.
                # However, the current logic tries to find maximal rectangles first.
                # If the block check failed after finding potential h/w, we still need to mark the initial cell.
                elif not visited[r,c]: # ensure we don't double mark if validation failed weirdly
                     visited[r,c] = True


    return blocks


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Identifies solid rectangular blocks of non-white color.
    For blocks exactly 3 rows high, modifies the middle row to alternate
    between the block's original color and white (0), starting with the original color.
    Other blocks and the background remain unchanged.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Create a copy to modify
    output_np = np.copy(input_np)
    
    # Find all solid rectangular blocks
    blocks = find_blocks(input_np)
    
    # Iterate through each found block
    for block in blocks:
        # Check if the block's height is exactly 3
        if block['height'] == 3:
            # Get block properties
            original_color = block['color']
            middle_row_index = block['top'] + 1
            start_col = block['left']
            end_col = block['left'] + block['width'] # Exclusive end index
            
            # Iterate through the columns of the middle row within the block
            for col in range(start_col, end_col):
                # Check if the column index relative to the block start is even or odd
                if (col - start_col) % 2 == 0:
                    # Even index (0, 2, 4...): set to original color (already is, but explicit)
                    output_np[middle_row_index, col] = original_color
                else:
                    # Odd index (1, 3, 5...): set to white (0)
                    output_np[middle_row_index, col] = 0
                    
    # Convert the result back to a list of lists
    output_grid = output_np.tolist()
    
    return output_grid