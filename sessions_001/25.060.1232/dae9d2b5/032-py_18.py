"""
Condenses the input grid into a 3x3 output grid, preserving the relative configuration of non-white objects. Non-white pixels in the input are represented by magenta (6) pixels in the output, maintaining their relative positions within a 3x3 grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as 3x3 with all white (0) pixels.
    output_grid = np.zeros((3, 3), dtype=int)
    rows, cols = input_grid.shape

    # Define the boundaries of the 3x3 regions in the input grid.
    row_thirds = np.linspace(0, rows, 4, dtype=int)
    col_thirds = np.linspace(0, cols, 4, dtype=int)

    # Check for non-white pixels in the top-center region.
    for r in range(row_thirds[0], row_thirds[1]):
        for c in range(col_thirds[1], col_thirds[2]):
            if input_grid[r, c] != 0:
                output_grid[0, 1] = 6
                break
        else:
            continue
        break

    # Check for non-white pixels in the center-center region
    for r in range(row_thirds[1], row_thirds[2]):
        for c in range(col_thirds[1], col_thirds[2]):
            if input_grid[r,c] != 0:
                output_grid[1,1] = 6
                break
        else:
            continue
        break

    # Check for non-white pixels in the bottom-left region.
    for r in range(row_thirds[2], row_thirds[3]):
        for c in range(col_thirds[0], col_thirds[1]):
            if input_grid[r, c] != 0:
                output_grid[2, 0] = 6
                break
        else:
            continue
        break

    # Check for non-white pixels in the bottom-center region.
    for r in range(row_thirds[2], row_thirds[3]):
        for c in range(col_thirds[1], col_thirds[2]):
            if input_grid[r, c] != 0:
                output_grid[2, 1] = 6
                break
        else:
            continue
        break

    # Check for non-white pixels in the bottom-right region.
    for r in range(row_thirds[2], row_thirds[3]):
        for c in range(col_thirds[2], col_thirds[3]):
            if input_grid[r, c] != 0:
                output_grid[2, 2] = 6
                break
        else:
            continue
        break

    return output_grid