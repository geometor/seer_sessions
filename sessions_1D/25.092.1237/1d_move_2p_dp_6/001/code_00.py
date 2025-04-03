"""
Transforms the input grid by performing a cyclic shift (rotation) of the single row 
of pixels two positions to the right. Pixels shifted off the right end wrap around 
to the beginning of the row.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a cyclic shift of 2 positions to the right on the input row.

    Args:
        input_grid (list of lists): A grid containing a single row of pixels.

    Returns:
        list of lists: The transformed grid with the row shifted.
    """
    # Convert the input grid (list of lists) to a NumPy array for easier manipulation
    # Assuming the input_grid always contains exactly one row
    input_row = np.array(input_grid[0])
    
    # Get the length (number of columns) of the row
    row_length = len(input_row)
    
    # Create an output row of the same length, initialized with zeros (or any placeholder)
    # Using NumPy array simplifies assignment
    output_row = np.zeros_like(input_row)
    
    # Iterate through each pixel in the input row
    for i in range(row_length):
        # Calculate the new index j after shifting right by 2 positions
        # Use the modulo operator (%) to handle the wrap-around
        j = (i + 2) % row_length
        
        # Place the pixel from the input row at index i into the output row at index j
        output_row[j] = input_row[i]
        
    # Convert the resulting NumPy array back to a list of lists format
    output_grid = [output_row.tolist()]
    
    return output_grid
