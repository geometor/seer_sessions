"""
The transformation selects the first non-black, and non-green pixel from each of three equal horizontal segments of the input grid and places them in a 3x3 output grid. The selected pixels are placed vertically in the output grid, in order of the segment from which it was selected, and put in the left-most column.
"""

import numpy as np

def transform(input_grid):
    # Initialize 3x3 output grid with 0s (black)
    output_grid = np.zeros((3, 3), dtype=int)

    input_height = input_grid.shape[0]
    segment_height = input_height // 3
    
    output_row = 0
    # Iterate through each segment
    for segment_index in range(3):
        start_row = segment_index * segment_height
        end_row = (segment_index + 1) * segment_height
        if segment_index == 2 :
            end_row = input_height
        
        # Find the first non-black and non-green pixel in the current segment
        found = False
        for row in range(start_row, end_row):
            for col in range(input_grid.shape[1]):
                if input_grid[row, col] != 0 and input_grid[row, col] != 3:
                    output_grid[output_row, 0] = input_grid[row, col]
                    output_row += 1
                    found = True
                    break  # Stop searching after finding the first matching pixel
            if found:
                break

    return output_grid