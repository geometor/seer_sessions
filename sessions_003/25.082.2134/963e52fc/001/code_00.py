"""
The transformation rule is to double the width of each row in the input grid.
If a row contains only zeros, the output row will be double the length, filled with zeros.
If a row contains any non-zero values, each element in that row is duplicated to form the new row.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_array = np.array(input_grid)
    rows, cols = input_array.shape
    
    # Initialize the output grid as a list
    output_grid = []

    # Iterate through each row of the input grid
    for row in input_array:
        # Check if the row contains only zeros
        if np.all(row == 0):
            # Create a new row of zeros with double the width
            new_row = [0] * (2 * cols)
        else:
            # Expand the row by repeating each element
            new_row = []
            for element in row:
                new_row.extend([element, element])
        
        # Add new row
        output_grid.append(new_row)
    
    return output_grid