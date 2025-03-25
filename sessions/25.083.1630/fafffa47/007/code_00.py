"""
Transforms the top section of the input_grid into a 3x3 output_grid.
Maroon (9) pixels in the top section of the input become red (2) pixels in the output.
The bottom section of the input_grid (containing blue pixels) is ignored.
The output grid is always 3x3.
The positions of red pixels in the output are determined by the positions of the maroon pixels, using the transformation:
output_grid[r][c] = 2 if input_grid contains 9 at position [(c, rows_top_section - r - 1)]
and 0 elsewhere.
"""

import numpy as np

def get_top_section(grid):
    """
    Extracts the top section of the input grid, which contains only 0s and 9s.
    """
    rows, cols = grid.shape
    top_section = []
    for r in range(rows):
        row = grid[r]
        if np.any(row == 1):  # Stop when a blue pixel is encountered
            break
        top_section.append(row)
    return np.array(top_section)

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    top_section = get_top_section(input_grid)
    output_grid = np.zeros((3, 3), dtype=int)
    rows_top_section = top_section.shape[0]

    # change output pixels
    for r in range(3):
        for c in range(3):
            if rows_top_section > 0: # Ensure top_section is not empty
                r_in = c
                c_in = rows_top_section - r -1
                if 0 <= r_in < top_section.shape[0] and 0 <= c_in < top_section.shape[1]:
                    if top_section[r_in, c_in] == 9:
                        output_grid[r,c] = 2

    return output_grid