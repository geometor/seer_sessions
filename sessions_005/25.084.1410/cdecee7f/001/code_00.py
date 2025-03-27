"""
Extract non-white pixels from the input grid by scanning column-first (top-to-bottom within each column), collect their colors into a sequence. 
Arrange these colors into a 3x3 output grid. 
The first row of the output uses the first 3 colors from the sequence in order.
The second row uses the next 3 colors (elements 3, 4, 5) from the sequence, but placed in reverse order (sequence[5], sequence[4], sequence[3]).
The third row uses the next 3 colors (elements 6, 7, 8) from the sequence in order.
If the sequence has fewer than 9 colors, the remaining output grid cells are left as white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the described scanning and placement rule.
    
    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.
        
    Returns:
        np.ndarray: A 3x3 numpy array representing the output grid.
    """
    # Get dimensions of the input grid
    rows, cols = input_grid.shape
    
    # Initialize an empty list to store the sequence of non-white colors
    color_sequence = []
    
    # Scan the input grid column by column, then row by row within each column
    for j in range(cols):
        for i in range(rows):
            # Get the color of the current pixel
            color = input_grid[i, j]
            # If the color is not white (0), add it to the sequence
            if color != 0:
                color_sequence.append(color)
                
    # Initialize a 3x3 output grid filled with white (0)
    output_grid = np.zeros((3, 3), dtype=int)
    
    # Fill the output grid based on the color_sequence
    
    # Fill the first row (row index 0)
    for i in range(3):
        if i < len(color_sequence):
            output_grid[0, i] = color_sequence[i]
            
    # Fill the second row (row index 1) in reverse order of sequence elements [3, 4, 5]
    # output_grid[1, 0] <-- color_sequence[5]
    # output_grid[1, 1] <-- color_sequence[4]
    # output_grid[1, 2] <-- color_sequence[3]
    if 5 < len(color_sequence):
        output_grid[1, 0] = color_sequence[5]
    if 4 < len(color_sequence):
        output_grid[1, 1] = color_sequence[4]
    if 3 < len(color_sequence):
        output_grid[1, 2] = color_sequence[3]
        
    # Fill the third row (row index 2)
    for i in range(3):
        sequence_index = 6 + i
        if sequence_index < len(color_sequence):
            output_grid[2, i] = color_sequence[sequence_index]
            
    return output_grid
