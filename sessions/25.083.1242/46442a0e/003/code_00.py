"""
The transformation takes the input grid and creates a 2x2 larger grid where each quadrant is a mirrored version of the input:

*   Top-Left: Original Input
*   Top-Right: Horizontally mirrored Input
*   Bottom-Left: Vertically mirrored Input
*   Bottom-Right: Diagonally mirrored Input (or both H and V mirrored)
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_np = np.array(input_grid)
    rows, cols = input_np.shape
    output_rows = rows * 2
    output_cols = cols * 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Top-Left: Original Input
    output_grid[:rows, :cols] = input_np

    # Top-Right: Horizontally mirrored Input
    output_grid[:rows, cols:] = np.flip(input_np, axis=1)

    # Bottom-Left: Vertically mirrored Input
    output_grid[rows:, :cols] = np.flip(input_np, axis=0)

    # Bottom-Right: Diagonally mirrored Input
    output_grid[rows:, cols:] = np.flip(input_np, axis=(0, 1))

    return output_grid.tolist()