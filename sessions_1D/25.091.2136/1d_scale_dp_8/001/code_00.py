import numpy as np

def find_first_color_block_end(grid_1d):
    """Finds the end index and color of the first non-white, non-yellow block."""
    block_color = -1
    block_end_index = -1
    in_block = False
    for i, pixel in enumerate(grid_1d):
        if not in_block and pixel != 0 and pixel != 4:
            # Start of a potential block
            block_color = pixel
            in_block = True
            block_end_index = i 
        elif in_block:
            if pixel == block_color:
                # Continue the block
                block_end_index = i
            else:
                # End of the block found
                return block_color, block_end_index
    # Handle case where block goes to the end of the grid
    if in_block:
        return block_color, block_end_index
    return -1, -1 # No suitable block found

def find_first_yellow_after(grid_1d, start_index):
    """Finds the index of the first yellow pixel (4) at or after start_index."""
    for i in range(start_index, len(grid_1d)):
        if grid_1d[i] == 4:
            return i
    return -1 # Yellow not found

def transform(input_grid):
    """
    Identifies the first contiguous block of a single color (Color C) that is not white (0) and not yellow (4).
    Finds the first yellow pixel (4) appearing after this block.
    Changes the color of all white pixels (0) located between the end of the Color C block and the yellow pixel to Color C.
    Leaves all other pixels unchanged.
    Assumes input is a 1D list representing the grid row.
    """
    # Convert input list to numpy array for easier handling
    # Ensure it's treated as a 1D array
    grid_1d = np.array(input_grid, dtype=int).flatten() 
    
    # Initialize output_grid as a copy of the input
    output_grid = grid_1d.copy()

    # 1. & 3. Find the first contiguous block of a non-white, non-yellow color (Color C) and its end index.
    block_color, block_end_index = find_first_color_block_end(grid_1d)
    
    # Check if a valid block was found
    if block_color != -1:
        # 4. Find the first yellow pixel (4) after the block ends.
        yellow_index = find_first_yellow_after(grid_1d, block_end_index + 1)

        # Check if yellow was found after the block
        if yellow_index != -1:
            # 5. & 6. Identify white pixels between the block end and the yellow pixel and change their color.
            # Iterate from the pixel immediately after the block up to (but not including) the yellow pixel.
            for i in range(block_end_index + 1, yellow_index):
                if output_grid[i] == 0: # If the pixel is white
                    output_grid[i] = block_color # Change it to the block's color

    # 8. Return the modified grid as a list (matching the input format)
    # Since the input was shown as a flat list, return a flat list.
    return output_grid.tolist()