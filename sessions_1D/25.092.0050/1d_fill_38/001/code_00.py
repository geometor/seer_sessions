import numpy as np

"""
This function transforms a 1D input grid (represented as a numpy array) 
containing exactly two non-white pixels of the same color into an output grid 
of the same dimensions. The transformation involves filling the segment 
between these two non-white pixels (inclusive) with their color. Pixels 
outside this segment remain white (0).
"""

def transform(input_grid):
    """
    Fills the segment between two non-white pixels in a 1D grid.

    Args:
        input_grid (list or tuple): A 1D list or tuple representing the input grid.

    Returns:
        numpy.ndarray: A 1D numpy array representing the transformed output grid.
    """
    # Convert input to a numpy array for efficient operations
    input_array = np.array(input_grid, dtype=int)
    
    # Find the indices of all non-white (non-zero) pixels
    non_white_indices = np.where(input_array != 0)[0]

    # Check if there are exactly two non-white pixels as expected
    if len(non_white_indices) != 2:
        # Handle unexpected input, perhaps return input or raise error
        # For this specific task based on examples, we assume 2 points exist.
        # If not, returning the original might be a safe fallback, 
        # or returning an empty/zero array depending on expected behavior for errors.
        # Let's return the input copy for now if the assumption fails.
        # print("Warning: Input does not contain exactly two non-white pixels.")
        return input_array.copy() 

    # Determine the start and end indices of the segment
    # The indices might not be sorted, so find the min and max
    start_index = np.min(non_white_indices)
    end_index = np.max(non_white_indices)
    
    # Get the fill color from one of the non-white pixels (they have the same color)
    fill_color = input_array[start_index]
    
    # Initialize the output grid with the same shape as the input, filled with white (0)
    output_grid = np.zeros_like(input_array)
    
    # Fill the segment in the output grid from start_index to end_index (inclusive)
    # Note: numpy slicing is exclusive of the end index, so we add 1
    output_grid[start_index : end_index + 1] = fill_color
    
    return output_grid
