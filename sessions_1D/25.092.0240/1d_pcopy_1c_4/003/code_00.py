"""
Transforms a single-row input grid (represented as a 1xN NumPy array) by replacing 
every occurrence of the pattern [white, magenta, white] (i.e., [0, 6, 0]) with 
the pattern [magenta, magenta, magenta] (i.e., [6, 6, 6]). 
Existing sequences of three magenta pixels are preserved.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the pattern replacement transformation to the input grid.

    Args:
        input_grid (np.ndarray): A 2D NumPy array, expected shape (1, N), 
                                containing integer color values (0 and 6).

    Returns:
        np.ndarray: A 2D NumPy array of the same shape as the input, 
                   with the transformation applied.
    """
    # Ensure the input is a 2D numpy array and has at least one row
    if not isinstance(input_grid, np.ndarray) or input_grid.ndim != 2 or input_grid.shape[0] == 0:
         raise ValueError("Input must be a 2D NumPy array with at least one row.")
         
    # Extract the first row (assuming the transformation only applies to the first row or it's a 1xN grid)
    input_row = input_grid[0, :] 
    
    # Initialize output_row as a copy of the input_row to modify
    # We make a copy to read from the original while modifying the copy
    output_row = input_row.copy()
    row_length = len(input_row)

    # Iterate through the input row to find the pattern [0, 6, 0]
    # We need to check indices i-1, i, and i+1, so the loop runs from 1 to length-2
    for i in range(1, row_length - 1):
        # Check if the pattern [white, magenta, white] exists in the *original* input row
        if input_row[i-1] == 0 and input_row[i] == 6 and input_row[i+1] == 0:
            # If the pattern is found, modify the *output* row copy
            # Replace the [0, 6, 0] pattern with [6, 6, 6] centered at index i
            output_row[i-1] = 6
            output_row[i] = 6
            output_row[i+1] = 6
            
    # Reshape the modified 1D row back into a 2D array (1, N) to match ARC format
    # The -1 in reshape infers the second dimension based on the array size and the first dimension (1)
    output_grid = output_row.reshape(1, -1) 

    return output_grid
