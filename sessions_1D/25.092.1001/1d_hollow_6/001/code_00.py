import copy
import numpy as np # Although not strictly needed for list manipulation, ARC often uses numpy

"""
Transforms the input 1D grid (list or numpy array) by identifying a single 
contiguous block of non-white pixels and changing all pixels within that block, 
except for the first and last pixels of the block, to white (0). White pixels 
outside the block remain unchanged. Assumes the input is effectively 1D.
"""

def find_non_white_block_indices(grid):
    """
    Finds the start and end indices of the single contiguous non-white block 
    in a 1D list or array.
    Assumes there is at most one such block per the task description.
    It identifies the index of the first non-white pixel and the index of the 
    last non-white pixel.
    Returns (None, None) if no non-white pixels are found.

    Args:
        grid (list | np.ndarray): A 1D list or numpy array of integers representing pixels.

    Returns:
        tuple: A tuple containing (start_index, end_index).
               Returns (None, None) if no non-white block is found.
    """
    start_index = None
    end_index = None
    
    # Flatten in case of a 1xN or Nx1 numpy array, otherwise iterate directly
    if isinstance(grid, np.ndarray):
        grid_flat = grid.flatten()
    else:
        grid_flat = grid # Assumed to be a list

    for i, pixel in enumerate(grid_flat):
        if pixel != 0:  # Check for non-white pixel (value is not 0)
            if start_index is None:
                # Record the index of the first non-white pixel encountered
                start_index = i
            # Always update the end index to the latest non-white pixel found
            end_index = i
            
    return start_index, end_index

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list | np.ndarray): A list or numpy array of integers 
                                        representing the input pixels. 
                                        Assumed to be 1D or effectively 1D (e.g., 1xN).

    Returns:
        list | np.ndarray: A new grid representing the transformed pixels, 
                           in the same format as the input (list or numpy array).
    """
    
    is_numpy = isinstance(input_grid, np.ndarray)
    
    # Handle numpy array input: flatten, process, reshape
    if is_numpy:
        original_shape = input_grid.shape
        # Ensure it's effectively 1D
        if not (len(original_shape) == 1 or 
                (len(original_shape) == 2 and (original_shape[0] == 1 or original_shape[1] == 1))):
             # This function is designed for 1D grids based on examples.
             # If input is truly 2D with more than one row/column, the logic might need revision.
             # For now, proceed assuming it behaves like 1D.
             pass 
        grid_list = input_grid.flatten().tolist()
    else:
        # Assume input is already a list
        grid_list = input_grid

    # Find the start and end indices of the non-white block in the list version
    start_index, end_index = find_non_white_block_indices(grid_list)

    # Initialize the output grid as a copy of the input list
    output_list = list(grid_list)

    # Check if a valid block of length > 1 was found
    # A block exists if start_index is not None (end_index will also be not None)
    # The length is > 1 if end_index > start_index
    if start_index is not None and end_index > start_index:
        # Iterate through the indices *between* the start and end indices
        # range(start, stop) goes up to stop - 1
        for i in range(start_index + 1, end_index):
            # Change the interior pixels of the block to white (0)
            output_list[i] = 0

    # If the input was a numpy array, convert the result back and reshape
    if is_numpy:
        output_grid = np.array(output_list).reshape(original_shape)
    else:
        # If the input was a list, return the list
        output_grid = output_list

    # Return the modified grid
    return output_grid