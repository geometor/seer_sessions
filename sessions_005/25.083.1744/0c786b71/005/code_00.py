"""
The output grid is twice the size of the input grid in both dimensions. 
The output grid is constructed by interleaving the reversed rows of the input grid with the original rows, 
then repeating this interleaved pattern.
"""

import numpy as np

def transform(input_grid):
    # Get dimensions of input grid
    input_height, input_width = input_grid.shape
    
    # Initialize output grid with doubled dimensions
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through the input grid rows
    for i in range(input_height):
        # Get the current row
        original_row = input_grid[i, :]
        
        # Reverse the row
        reversed_row = original_row[::-1]

        # Interleave original and reversed rows
        interleaved_row = np.empty(input_width * 2, dtype=int)
        interleaved_row[0::2] = reversed_row
        interleaved_row[1::2] = original_row
        
        # Populate the corresponding rows in output grid
        output_grid[i] = interleaved_row
        output_grid[i + input_height] = interleaved_row

    return output_grid