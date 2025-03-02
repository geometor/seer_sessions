"""
The transformation extracts the bottom-right 4x4 non-zero colored subgrid from input and presents in the output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((4, 4), dtype=int)

    # Focus Area: Extract a sub-grid that is size 4x4 aligned with the bottom right of input.
    sub_grid = input_grid[rows-4:, cols-4:]

    # Preserve Colors: Within the selected area, maintain the existing colors (which are already non-zero).
    output_grid[:] = sub_grid
    
    return output_grid.tolist()