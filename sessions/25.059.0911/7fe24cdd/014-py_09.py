"""
The input grid is expanded to double its original dimensions. The 3x3 input becomes a 6x6 output.

The original 3x3 input grid occupies the top-left quadrant of the 6x6 output grid.
The top-right quadrant of the output is a vertically reflected image of the top-left quadrant.
The bottom-left quadrant of the output is a horizontally reflected image of the top-left quadrant.
The bottom-right quadrant is both a horizontally and vertically reflected image of the top-left, which is equivalent to a 180-degree rotation.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_array = np.array(input_grid)
    rows, cols = input_array.shape
    output_array = np.zeros((rows * 2, cols * 2), dtype=int)

    # Copy the original grid to top-left
    output_array[:rows, :cols] = input_array

    # Vertical reflection to top-right
    output_array[:rows, cols:] = np.flip(input_array, axis=1)

    # Horizontal reflection to bottom-left
    output_array[rows:, :cols] = np.flip(input_array, axis=0)

    # Horizontal and vertical reflection (180 rotation) to bottom-right
    output_array[rows:, cols:] = np.flip(np.flip(input_array, axis=0), axis=1)
    
    return output_array.tolist()