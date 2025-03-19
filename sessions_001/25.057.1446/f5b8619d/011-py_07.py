"""
Creates a 12x12 output grid filled with azure (8), preserving gray (5) pixels from the input grid in their original row positions, and expanding the input width by a factor of 2, inserting additional azure pixels based on original input.
"""

import numpy as np

def transform(input_grid):
    # Create a 12x12 output grid filled with azure (8)
    output_grid = np.full((12, 12), 8)

    # Get the number of columns in original input
    input_cols = input_grid.shape[1]
    
    # Calculate expansion factor, expected output columns 
    expanded_cols = input_cols * 2

    # Calculate left padding = total - (original + expanded)
    left_padding = 12 - expanded_cols

    # Preserve Gray: Copy gray (5) pixels from input to output, maintaining row and relative column positions
    for row_index, row in enumerate(input_grid):
        gray_indices = np.where(row == 5)[0]  # Find indices of gray pixels in the current row
        
        if gray_indices.size > 0:
            new_positions = [] # create list of new positions

            for col_index in gray_indices:
               # the padding shifts the position, and the new position must maintain spacing by doubling its original index
               new_positions.append(left_padding + (col_index * 2) )

            # place '5' based on the newly calculated position
            for pos in new_positions:
               if pos < 12: # Ensure position is within bounds
                  output_grid[row_index, pos] = 5
            
    return output_grid