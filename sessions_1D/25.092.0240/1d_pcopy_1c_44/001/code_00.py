import numpy as np

def find_non_white_blocks(grid_row):
    """
    Identifies contiguous blocks of non-white pixels in a 1D grid row.

    Args:
        grid_row: A 1D numpy array representing the row.

    Returns:
        A list of tuples, where each tuple represents a block:
        (color, start_index, end_index, size)
    """
    blocks = []
    width = len(grid_row)
    col = 0
    while col < width:
        color = grid_row[col]
        if color == 0:  # Background pixel
            col += 1
            continue

        # Found the start of a non-white block
        start_col = col
        block_color = color
        # Find the end of the block
        while col < width and grid_row[col] == block_color:
            col += 1
        end_col = col - 1  # Inclusive end index
        block_size = end_col - start_col + 1
        blocks.append((block_color, start_col, end_col, block_size))
        # 'col' is already advanced past the current block
    return blocks

def transform(input_grid):
    """
    Transforms the input grid based on the size of contiguous non-white blocks.
    Single-pixel blocks are expanded to three pixels (center, left, right).
    Multi-pixel blocks are copied unchanged.

    Args:
        input_grid: A numpy array representing the input grid (expected to be 1 row).

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Ensure input is a 2D numpy array
    input_grid = np.array(input_grid)
    
    # Get dimensions
    height, width = input_grid.shape
    
    # Initialize output grid with background color (white, 0)
    output_grid = np.zeros_like(input_grid)

    # Process the single row (assuming height is always 1 for this task based on examples)
    if height == 1:
        input_row = input_grid[0]
        output_row = output_grid[0]
        
        # Find all non-white blocks in the input row
        blocks = find_non_white_blocks(input_row)

        # Process each block based on its size
        for color, start_idx, end_idx, size in blocks:
            if size == 1:
                # Expand single-pixel block to size 3
                center_idx = start_idx
                output_row[center_idx] = color  # Set center pixel
                if center_idx > 0:
                    output_row[center_idx - 1] = color  # Set left pixel if within bounds
                if center_idx < width - 1:
                    output_row[center_idx + 1] = color  # Set right pixel if within bounds
            elif size > 1:
                # Copy multi-pixel block directly
                output_row[start_idx : end_idx + 1] = input_row[start_idx : end_idx + 1]
                
    # If the input grid had more than one row (unexpected based on examples),
    # the output would just be zeros. The logic currently only handles the first row.
    # For a robust solution handling multiple rows, the logic would need adjustment,
    # potentially processing each row independently if the rule applies row-wise.

    return output_grid