"""
The input grid is transformed into the output grid by rotating it 90 degrees clockwise, then computing the transpose.
Equivalently, reflect the input across the main diagonal. The colors of the pixels are preserved.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to numpy array
    input_np = np.array(input_grid)

    # Rotate the grid 90 degrees clockwise
    rotated_grid = np.rot90(input_np, k=-1)

    # Transpose the rotated grid
    output_np = rotated_grid.T
    
    # Convert the numpy array back to a list
    output_grid = output_np.tolist()

    return output_grid