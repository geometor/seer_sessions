"""
The transformation involves identifying a rectangular blue border within the grid. 
Inside this border, specific colored objects (non-white, non-blue pixels) are present. 
The transformation rearranges these inner objects by mirroring their positions across both the horizontal and vertical axes of symmetry within the border.
"""

import numpy as np

def find_border(grid):
    # Find the coordinates of the blue border (color 1).
    rows, cols = np.where(grid == 1)
    if len(rows) == 0:  # No blue border found.
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, max_row, min_col, max_col)

def find_inner_objects(grid, border):
    # Find the positions and colors of inner objects within the border.
    min_row, max_row, min_col, max_col = border
    inner_objects = []
    for r in range(min_row + 1, max_row):
        for c in range(min_col + 1, max_col):
            if grid[r, c] != 0 and grid[r, c] != 1:  # Not white and not blue.
                inner_objects.append(((r, c), grid[r, c]))
    return inner_objects

def mirror_position(pos, border):
    # Calculate mirrored position within the border.
    min_row, max_row, min_col, max_col = border
    row_center = (min_row + max_row) / 2
    col_center = (min_col + max_col) / 2
    mirrored_row = int(2 * row_center - pos[0])
    mirrored_col = int(2 * col_center - pos[1])
    return (mirrored_row, mirrored_col)
    

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)
    
    # Find the blue border.
    border = find_border(output_grid)
    if border is None:
        return output_grid  # No border found, return original grid.

    # Find inner objects.
    inner_objects = find_inner_objects(output_grid, border)

    # Clear original positions of inner objects in the output grid.
    for (row, col), _ in inner_objects:
      output_grid[row, col] = 0

    # Place inner objects at their mirrored positions.
    for (row, col), color in inner_objects:
        mirrored_pos = mirror_position((row, col), border)
        output_grid[mirrored_pos] = color
    
    return output_grid