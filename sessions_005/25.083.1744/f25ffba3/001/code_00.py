"""
The transformation takes the movement path of a 1x4 colored block, reverses it, and uses that reversed path to construct the output.
"""

import numpy as np

def find_colored_block(grid):
    # Iterate through rows to find the colored block (1x4 horizontal line)
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols - 3):
            if len(set(grid[r, c:c+4])) == 4: #four unique colors
                return r, c, grid[r, c:c+4]
    return None, None, None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape
    
    # Find the colored block's starting row and colors
    start_row, start_col, colors = find_colored_block(input_grid)

    if start_row is None:
        return output_grid  # Return empty grid if no block is found

    # Extract the path of the colored block (rows where it appears)
    path_rows = []
    for r in range(rows):
        if (input_grid[r, start_col:start_col + 4] == colors).all():
          path_rows.append(r)

    # Reflect the path and create output
    reflected_path = path_rows[::-1]

    # combining forward and reverse paths
    fill_rows = reflected_path + path_rows[1:]

    #filling output
    output_row_index = 0
    while output_row_index < len(output_grid):
        for path_row in fill_rows:
            if output_row_index < len(output_grid):
                output_grid[output_row_index,start_col:start_col+4] = colors
                output_row_index +=1
            else:
              break

    return output_grid