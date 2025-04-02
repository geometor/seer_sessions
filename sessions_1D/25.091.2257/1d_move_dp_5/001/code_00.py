import numpy as np

"""
Identifies a contiguous horizontal block of a single color (not white 0 or azure 8) 
and a single azure (8) pixel in a 1D input grid.
Moves the colored block horizontally to the right so that its rightmost pixel 
is immediately adjacent to the left of the azure pixel. 
The background remains white (0), and the azure pixel's position is fixed.
The output grid has the same dimensions as the input grid.
"""

# Helper function to find the index of the first pixel of a given color in a 1D array
def find_pixel_index(grid_1d, color):
    """Finds the index of the first occurrence of a specific color."""
    indices = np.where(grid_1d == color)[0]
    if len(indices) > 0:
        return indices[0] # Return the index of the first occurrence
    return -1 # Indicate not found

# Helper function to find the contiguous block of the main color (non-0, non-8)
def find_colored_block(grid_1d):
    """
    Finds the main colored block (non-0, non-8).
    Returns its color, start index, and length.
    Returns None if no such block is found.
    """
    block_color = -1
    block_start = -1
    block_length = 0
    in_block = False
    background_color = 0
    target_color = 8

    for i, pixel in enumerate(grid_1d):
        # Check if the pixel is part of the movable block
        is_block_pixel = (pixel != background_color and pixel != target_color)

        if is_block_pixel:
            if not in_block:
                # Found the start of the block
                block_color = pixel
                block_start = i
                block_length = 1
                in_block = True
            elif pixel == block_color:
                # Continue the block
                block_length += 1
            else:
                # Found a different color - this shouldn't happen based on examples
                # Assuming only one contiguous block exists
                break 
        elif in_block:
            # The pixel is background or target, and we were in a block, so the block ends here
            break
            
    if block_start != -1:
        return block_color, block_start, block_length
    else:
        # No block found
        return None

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by moving the colored block next to the azure pixel.

    Args:
        input_grid: A numpy array representing the input grid. Assumed to be 1D
                    or a 2D array with a single row based on examples.

    Returns:
        A numpy array representing the transformed grid.
    """
    
    # Handle potential 2D array with single row by flattening
    original_shape = input_grid.shape
    if input_grid.ndim > 1:
        if input_grid.shape[0] == 1 or input_grid.shape[1] == 1:
             grid_1d = input_grid.flatten()
        else:
             # If it's genuinely 2D and not a single row/column, this logic might not apply
             # For now, return a copy as the transformation is defined for 1D sequence
             print(f"Warning: Input grid dimensions {original_shape} not handled. Returning copy.")
             return input_grid.copy()
    else:
        grid_1d = input_grid

    # Define background and target colors
    background_color = 0
    target_color = 8

    # Initialize the output grid with the background color
    output_grid = np.full_like(grid_1d, background_color)

    # Locate the target azure pixel (8)
    azure_index = find_pixel_index(grid_1d, target_color)
    if azure_index == -1:
        # If no target pixel, maybe return the original grid or background grid
        print("Warning: Azure pixel (8) not found. Returning background grid.")
        return output_grid.reshape(original_shape) # Reshape back before returning

    # Place the target pixel in the output grid
    output_grid[azure_index] = target_color

    # Locate the colored block (non-background, non-target)
    block_info = find_colored_block(grid_1d)
    if block_info is None:
        # If no block found, return the grid with only the target pixel placed
        print("Warning: Colored block not found. Returning grid with only azure pixel.")
        return output_grid.reshape(original_shape) # Reshape back

    block_color, _, block_length = block_info # Original start index is not needed for placement

    # Calculate the new starting index for the block
    # The block should end at the index immediately before the azure pixel (azure_index - 1)
    # So, the block starts at (azure_index - 1) - (block_length - 1) = azure_index - block_length
    new_block_start = azure_index - block_length

    # Check for validity of the new start index
    if new_block_start < 0:
        print(f"Warning: Calculated block start index {new_block_start} is out of bounds. Block not placed.")
        # Return grid with only azure pixel placed
        return output_grid.reshape(original_shape) # Reshape back

    # Place the colored block at its new position in the output grid
    output_grid[new_block_start : new_block_start + block_length] = block_color

    # Reshape the output to match the original input shape (e.g., if it was 1xN)
    return output_grid.reshape(original_shape)