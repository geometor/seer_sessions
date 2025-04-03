import numpy as np

"""
Transforms a 1xN input grid based on the following rules:
1.  Extract the single row of pixel data from the 1xN input grid.
2.  Create an output grid of the same 1xN dimensions, filled initially with 
    the background color white (0). Extract the single row of the output 
    grid for modification.
3.  Locate the column index of the azure (8) pixel (the anchor) in the 
    input row. Let this be `anchor_index`.
4.  Place the azure (8) pixel into the output row at `anchor_index`.
5.  Identify the contiguous horizontal block of pixels in the input row 
    consisting of a single color that is *not* white (0) and *not* azure (8). 
    Determine its color (`block_color`) and its length (`block_length`). 
    (Assume only one such block exists).
6.  Calculate the target starting column index for this block in the output 
    row: `target_start_index = anchor_index - block_length`.
7.  Fill the pixels in the output row from `target_start_index` up to 
    (but not including) `anchor_index` with the `block_color`.
8.  Return the modified 1xN output grid.
"""

def find_anchor(grid_row, anchor_color=8):
    """
    Finds the index of the first occurrence of the anchor color in a 1D array.
    Returns -1 if not found.
    """
    for i, color in enumerate(grid_row):
        if color == anchor_color:
            return i
    return -1 # Anchor color not found

def find_movable_block(grid_row, background_color=0, anchor_color=8):
    """
    Finds the first contiguous block of a single color that is not 
    background or anchor. Returns its color and length.
    Assumes only one such block exists per the examples.
    Returns (None, 0) if no such block is found.
    """
    block_color = None
    block_length = 0
    current_len = 0
    current_color = None
    in_block = False

    for color in grid_row:
        is_movable_color = (color != background_color and color != anchor_color)
        
        if is_movable_color:
            if not in_block: # Start of a new potential block
                in_block = True
                current_color = color
                current_len = 1
            elif color == current_color: # Continue the current block
                current_len += 1
            else: # Found a block, but then a different movable color started
                  # Since we assume only one block, we take the first one found.
                  # This edge case might need refinement if multiple blocks were possible.
                  block_color = current_color
                  block_length = current_len
                  return block_color, block_length # Return immediately
        elif in_block: # End of the block we were tracking
            block_color = current_color
            block_length = current_len
            return block_color, block_length # Return immediately as we found the block

    # If the block extends to the end of the row
    if in_block:
        block_color = current_color
        block_length = current_len
        return block_color, block_length
        
    return None, 0 # No movable block found


def transform(input_grid):
    """
    Applies the transformation rule to move the colored block next to the anchor.
    """
    # Convert input grid (list of lists) to a numpy array
    input_np = np.array(input_grid, dtype=int)
    
    # --- 1. Extract the single row of pixel data ---
    if input_np.ndim == 2 and input_np.shape[0] == 1:
         input_row = input_np[0] # Select the first (and only) row
    elif input_np.ndim == 1: # Handle if input was already 1D
         input_row = input_np
    else:
         # Handle unexpected dimensions if necessary, or raise error
         raise ValueError("Input grid must be 1xN or 1D")

    height = 1
    width = len(input_row)
    
    # --- 2. Create an output grid (1xN) filled with background color ---
    output_grid = np.zeros((height, width), dtype=int)
    # Get a view of the output row for easier modification
    output_row = output_grid[0] 

    # --- 3. Locate the anchor pixel index ---
    anchor_index = find_anchor(input_row, anchor_color=8)
    if anchor_index == -1:
        # Handle case where anchor is not found (return default grid or raise error)
        # Based on examples, anchor is always present.
        print("Warning: Anchor pixel (8) not found in input.")
        return output_grid.tolist() 

    # --- 4. Place the anchor pixel in the output ---
    output_row[anchor_index] = 8

    # --- 5. Identify the movable block ---
    block_color, block_length = find_movable_block(input_row, background_color=0, anchor_color=8)

    # Proceed only if a movable block was found
    if block_color is not None and block_length > 0:
        # --- 6. Calculate the target starting index for the block ---
        target_start_index = anchor_index - block_length
        
        # --- 7. Fill the block's position in the output row ---
        # Check bounds to prevent negative indexing 
        if target_start_index >= 0:
            output_row[target_start_index:anchor_index] = block_color
        else:
            # Handle cases where block doesn't fit entirely to the left of anchor
            # (e.g., block is too long). The examples don't show this.
            # We could potentially truncate or raise an error.
            # For now, assuming it always fits based on examples.
            print(f"Warning: Block (color {block_color}, length {block_length}) "
                  f"does not fit completely to the left of anchor at index {anchor_index}. "
                  f"Calculated start index: {target_start_index}.")
            # Optionally, place the part that fits:
            # valid_length = anchor_index 
            # output_row[0:anchor_index] = block_color 
            pass # Current behavior: do nothing if it doesn't fit.


    # --- 8. Return the modified 1xN output grid as list of lists ---
    return output_grid.tolist()