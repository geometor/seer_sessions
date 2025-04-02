import numpy as np

def find_first_non_white_block(grid):
    """
    Finds the start index, end index, and color of the first contiguous block of non-white pixels.
    Returns (start_index, end_index, color) or (None, None, None) if no such block is found.
    Assumes grid is 1D.
    """
    start_index = -1
    end_index = -1
    block_color = None
    
    for i, pixel in enumerate(grid):
        if pixel != 0: # Found a non-white pixel
            if start_index == -1: # Start of the block
                start_index = i
                block_color = pixel
            # Continue if the pixel matches the block color
            if pixel == block_color:
                 end_index = i
            else: # Found a different color, block ended before this
                 break # Stop after the first block
        elif start_index != -1: # Found white after the block started, block ended
            break
            
    if start_index != -1:
        return start_index, end_index, block_color
    else:
        return None, None, None

def find_first_pixel(grid, color, start_search_index):
    """
    Finds the index of the first occurrence of a specific color starting from a given index.
    Returns the index or None if not found.
    Assumes grid is 1D.
    """
    for i in range(start_search_index, len(grid)):
        if grid[i] == color:
            return i
    return None

def transform(input_grid):
    """
    Identifies the first contiguous block of non-white pixels and the first azure (8) pixel
    that appears after it. Fills any white (0) pixels between the end of the block
    and the azure pixel with the color of the block.
    """
    # Handle the 1xN 2D grid case by flattening it to 1D
    if input_grid.ndim == 2 and input_grid.shape[0] == 1:
        grid_1d = input_grid[0]
    elif input_grid.ndim == 1:
        grid_1d = input_grid
    else:
        # Handle cases not described (e.g., multi-row grids) - return unchanged for now
        # Or raise an error depending on expected behavior.
        # For this specific task, examples are 1xN, so flattening is appropriate.
        # Let's assume it will always be 1xN or 1D based on examples.
         if input_grid.ndim > 1 and input_grid.shape[0] > 1:
              print("Warning: unexpected grid dimensions. Returning input unchanged.")
              return input_grid.copy()
         # If shape is (1, N), flatten it
         grid_1d = input_grid.flatten()


    # Create a copy to modify
    output_grid_1d = grid_1d.copy()
    
    # 1. Identify the first contiguous block of non-white pixels
    start_index, block_end_index, fill_color = find_first_non_white_block(grid_1d)
    
    # Proceed only if a block was found
    if start_index is not None:
        # 2. Find the index of the first azure (8) pixel after the block
        azure_index = find_first_pixel(grid_1d, 8, block_end_index + 1)
        
        # 3. If an azure pixel is found after the block
        if azure_index is not None:
            # a. Iterate from the pixel after the block up to the azure pixel
            for i in range(block_end_index + 1, azure_index):
                # b. If the pixel is white (0), change its color
                if output_grid_1d[i] == 0:
                    output_grid_1d[i] = fill_color

    # 4. Leave all other pixels unchanged (already handled by copying)
    
    # 5. Reshape back to original input shape if it was 2D
    if input_grid.ndim == 2:
        output_grid = output_grid_1d.reshape(input_grid.shape)
    else:
        output_grid = output_grid_1d

    return output_grid