"""
1. Preserve the Frame: Keep the outer frame of the grid (color 6) unchanged in the output.
2. Identify non-white/magenta rows: The first appearance of any combination of colors that are not white (0) or magenta (6)
3. Replicate identified row: Duplicate the content, excluding the frame, down until another row that is not white is reached, or the last interior row.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the first row with non-white/magenta pixels in interior
    replication_row = None
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if input_grid[i][j] != 0 and input_grid[i][j] != 6:
                replication_row = i
                break  # only want the first such row
        if replication_row is not None:
           break

    # If found row to replicate, start duplicating the interior
    if replication_row is not None:
        for i in range(replication_row + 1, rows -1):
            output_grid[i, 1:cols-1] = output_grid[replication_row, 1:cols-1]

    return output_grid