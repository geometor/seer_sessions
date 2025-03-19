"""
1.  **Identify** the vertical gray bar.
2.  **Identify** shape1: For each example, shape1 consists of the colored pixels that are *not* blue or gray.
3.  **Copy** shape1 to create shape2.
4.  **Translate** shape2: Place shape2 to the immediate right of the gray bar.  The top of shape2 should align with the bottom of the gray bar, if the gray bar extends to the bottom of the input, then shape2 aligns to the top of the gray bar.
5.  **Remove** all blue pixels from the grid.
6.  **Keep** the gray bar in its original position.
"""

import numpy as np

def find_gray_bar(grid):
    """Finds the column index of the vertical gray bar."""
    rows, cols = grid.shape
    for c in range(cols):
        if all(grid[r, c] == 5 for r in range(rows)):
            return c
    return -1  # Return -1 if no gray bar is found

def find_shape(grid, gray_bar_col):
    """Finds the coordinates of a shape defined by non-blue, non-gray pixels."""
    rows, cols = grid.shape
    shape_coords = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 1 and grid[r,c] != 5:
                shape_coords.append((r, c))
    return shape_coords

def translate_shape(coords, row_offset, col_offset):
    """Translates a set of coordinates by given offsets."""
    return [(r + row_offset, c + col_offset) for r, c in coords]

def remove_color(grid, color):
    """Removes all pixels of a specified color from the grid."""
    rows, cols = grid.shape
    new_grid = np.copy(grid)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == color:
                new_grid[r][c] = 0
    return new_grid

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Identify the vertical gray bar
    gray_bar_col = find_gray_bar(input_grid)

    # Identify shape1 (all non-blue, non-gray pixels)
    shape1_coords = find_shape(input_grid, gray_bar_col)

    # Copy shape1 to create shape2
    shape2_coords = shape1_coords.copy()
    
    #fill original shape into output
    for r, c in shape1_coords:
      output_grid[r,c] = input_grid[r,c]

    # Determine row offset for shape2 translation
    gray_bar_height = input_grid.shape[0]
    if gray_bar_col != -1:
        gray_bar_bottom = gray_bar_height
        row_offset = gray_bar_bottom - shape1_coords[0][0]

        #if gray bar is at the bottom, offset to the top of the bar
        if gray_bar_bottom == input_grid.shape[0]:
            #get top of gray bar
            for r in range(input_grid.shape[0]):
              if input_grid[r, gray_bar_col] == 5:
                gray_bar_top = r
                break
            row_offset = gray_bar_top - shape1_coords[0][0]

    else:
        row_offset = 0
    
    #always put next to right of gray_bar
    col_offset = gray_bar_col - shape1_coords[0][1] + 1 if gray_bar_col != -1 else 0

    # Translate shape2
    shape2_coords = translate_shape(shape2_coords, row_offset, col_offset)


    #fill translated shape into output
    for r, c in shape2_coords:
      #make sure to stay in grid, the shape can be clipped
      if r < output_grid.shape[0] and c < output_grid.shape[1]:
        output_grid[r, c] = input_grid[r-row_offset, c-col_offset]


    # Keep the gray bar
    if gray_bar_col != -1:
        for r in range(output_grid.shape[0]):
            output_grid[r, gray_bar_col] = 5

    # Remove blue pixels
    output_grid = remove_color(output_grid, 1)

    return output_grid