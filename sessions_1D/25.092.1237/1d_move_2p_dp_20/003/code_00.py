import numpy as np
import copy

"""
Transforms a 1xN grid by moving a contiguous block of a non-background (0), 
non-anchor (5) color rightwards so its right edge is immediately adjacent 
to the left of a fixed anchor pixel (gray, 5). The space left behind by 
the moving block and the space it moves over are filled with the background 
color (white, 0). Pixels at and to the right of the anchor pixel remain 
unchanged.
"""

def find_anchor(row_array):
    """
    Finds the column index of the anchor pixel (5) in a 1D array.

    Args:
        row_array (np.array): The 1D array representing the grid row.

    Returns:
        int: The column index of the anchor pixel, or -1 if not found.
    """
    anchor_indices = np.where(row_array == 5)[0]
    if len(anchor_indices) > 0:
        return anchor_indices[0] # Assume only one anchor
    return -1

def find_moving_block(row_array, anchor_col):
    """
    Finds the contiguous block of non-white (0) and non-gray (5) pixels 
    to the left of the anchor_col in a 1D array.

    Args:
        row_array (np.array): The 1D input grid row.
        anchor_col (int): The column index of the anchor pixel (5).

    Returns:
        tuple: (block_color, start_col, end_col, length) or (None, -1, -1, 0) 
               if no such block is found.
    """
    block_color = None
    start_col = -1
    end_col = -1
    length = 0

    # Iterate only up to the anchor column
    search_limit = anchor_col if anchor_col != -1 else len(row_array)
    
    for i in range(search_limit):
        pixel = row_array[i]
        if pixel != 0 and pixel != 5:
            if block_color is None:  # Start of a potential block
                block_color = pixel
                start_col = i
                end_col = i
                length = 1
            elif pixel == block_color: # Continue the block
                end_col = i
                length += 1
            else: # Different non-0/5 color - reset (shouldn't happen based on examples)
                 # This implies only ONE block is expected. If a second block of a different
                 # color starts, we stop considering the first one.
                 # If the task allows multiple blocks and we must find the *rightmost* one
                 # before the anchor, this logic needs adjustment. Assuming the first one found is *the* one.
                 return block_color, start_col, end_col, length # Return the first block found

        elif block_color is not None: # End of the block detected by 0 or 5
            # Found the complete block before the anchor or end of search area
             return block_color, start_col, end_col, length

    # If the loop finished and we were tracking a block right up to the anchor
    if block_color is not None:
        return block_color, start_col, end_col, length
        
    # If no block was found before the anchor
    return None, -1, -1, 0


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list): A list of lists representing the 1xN input grid.

    Returns:
        list: A list of lists representing the transformed 1xN output grid.
    """
    # Ensure input is treated as a 2D grid, even if 1xN
    input_array = np.array(input_grid, dtype=int)
    
    # Handle potential empty input
    if input_array.size == 0:
        return []
        
    # Verify assumption: Input is 1xN
    if input_array.shape[0] != 1:
         print(f"Warning: Expected 1 row, got {input_array.shape[0]}. Processing first row only.")
         # Or raise an error depending on desired strictness
         # raise ValueError(f"Input grid must have exactly 1 row, got {input_array.shape[0]}")

    input_row = input_array[0] # Work with the first (and only) row
    grid_width = len(input_row)

    # Initialize output row with background color (white, 0)
    output_row = np.zeros(grid_width, dtype=int)

    # Find the anchor pixel (gray, 5) column
    anchor_col = find_anchor(input_row)

    # If anchor exists, copy anchor and everything to its right from input to output
    if anchor_col != -1:
        output_row[anchor_col:] = input_row[anchor_col:]
    else:
        # No anchor found. Based on examples, this shouldn't happen. 
        # If it did, the rule is undefined. We could return the input, 
        # an all-zero grid, or raise an error. Returning all-zero for now.
        print("Warning: Anchor pixel (5) not found. Returning grid initialized to 0.")
        return [output_row.tolist()] # Return the initialized grid

    # Find the moving block (non-white, non-gray) to the left of the anchor
    block_color, start_col, end_col, block_length = find_moving_block(input_row, anchor_col)

    # If a moving block was found
    if block_color is not None:
        # Calculate the target position for the moving block
        # Target end column is one column to the left of the anchor
        target_end_col = anchor_col - 1
        # Target start column is calculated based on the length
        target_start_col = target_end_col - block_length + 1

        # Place the moving block in the target position in the output row
        # Ensure the block placement is valid (doesn't go off the left edge)
        if target_start_col >= 0:
            output_row[target_start_col : target_end_col + 1] = block_color
        else:
            # Handle theoretical case where block might not fully fit 
            # (start index < 0). Shouldn't happen with task constraints.
            print(f"Warning: Block does not fit entirely left of the anchor. Calculated start: {target_start_col}")
            # Place the part that fits, starting from column 0
            fit_length = block_length + target_start_col # How many columns actually fit
            if fit_length > 0:
                 output_row[0 : fit_length] = block_color
            # The rest (target_end_col + 1 to anchor_col-1) remains 0, which is correct.

    # If no moving block was found, the output_row already contains the
    # anchor section (if found) and is otherwise filled with 0s, which is correct.

    # Convert the final numpy row back to a list and wrap it in another list
    # to match the expected 1xN grid output format.
    output_grid = [output_row.tolist()]
    
    return output_grid