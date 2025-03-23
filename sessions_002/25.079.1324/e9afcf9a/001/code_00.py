"""
Transforms two rows of uniform-colored pixels into two rows of alternating colors, 
where the colors are taken from the input rows. The first output row starts with 
the color of the first input row, and the second output row starts with the color 
of the second input row.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the alternating color rule.
    """
    # Get the colors from the input rows.
    color_a = input_grid[0, 0]
    color_b = input_grid[1, 0]
    
    # Get the length of the rows.
    length = input_grid.shape[1]
    
    # Initialize the output grid with the same dimensions as the input.
    output_grid = np.zeros_like(input_grid)
    
    # Create the first output row with alternating colors, starting with color_a.
    for i in range(length):
        if i % 2 == 0:
            output_grid[0, i] = color_a
        else:
            output_grid[0, i] = color_b
    
    # Create the second output row with alternating colors, starting with color_b.
    for i in range(length):
        if i % 2 == 0:
            output_grid[1, i] = color_b
        else:
            output_grid[1, i] = color_a
            
    return output_grid