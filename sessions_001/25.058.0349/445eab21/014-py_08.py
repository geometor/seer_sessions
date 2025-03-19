"""
1.  Identify the bounding box of the yellow (4) "C" shape within the input grid.
2.  Identify the upper-left corner of the c shape bounding box.
3.  Extract a 2x2 subgrid from the input grid, starting at the yellow C shape's top-left corner.
4.  The extracted 2x2 subgrid is the output. Ignore all other parts of the input grid.
"""

import numpy as np

def find_object_bounding_box(grid, color):
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # Color not found in the grid
    top_left = (min(rows), min(cols))
    bottom_right = (max(rows), max(cols))
    return top_left, bottom_right

def transform(input_grid):
    # Find the bounding box of the yellow (4) C shape.
    yellow_color = 4
    bounding_box = find_object_bounding_box(np.array(input_grid), yellow_color)
    
    if bounding_box is None:
        return [[]] # returns an empty grid if no yellow is found
        
    top_left, _ = bounding_box

    # Extract a 2x2 subgrid starting at the top-left corner of the bounding box.
    row_start, col_start = top_left
    output_grid = []
    for i in range(2):
        row = []
        for j in range(2):
            if row_start + i < len(input_grid) and col_start + j < len(input_grid[0]):
                row.append(input_grid[row_start + i][col_start + j])
            else:
              row.append(0) # pad with zero if out of bounds
        output_grid.append(row)

    return output_grid