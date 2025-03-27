import numpy as np

def find_background_and_pattern_start(grid):
    """
    Finds the background color and the starting row index of the pattern block.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (background_color, pattern_start_row)
               Returns (None, -1) if no pattern block is found.
    """
    if grid.shape[0] == 0:
        return None, -1

    # Assume the color of the top-left pixel is the background initially
    background_color = grid[0, 0]
    
    # Find the first row that is NOT entirely the background color
    pattern_start_row = -1
    for r in range(grid.shape[0]):
        if not np.all(grid[r, :] == background_color):
            pattern_start_row = r
            break
            
    # If all rows are background, maybe the top-left wasn't representative?
    # Or maybe there's no pattern. Let's refine: check if the first row *is* fully background.
    if pattern_start_row == -1:
        if np.all(grid[0, :] == background_color):
             # Entire grid is background color, no pattern found this way
             return background_color, -1
        else:
             # The first row itself contains non-background, so pattern starts at row 0
             # Find a dominant background color if possible (e.g., most frequent in grid)
             # For simplicity based on examples, let's assume if row 0 isn't uniform background,
             # the pattern starts at 0, and background needs another definition (unused here).
             # Or, maybe the background assumption was wrong. Let's assume pattern starts at 0
             # if row 0 isn't uniform background as identified by top-left.
             # A safer approach for background might be the most frequent color overall.
             # Let's stick to the simpler logic for now based on examples:
             # Background is the color filling the top uniform rows.
             background_color = grid[0, 0] # Re-confirm top-left
             pattern_start_row = 0
             for r in range(grid.shape[0]):
                 if not np.all(grid[r, :] == background_color):
                     pattern_start_row = r
                     break
                 if r > 0 and not np.all(grid[r,:] == grid[0,:]): # Check if row is uniform AND same as first row
                    pattern_start_row = r
                    background_color = grid[0,0] # Keep initial assumption
                    break
             # If still -1, it means the whole grid *is* uniform, matching the top-left color
             if pattern_start_row == -1: return background_color, -1


    # Find the actual background color based on the first uniform rows
    background_color = grid[0, 0] # Assume top-left initially
    for r in range(pattern_start_row):
        if not np.all(grid[r,:] == grid[0,0]):
            # This case shouldn't happen if pattern_start_row logic is correct
            # If it does, maybe background is just grid[0,0]?
            pass # Keep background_color as grid[0,0]
        
    return background_color, pattern_start_row


def find_pattern_block(grid, background_color, pattern_start_row):
    """
    Extracts the pattern block from the grid.

    Args:
        grid (np.ndarray): The input grid.
        background_color (int): The identified background color.
        pattern_start_row (int): The starting row index of the pattern.

    Returns:
        np.ndarray: The pattern block (subgrid), or None if no pattern found.
    """
    if pattern_start_row == -1:
        return None

    pattern_rows = []
    # Iterate from the start row downwards
    for r in range(pattern_start_row, grid.shape[0]):
        # A row belongs to the pattern if it contains any non-background color
        if np.any(grid[r, :] != background_color):
            pattern_rows.append(grid[r, :])
        else:
            # If we find a fully background row *after* the pattern started,
            # check if subsequent rows also contain non-background.
            # The description implies a *contiguous* block below background rows.
            # So, the first full background row after the start marks the end.
            break 
            
    # Alternative interpretation: Pattern block includes *all* rows from pattern_start_row to the end.
    # Let's test based on examples: example 1 pattern is rows 5-9. Example 2 is 6-9.
    # This suggests the pattern block is simply all rows from pattern_start_row to the end.
    pattern_block = grid[pattern_start_row:, :]

    if pattern_block.shape[0] == 0:
         return None
         
    return pattern_block


def transform(input_grid):
    """
    Transforms the input grid based on identifying a pattern block and tiling it.

    1. Determine grid dimensions (H, W).
    2. Identify the background color (dominant color in top rows).
    3. Identify the `PatternBlock`: Contiguous rows below background containing non-background colors. Note its height `H_p`.
    4. Determine the `TileBlock`:
       a. If `H_p * 2 == H`, `TileBlock` is the `PatternBlock`.
       b. Otherwise, split `PatternBlock` at `mid = H_p // 2`. `TileBlock` is `BottomHalf` concatenated vertically above `TopHalf`.
    5. Construct the output grid by tiling the `TileBlock` vertically to fill the height H.
    """
    input_grid = np.array(input_grid)
    H, W = input_grid.shape

    # 1 & 2: Identify background color and start of pattern
    # Using a simple approach first: background is color of grid[0,0]
    # Pattern starts at the first row different from row 0 OR containing non-background
    background_color = input_grid[0, 0]
    pattern_start_row = 0
    uniform_background_rows_end = -1
    for r in range(H):
        is_uniform_bkg = np.all(input_grid[r, :] == background_color)
        if r==0 and not is_uniform_bkg: # Pattern starts at row 0
             pattern_start_row = 0
             uniform_background_rows_end = -1 # No uniform background rows
             break
        if r > 0 and not is_uniform_bkg: # Found the first row with non-background elements
             pattern_start_row = r
             uniform_background_rows_end = r - 1
             break
        if r == H - 1 and is_uniform_bkg: # Reached end, all uniform background
             # This implies no pattern according to the rule "below background rows"
             # However, the output should probably be the input in this case?
             # Or maybe just the background? Let's assume output is input grid itself.
             # For now, let's signal no pattern found.
              pattern_start_row = -1
              break # Exit loop

    # If no pattern found (e.g., all background), return the input grid? Or empty?
    # Based on the logic, we expect a pattern. If not, maybe return input unchanged.
    if pattern_start_row == -1:
        # Or based on examples, if no pattern is distinct, maybe tile the whole input?
        # Let's refine based on NLP: find pattern block *below* background rows.
        # If uniform_background_rows_end is H-1, there are no rows *below*.
        if uniform_background_rows_end == H-1:
            # According to logic, no pattern block exists. What should output be?
            # Let's default to returning the input grid for now.
             print("Warning: No pattern block found below background rows.")
             return input_grid.tolist()


    # 3. Identify the PatternBlock
    # It consists of all rows from pattern_start_row to the end of the grid.
    pattern_block = input_grid[pattern_start_row:, :]
    H_p = pattern_block.shape[0]

    if H_p == 0:
         print("Warning: Pattern block has zero height.")
         # This case means pattern_start_row was H, which shouldn't happen with prior checks.
         return input_grid.tolist() # Return input as fallback

    # 4. Determine the TileBlock
    tile_block = None
    if H_p * 2 == H:
        # Condition met: TileBlock is identical to PatternBlock
        tile_block = pattern_block
        # Update H_p to reflect the tile block height (it's the same here)
        tile_H = H_p
        # print(f"Condition H_p*2 == H met. Tile height: {tile_H}")

    else:
        # Condition not met: Rearrange PatternBlock
        mid = H_p // 2
        top_half = pattern_block[:mid, :]
        bottom_half = pattern_block[mid:, :]
        # Concatenate bottom half above top half
        tile_block = np.vstack((bottom_half, top_half))
        # Update H_p to reflect the tile block height (it's the same as pattern block height)
        tile_H = H_p
        # print(f"Condition H_p*2 == H NOT met. Tile height: {tile_H}, Midpoint: {mid}")


    # 5. Construct the output grid by tiling
    N_repeats = H // tile_H
    N_remainder = H % tile_H

    # Initialize list to collect output rows
    output_rows = []

    # Append full TileBlock repetitions
    for _ in range(N_repeats):
        output_rows.append(tile_block)

    # Append remaining rows from the top of TileBlock
    if N_remainder > 0:
        output_rows.append(tile_block[:N_remainder, :])

    # Concatenate all parts into the final output grid
    if not output_rows:
         # Should not happen if H > 0
         print("Warning: No output rows generated.")
         return np.zeros((H, W), dtype=int).tolist() # Return empty grid of correct size

    output_grid = np.vstack(output_rows)

    # Ensure output grid has the correct dimensions (should be guaranteed by logic)
    if output_grid.shape != (H, W):
        print(f"Warning: Output shape {output_grid.shape} doesn't match input shape {(H, W)}. Resizing.")
        # This indicates a potential logic error, but let's try to resize/crop/pad if needed
        # For now, let's assume the vstack worked correctly.
        pass # Or raise an error, or attempt correction

    return output_grid.tolist()