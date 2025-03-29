import numpy as np
import collections # Although not strictly needed with numpy, kept for potential future use

"""
Transforms the input grid based on the following rules:

1.  Define the background color as white (0).
2.  Create a new output grid with the same dimensions as the input grid, filled entirely with the background color.
3.  Identify all "separator columns" in the input grid, which are columns consisting solely of the background color.
4.  Identify all "content blocks" in the input grid, which are maximal contiguous horizontal sequences of columns that are *not* separator columns. Record each block's start column, end column, and width.
5.  Determine if the grid configuration is "symmetric": This occurs if and only if there is exactly one separator column, and there is a content block immediately to its left (ending at `separator_column - 1`) AND a content block immediately to its right (starting at `separator_column + 1`).
6.  Iterate through each identified content block:
    a.  Extract the pixel data corresponding to this block's columns from the input grid.
    b.  Flip this extracted block data vertically (upside-down).
    c.  Determine the target start column for placing the flipped block in the output grid based on the symmetry check:
        i.  **If the grid is symmetric:** Let `sep_idx` be the index of the single separator column. If the current block is the one immediately to the left of the separator (`block_end_column == sep_idx - 1`), the target start column is `block_start_column + 1`. If the current block is the one immediately to the right of the separator (`block_start_column == sep_idx + 1`), the target start column is the block's original `block_start_column`.
        ii. **If the grid is not symmetric:** Check if the block is immediately preceded by a separator column (`sep_idx = block_start_column - 1`). If yes, the target start column is `sep_idx - block_width + 1`. If the block is *not* immediately preceded by a separator column, the target start column is the block's original `block_start_column`.
    d.  Calculate the target end column based on the target start column and the block's width.
    e.  Place the vertically flipped block data into the output grid at the calculated target columns. Ensure placement respects grid boundaries (clipping if necessary). Overwrite any existing pixels in the target location.
7.  Return the completed output grid.
"""

def find_separator_columns(grid, background_color=0):
    """Finds indices of columns composed entirely of the background color."""
    separator_cols = set()
    height, width = grid.shape
    for c in range(width):
        # Check if all pixels in the column match the background color
        if np.all(grid[:, c] == background_color):
            separator_cols.add(c)
    return separator_cols

def find_content_column_blocks(grid, separator_cols):
    """
    Finds contiguous blocks of columns that are not separator columns.
    Returns a list of dictionaries, each with 'start', 'end', and 'width'.
    """
    blocks = []
    height, width = grid.shape
    in_block = False
    start_col = -1
    for c in range(width):
        is_separator = c in separator_cols
        if not is_separator and not in_block:
            # Start of a new content block
            in_block = True
            start_col = c
        elif is_separator and in_block:
            # End of the current content block (separator encountered)
            in_block = False
            end_col = c - 1
            blocks.append({'start': start_col, 'end': end_col, 'width': end_col - start_col + 1})
            start_col = -1 # Reset start_col
        # Handle the case where a block extends to the last column
        if c == width - 1 and in_block:
             end_col = c
             blocks.append({'start': start_col, 'end': end_col, 'width': end_col - start_col + 1})
    return blocks

def transform(input_grid):
    """
    Applies the transformation logic involving flipping and repositioning
    column blocks based on separators and symmetry.
    """
    # Convert input to numpy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    background_color = 0

    # 1. Initialize the output grid filled with the background color.
    output_np = np.full_like(input_np, background_color)

    # 2. Identify separator columns and content blocks.
    separator_cols = find_separator_columns(input_np, background_color)
    content_blocks = find_content_column_blocks(input_np, separator_cols)

    # If no content, return the background grid
    if not content_blocks:
        return output_np.tolist()

    # 3. Check for the specific symmetric configuration.
    is_symmetric = False
    sep_idx = -1 # Store the index if symmetric
    if len(separator_cols) == 1:
        sep_idx = list(separator_cols)[0]
        # Check if a block ends immediately before and another starts immediately after
        left_block_present = any(b['end'] == sep_idx - 1 for b in content_blocks)
        right_block_present = any(b['start'] == sep_idx + 1 for b in content_blocks)
        if left_block_present and right_block_present:
            is_symmetric = True

    # 4. Iterate through each content block and apply transformations.
    for block in content_blocks:
        start_col = block['start']
        end_col = block['end']
        block_width = block['width']

        # a. Extract the block data from the *input* grid.
        block_data = input_np[:, start_col : end_col + 1]

        # b. Flip the block data vertically.
        flipped_block_data = np.flipud(block_data)

        # c. Determine the target start column based on symmetry or separator adjacency.
        target_start = start_col # Default: stays in place

        if is_symmetric:
            # Symmetric case rules (Example 2 logic)
            if end_col == sep_idx - 1: # Block is to the left of the separator
                target_start = start_col + 1
            elif start_col == sep_idx + 1: # Block is to the right of the separator
                target_start = start_col # Stays put
            # Note: If somehow a block wasn't adjacent in symmetric case, it would default stay put
        else:
            # Non-symmetric case rules (Example 1 logic)
            precedes_sep_idx = start_col - 1
            # Check if the block is immediately preceded by a separator
            if start_col > 0 and precedes_sep_idx in separator_cols:
                target_start = precedes_sep_idx - block_width + 1
            # Otherwise (not preceded by sep), it stays in its original start position

        # d. Calculate the target end column.
        target_end = target_start + block_width - 1

        # e. Place the flipped block into the output grid, handling boundary clipping.
        # Calculate the actual column range within the output grid bounds (0 to width-1).
        actual_target_start = max(0, target_start)
        actual_target_end = min(width - 1, target_end)

        # Calculate the corresponding column range to slice from the flipped source block data.
        source_start_col = 0
        if target_start < 0:
            source_start_col = -target_start # Offset if target starts left of grid

        source_end_col = block_width - 1
        if target_end >= width:
            source_end_col = block_width - 1 - (target_end - (width - 1)) # Adjust if target ends right of grid

        # Perform placement only if there's a valid overlap in columns.
        if actual_target_start <= actual_target_end and source_start_col <= source_end_col:
             # Check if the calculated source slice width matches the target slice width
             if (actual_target_end - actual_target_start) == (source_end_col - source_start_col):
                 # Place the correctly sliced portion of the flipped block into the target columns
                 output_np[:, actual_target_start : actual_target_end + 1] = \
                    flipped_block_data[:, source_start_col : source_end_col + 1]
             # else: Handle potential dimension mismatch (should not happen with correct logic)

    # 5. Convert the final numpy array back to a list of lists.
    return output_np.tolist()