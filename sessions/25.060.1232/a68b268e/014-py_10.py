"""
The transformation identifies the largest uniform color blocks anchored to the top-left and bottom-right of the input grid. It extracts the colors from the top-left corner of the top-left block and the top-left and bottom-right corners of the bottom-right block. These colors are then used to construct a 4x4 output grid. The first column is filled with the top-left block's top-left corner color. The second and fourth columns are filled with top-left and bottom-right colors, respectively, from the bottom-right block. Empty cells in the output grid are filled with 0.
"""

import numpy as np

def find_uniform_block(grid, start_row, start_col):
    """Finds the largest uniform color block starting from a given position."""
    color = grid[start_row, start_col]
    rows, cols = grid.shape
    end_row = start_row
    end_col = start_col

    # Expand rightwards
    while end_col + 1 < cols and grid[start_row, end_col + 1] == color:
        end_col += 1

    # Expand downwards
    while end_row + 1 < rows:
        valid_row = True
        for c in range(start_col, end_col + 1):
            if grid[end_row + 1, c] != color:
                valid_row = False
                break
        if valid_row:
            end_row += 1
        else:
            break

    return (start_row, start_col), (end_row, end_col)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((4, 4), dtype=int)
    input_grid = np.array(input_grid)

    # Find top-left uniform block
    top_left_start, _ = find_uniform_block(input_grid, 0, 0)
    top_left_color = input_grid[top_left_start[0], top_left_start[1]]

    # Find bottom-right uniform block
    rows, cols = input_grid.shape
    _, bottom_right_end = find_uniform_block(input_grid, rows -1, cols - 1)
    
    # handle cases where the identified block only contains one element
    bottom_right_start_row = 0
    bottom_right_end_row = 0
    for r in range(rows):
        if input_grid[r, bottom_right_end[1]] == input_grid[bottom_right_end[0], bottom_right_end[1]]:
            bottom_right_start_row = r
            break;
    
    for r in range(rows - 1, -1, -1):
        if input_grid[r, bottom_right_end[1]] == input_grid[bottom_right_end[0], bottom_right_end[1]]:
           bottom_right_end_row = r
           break

    bottom_right_top_left_color = input_grid[bottom_right_start_row, bottom_right_end[1]]    
    bottom_right_bottom_right_color = input_grid[bottom_right_end_row, bottom_right_end[1]]
    

    # Construct output grid
    output_grid[:, 0] = top_left_color  # Fill first column
    output_grid[0::2, 1] = bottom_right_top_left_color # Fill second column (even rows)
    output_grid[1::2, 1] = 0
    
    output_grid[0::2, 3] = bottom_right_bottom_right_color # Fill fourth column (even rows)
    output_grid[1::2, 3] = 0

    return output_grid