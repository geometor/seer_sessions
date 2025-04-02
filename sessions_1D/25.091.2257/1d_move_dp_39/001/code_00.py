import numpy as np

def find_green_pixel(grid):
    """Finds the index of the green pixel (3) in a 1D grid."""
    for index, pixel in enumerate(grid):
        if pixel == 3:
            return index
    return -1 # Should not happen based on examples

def find_colored_block(grid):
    """
    Finds the contiguous block of non-white (0) and non-green (3) pixels.
    Returns the color, start index, and length of the block.
    """
    block_color = -1
    start_index = -1
    length = 0
    in_block = False

    for index, pixel in enumerate(grid):
        if pixel != 0 and pixel != 3:
            if not in_block:
                # Start of a new block
                block_color = pixel
                start_index = index
                length = 1
                in_block = True
            elif pixel == block_color:
                # Continue the current block
                length += 1
            else:
                 # Found a different color, should not happen based on task description
                 # but if it did, the first block is the one we care about.
                 break 
        elif in_block:
            # End of the block
            break 
            
    if start_index != -1:
        return block_color, start_index, length
    else:
        # No block found (should not happen based on examples)
        return -1, -1, 0

def transform(input_grid):
    """
    Transforms the input grid according to the following rule:
    1. Identify the single green pixel (3) and keep its position fixed.
    2. Identify the contiguous block of a single color (other than white 0 or green 3).
    3. Move this colored block so that its rightmost pixel is immediately to the left of the green pixel.
    4. Fill the remaining cells with white pixels (0).
    Assumes the input is a 1D list or numpy array.
    """
    # Ensure input is a numpy array for easier slicing
    input_array = np.array(input_grid)
    
    # Get the dimensions (length) of the input grid
    grid_length = len(input_array)
    
    # Initialize the output grid with the same dimensions, filled with white (0)
    output_grid = np.zeros(grid_length, dtype=int)

    # Find the position (index) of the green pixel (3)
    green_index = find_green_pixel(input_array)
    if green_index == -1:
        # Handle error: Green pixel not found (though problem implies it always exists)
        return output_grid # Or raise an error

    # Place the green pixel (3) at the same position in the output grid
    output_grid[green_index] = 3

    # Find the colored block (non-0, non-3): its color, original start index, and length
    block_color, _, block_length = find_colored_block(input_array)
    
    if block_color != -1 and block_length > 0:
        # Calculate the new starting position for the block in the output grid
        # The end position of the block should be green_index - 1
        # So, the start position is (green_index - 1) - (block_length - 1) = green_index - block_length
        new_start_index = green_index - block_length

        # Ensure the block fits within the grid boundaries (optional check, might not be needed for ARC)
        if new_start_index >= 0 and (new_start_index + block_length) <= grid_length:
             # Place the identified block into the output grid at the calculated position
            output_grid[new_start_index : new_start_index + block_length] = block_color
        else:
            # Handle case where block placement is out of bounds (if necessary)
             print(f"Warning: Block placement out of bounds. Green Index: {green_index}, Block Length: {block_length}")


    # Return the modified grid (as a list, consistent with input format if needed)
    return output_grid.tolist() # Or return output_grid directly if numpy array is acceptable
