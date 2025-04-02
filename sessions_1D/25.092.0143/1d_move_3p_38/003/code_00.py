import numpy as np

"""
Transforms a 1D input grid by identifying a single contiguous block of 
non-white pixels and shifting this block exactly 3 positions to the right. 
The background remains white (0), and the block retains its color and length. 
Pixels shifted beyond the grid boundary are lost.
"""

def find_non_white_block_np(grid):
    """
    Finds the start index, end index, and color of the single contiguous 
    block of non-white pixels in a NumPy array.

    Args:
        grid (np.ndarray): The input 1D NumPy array.

    Returns:
        tuple: (start_index, end_index, color) or (None, None, None) if no 
               block found or if the block is not contiguous/uniform.
    """
    # Find indices of all non-white pixels
    non_white_indices = np.where(grid != 0)[0]

    # Handle case where there are no non-white pixels
    if len(non_white_indices) == 0:
        return None, None, None

    # Identify potential start and end indices
    start_index = non_white_indices[0]
    end_index = non_white_indices[-1]
    
    # Check if the identified range length matches the count of non-white pixels (checks contiguity)
    if (end_index - start_index + 1) != len(non_white_indices):
        # Implies multiple blocks or gaps
        return None, None, None 

    # Get the color of the first non-white pixel
    color = grid[start_index]
    
    # Verify that all pixels within the block have the same color
    block_slice = grid[start_index : end_index + 1]
    if not np.all(block_slice == color):
         # Implies multiple colors within the apparent block
        return None, None, None

    return start_index, end_index, color

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.ndarray): A 1D NumPy array representing the input grid.
                                 It's assumed to contain integers 0-9.

    Returns:
        np.ndarray: A 1D NumPy array representing the transformed output grid.
    """
    # Ensure input is a NumPy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # Ensure input is 1D for simplicity
    input_grid = input_grid.flatten()
    grid_size = len(input_grid)

    # Initialize the output grid with the background color (white, 0)
    output_grid = np.zeros_like(input_grid)

    # Find the non-white block in the input grid
    start_index, end_index, color = find_non_white_block_np(input_grid)

    # If no valid block was found, return the all-white grid
    if start_index is None:
        return output_grid

    # Calculate the length of the block
    block_length = end_index - start_index + 1

    # Calculate the new starting position (shifted 3 positions right)
    new_start_index = start_index + 3
    
    # Calculate the actual range in the output grid where the block will be placed,
    # respecting grid boundaries.
    
    # Determine the starting index in the output grid (cannot be less than 0)
    actual_start = new_start_index 
    
    # Determine the ending index in the output grid (cannot exceed grid_size - 1)
    actual_end = new_start_index + block_length -1

    # Place the block (with its color) into the output grid within the valid range
    # Iterate through the block's elements relative to its new start position
    for i in range(block_length):
        current_output_index = new_start_index + i
        # Check if the current position is within the grid bounds
        if 0 <= current_output_index < grid_size:
            output_grid[current_output_index] = color
        # No need to continue if we go past the end boundary
        elif current_output_index >= grid_size:
            break

    return output_grid