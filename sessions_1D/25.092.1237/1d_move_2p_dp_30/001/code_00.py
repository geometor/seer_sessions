import numpy as np

"""
Shift a contiguous block of non-white, non-gray pixels two positions to the right, 
while keeping a single gray pixel in its original position. The rest of the grid remains white.
The input is assumed to be a 1D array (represented as a 1xN grid).
"""

def find_colored_block(grid_1d):
    """Finds the start index, end index, and color of the colored block."""
    start_index = -1
    end_index = -1
    block_color = -1
    in_block = False
    for i, pixel in enumerate(grid_1d):
        if pixel != 0 and pixel != 5:
            if not in_block:
                start_index = i
                block_color = pixel
                in_block = True
            end_index = i # Keep updating end index while in block
        elif in_block: # Exited the block
            break
    if start_index != -1:
        return start_index, end_index, block_color
    else:
        return None # Should not happen based on examples

def find_gray_pixel(grid_1d):
    """Finds the index of the gray pixel."""
    for i, pixel in enumerate(grid_1d):
        if pixel == 5:
            return i
    return None # Should not happen based on examples

def transform(input_grid):
    """
    Transforms the input grid by shifting the colored block right by 2 positions,
    keeping the gray pixel fixed.
    """
    # Assuming input_grid is a 1xN numpy array or list of lists
    # Convert to 1D numpy array for easier processing
    if isinstance(input_grid, list):
        grid_1d = np.array(input_grid[0])
    else: # Assuming numpy array
        grid_1d = input_grid.flatten()

    grid_width = len(grid_1d)

    # Initialize output_grid with the background color (white)
    output_grid_1d = np.zeros(grid_width, dtype=int)

    # Find the gray pixel's position
    gray_index = find_gray_pixel(grid_1d)
    if gray_index is None:
        # Handle error or unexpected input: no gray pixel found
        print("Warning: Gray pixel not found.")
        # Decide on behavior: return input? return blank? raise error?
        # For now, proceed assuming it might be okay for some test cases
        # or return the initialized grid
        # return np.array([output_grid_1d.tolist()]) # return as 1xN list of lists

    # Find the colored block's details
    block_info = find_colored_block(grid_1d)
    if block_info is None:
         # Handle error or unexpected input: no colored block found
        print("Warning: Colored block not found.")
         # If gray pixel was also found, place it.
        if gray_index is not None:
             output_grid_1d[gray_index] = 5
        return np.array([output_grid_1d.tolist()]) # return as 1xN list of lists

    start_index, end_index, block_color = block_info
    block_length = end_index - start_index + 1

    # Place the gray pixel in the output grid at its original position
    # Check if gray_index was found before placing
    if gray_index is not None:
        output_grid_1d[gray_index] = 5

    # Calculate the new starting position for the colored block
    new_start_index = start_index + 2

    # Place the colored block in the output grid at the new position
    # Ensure the new block position is within bounds
    if new_start_index + block_length <= grid_width:
        output_grid_1d[new_start_index : new_start_index + block_length] = block_color
    else:
        # Handle case where the shifted block goes out of bounds (based on examples, this doesn't happen)
        # Option 1: Truncate the block
        # visible_length = grid_width - new_start_index
        # output_grid_1d[new_start_index : new_start_index + visible_length] = block_color
        # Option 2: Error or different logic? Assume it fits for now.
        print(f"Warning: Shifted block exceeds grid boundary. Start: {new_start_index}, Length: {block_length}, Width: {grid_width}")
        # Defaulting to placing what fits
        output_grid_1d[new_start_index : grid_width] = block_color


    # Reshape back to 1xN list of lists format expected by ARC
    output_grid = np.array([output_grid_1d.tolist()])

    return output_grid
