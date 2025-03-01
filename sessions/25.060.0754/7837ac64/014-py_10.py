"""
The transformation extracts the 'red' and 'azure' pixels from specific regions of the input grid and places them, in order, in a 3x3 output grid, maintaining a coarse representation of their original relative horizontal positions. Other cells are set to white.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid to the output grid according to the task rules.
    """
    output_grid = np.zeros((3, 3), dtype=int)  # Initialize 3x3 output grid with 0s

    input_height = input_grid.shape[0]
    segment_height = input_height // 3
    
    output_row = 0
    output_col = 0
    for segment_index in range(3):
        start_row = segment_index * segment_height
        end_row = (segment_index + 1) * segment_height
        
        
        for row in range(start_row, end_row):
            for col in range(input_grid.shape[1]):
                if input_grid[row, col] not in [0, 3]:
                    output_grid[output_row, output_col] = input_grid[row,col]
                    output_col += 1
                    break # only gets first from the segment
            if output_col > 2:
              break

        output_row +=1
        output_col = 0

    return output_grid