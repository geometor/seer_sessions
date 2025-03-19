"""
1. **Identify Corners:** Locate the yellow (4) pixels in the four corners of the *input* grid. These will define the corners of the smaller, *output* grid. If corner pixels of value 4 do not exist, ignore this rule.

2. **Determine Output Dimensions:** The output grid's dimensions are defined by drawing horizontal and vertical lines between opposite yellow corner pixels. If there are no yellow corners, the output size is the minimum rectangle enclosing all non-zero pixels.

3. **Summarize Vertical Stems:** For each non-zero, non-corner column in the input, identify contiguous vertical "stems" of the same color.  A "stem" is a vertical sequence of one or more pixels of the same color.

4. **Place Stems in Output:**  Represent each identified stem within the output grid's corresponding column.
    - The stem is represented by the same color.
    - Replicate that color in the *output* grid, filling a rectangle in the output column. The rectangle fills the whole column, except the top and bottom row if yellow pixels were present.

5. **Preserve corner elements**: replicate the yellow pixels in the corners to the output grid.
"""

import numpy as np

def find_corners(grid):
    """Finds the coordinates of yellow (4) corner pixels."""
    corners = []
    rows, cols = grid.shape
    if grid[0, 0] == 4:
        corners.append((0, 0))
    if grid[0, cols - 1] == 4:
        corners.append((0, cols - 1))
    if grid[rows - 1, 0] == 4:
        corners.append((rows - 1, 0))
    if grid[rows - 1, cols - 1] == 4:
        corners.append((rows - 1, cols - 1))
    return corners

def find_bounding_box(grid):
    """Finds the smallest rectangle enclosing all non-zero pixels."""
    rows, cols = grid.shape
    min_row, min_col = rows, cols
    max_row, max_col = 0, 0

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                min_row = min(min_row, r)
                min_col = min(min_col, c)
                max_row = max(max_row, r)
                max_col = max(max_col, c)
    return min_row, min_col, max_row, max_col

def get_stems(grid, col):
    stems = []
    rows = grid.shape[0]
    in_stem = False
    stem_color = 0
    
    for row in range(rows):
      if grid[row,col] != 0:
        if in_stem:
          if grid[row,col] != stem_color:
            in_stem = True
            stem_color = grid[row,col]
            
        else:
          in_stem = True
          stem_color = grid[row,col]
      else:
        in_stem = False
        stem_color = 0

    # build the stem list - this works by setting instem true/false above, 
    # then we create an array of that same color for each column in the final step
    in_stem = False
    stem_color = 0
    for row in range(rows):
        if grid[row, col] != 0:
            if in_stem:
                if grid[row, col] != stem_color:
                    stems.append((stem_color, start_row, row -1))
                    in_stem = True
                    stem_color = grid[row, col]
                    start_row = row
            else:
                in_stem = True
                stem_color = grid[row, col]
                start_row = row
        else:
            if in_stem:
                stems.append((stem_color, start_row, row - 1))
            in_stem = False
    if in_stem:
        stems.append((stem_color, start_row, rows-1))
    
    return stems

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    input_grid = np.array(input_grid)
    corners = find_corners(input_grid)
    
    if len(corners) == 4:
        # Determine output dimensions based on corners
        min_row, min_col = 0, 0 #corners[0]
        max_row, max_col = corners[3] # Assuming corners are in tl, tr, bl, br order
        output_rows = max_row - min_row + 1
        output_cols = max_col-min_col + 1
        output_grid = np.zeros((output_rows, output_cols), dtype=int)
        
        # Place corner pixels
        output_grid[0, 0] = 4
        output_grid[0, output_cols - 1] = 4
        output_grid[output_rows - 1, 0] = 4
        output_grid[output_rows - 1, output_cols - 1] = 4

        # skip first and last column in input_grid
        for c in range(min_col + 1, max_col):
          stems = get_stems(input_grid,c)
          
          # skip first and last row
          for color, s, e in stems:
            output_col_index = c-min_col
            
            output_grid[1:output_rows-1, output_col_index] = color

    else:
        # Determine output dimensions based on bounding box
        min_row, min_col, max_row, max_col = find_bounding_box(input_grid)
        output_rows = max_row - min_row + 1
        output_cols = max_col - min_col + 1
        output_grid = np.zeros((output_rows, output_cols), dtype=int)
        
        for c in range(min_col, max_col + 1):
            stems = get_stems(input_grid, c)
            for color, s, e in stems:
                output_col_index = c - min_col
                output_grid[:, output_col_index] = color # fill the whole column

    return output_grid