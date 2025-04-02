import numpy as np

"""
This function transforms a 1xN input grid containing exactly two non-white pixels 
of the same color into an output grid of the same dimensions. The transformation 
involves filling the horizontal segment between these two non-white pixels 
(inclusive) with their color. Pixels outside this segment remain white (0).
"""

def transform(input_grid):
    """
    Fills the horizontal segment between two non-white pixels in a 1xN grid.

    Args:
        input_grid (list of lists): A 2D list representing the 1xN input grid.

    Returns:
        numpy.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array
    input_array = np.array(input_grid, dtype=int)
    
    # Ensure the input is actually 1xN or Nx1 (handle potential ambiguity if needed)
    # For this specific task, examples are 1xN.
    if input_array.shape[0] != 1:
        # Handle unexpected input shape if necessary
        # print(f"Warning: Expected input shape 1xN, but got {input_array.shape}")
        return input_array # Return input if shape is not 1xN

    # Find the coordinates (row, column) of all non-white (non-zero) pixels
    # For a 1xN array, row_indices will always be [0, 0] if two points are found.
    row_indices, col_indices = np.where(input_array != 0)

    # Check if there are exactly two non-white pixels as expected
    if len(col_indices) != 2:
        # Handle unexpected number of non-white pixels.
        # Returning the original input grid is a safe fallback.
        # print(f"Warning: Expected 2 non-white pixels, found {len(col_indices)}.")
        return input_array.copy() 

    # Determine the start and end column indices of the segment
    # Find the minimum and maximum of the column indices found
    start_col = np.min(col_indices)
    end_col = np.max(col_indices)
    
    # Get the fill color from one of the non-white pixels (they have the same color)
    # Use the coordinates found by np.where
    fill_color = input_array[row_indices[0], col_indices[0]]
    
    # Initialize the output grid with the same shape as the input, filled with white (0)
    output_grid = np.zeros_like(input_array)
    
    # Fill the segment in the output grid's first row (row 0) 
    # from start_col to end_col (inclusive)
    # Numpy slicing [start:end] is exclusive of 'end', so use end_col + 1
    output_grid[0, start_col : end_col + 1] = fill_color
    
    return output_grid