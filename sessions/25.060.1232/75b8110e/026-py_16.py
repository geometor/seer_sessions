"""
The transformation identifies a diagonal line of non-zero pixels in the input grid and extracts it into the output grid. The length and position of the diagonal vary. If the identified diagonal has fewer than 4 elements, the missing cells in the 3x3 output should be filled by black, otherwise the full shape of the diagonal should be preserved in the output.
"""

import numpy as np

def find_longest_diagonal(grid):
    """
    Finds the longest diagonal of non-zero pixels, considering both directions (top-left to bottom-right and top-right to bottom-left).
    """
    rows, cols = grid.shape
    longest_diag = []

    # Helper function to get diagonal elements
    def get_diagonal(start_row, start_col, row_dir, col_dir):
        diag = []
        r, c = start_row, start_col
        while 0 <= r < rows and 0 <= c < cols:
            if grid[r, c] != 0:
                diag.append((r, c, grid[r,c]))
            else:
                break # stop when hit 0
            r += row_dir
            c += col_dir
        return diag

    # Check diagonals from top-left to bottom-right
    for r in range(rows):
        diag = get_diagonal(r, 0, 1, 1)
        if len(diag) > len(longest_diag):
            longest_diag = diag
    for c in range(1, cols):
        diag = get_diagonal(0, c, 1, 1)
        if len(diag) > len(longest_diag):
            longest_diag = diag

    # Check diagonals from top-right to bottom-left
    for r in range(rows):
        diag = get_diagonal(r, cols - 1, 1, -1)
        if len(diag) > len(longest_diag):
            longest_diag = diag
    for c in range(cols - 2, -1, -1):
        diag = get_diagonal(0, c, 1, -1)
        if len(diag) > len(longest_diag):
            longest_diag = diag
            
    return longest_diag

def transform(input_grid):
    # initialize input_grid
    input_grid = np.array(input_grid)

    # find longest diagonal
    longest_diag = find_longest_diagonal(input_grid)

    # determine output grid size and initialize
    if not longest_diag:
        return [[0,0,0],[0,0,0],[0,0,0]]

    output_size = max(len(longest_diag),3) if len(longest_diag) <= 4 else len(longest_diag) #should not exceed 4 if shape is 3x3

    output_grid = np.zeros((output_size, output_size), dtype=int)

    # copy diagonal to output, centered
    start_index = 0

    for i in range(len(longest_diag)):
        _, _, val = longest_diag[i]
        output_grid[start_index + i, i] = val

    return output_grid.tolist()