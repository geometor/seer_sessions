import numpy as np

"""
Transforms the input 1xN NumPy array by identifying the single contiguous block of non-white pixels. 
It keeps the first and last pixel of this block and changes all pixels strictly between them to white (0). 
Pixels outside the original block (the background white pixels) remain unchanged.
"""

def find_non_white_block_indices(row):
    """
    Finds the start and end indices of the contiguous non-white block in a 1D NumPy array.

    Args:
        row (np.array): A 1D NumPy array representing a row of the grid.

    Returns:
        tuple: A tuple containing (start_index, end_index). 
               Returns (None, None) if no non-white pixels are found.
    """
    # Find indices of all non-white pixels
    non_white_indices = np.where(row != 0)[0]
    
    # If no non-white pixels exist, return None for both indices
    if non_white_indices.size == 0:
        return None, None
        
    # The start index is the first non-white index found
    start_index = non_white_indices[0]
    # The end index is the last non-white index found
    end_index = non_white_indices[-1]
    
    # Note: This assumes a single contiguous block based on the examples.
    # A more complex check could verify np.all(np.diff(non_white_indices) == 1)
    
    return start_index, end_index

def transform(input_grid):
    """
    Hollows out the interior of a contiguous block of non-white pixels in a 1D grid (represented as 1xN NumPy array).

    Args:
        input_grid (np.array): A 2D NumPy array representing the input grid (expected to be 1xN).

    Returns:
        np.array: The transformed grid.
    """
    # Check for empty input grid
    if input_grid is None or input_grid.size == 0:
        return np.array([[]]) # Return an empty representation consistent with ARC format if needed

    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)
    
    # Extract the first (and likely only) row
    # Check if the grid has at least one row before accessing it
    if output_grid.shape[0] == 0:
         return output_grid # Return the empty copy if no rows

    row = output_grid[0]
    
    # Find the start and end indices of the non-white block in the row
    start_index, end_index = find_non_white_block_indices(row)
    
    # If no block was found (start_index is None), return the unmodified copy
    if start_index is None:
        return output_grid
        
    # Modify the pixels *between* the start and end indices to white (0)
    # This range only exists if end_index > start_index + 1 (block length > 2)
    # NumPy slicing handles the empty range case correctly (if end_index <= start_index + 1, nothing happens)
    # The slice output_grid[0, start_index + 1 : end_index] selects the row 0, 
    # and columns from start_index + 1 up to (but not including) end_index.
    output_grid[0, start_index + 1 : end_index] = 0
            
    return output_grid