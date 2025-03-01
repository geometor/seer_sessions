"""
Transforms an input grid based on the following rules:

1. Create the output grid with all white first.

2. Iterate input pixels.
    * If the pixel is blue(1)
    *   If this blue pixel forms part of the 1x3 or 3x1 blue block then paint this pixel to red, otherwise, if there are no adjacent blue pixels, keep the pixel blue.
    *    If this blue pixel creates a corner on 3x3 block, paint the corner to red.

3. If the pixel is white(0). Check its neighbors.
    *   If the white pixel is next to a blue pixel vertically, or horizontally. Copy the blue pixel to output.
    *   If the white pixel is next to a red pixel vertically, or horizontally. Copy the red pixel to output.
    *   If the white pixel is next to both red and blue, perform the above check twice, in that order.
"""

import numpy as np

def is_within_bounds(grid, r, c):
    rows, cols = grid.shape
    return 0 <= r < rows and 0 <= c < cols

def get_neighbors(grid, r, c):
    neighbors = []
    rows, cols = grid.shape
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if is_within_bounds(grid, nr, nc):
            neighbors.append((nr, nc))
    return neighbors

def check_blue_block(grid, r, c):
    # check for 1x3 or 3x1 blue block
    horizontal_count = 0
    vertical_count = 0
    
    #check horizontal
    if is_within_bounds(grid, r, c-1) and grid[r,c-1] == 1:
        horizontal_count +=1
    if is_within_bounds(grid, r, c+1) and grid[r,c+1] == 1:
        horizontal_count +=1

    # Check vertical
    if is_within_bounds(grid, r-1, c) and grid[r-1, c] == 1:
        vertical_count += 1
    if is_within_bounds(grid, r+1, c) and grid[r+1, c] == 1:
        vertical_count += 1
        
    return horizontal_count == 2 or vertical_count == 2
    
def check_3x3_corner(grid, r, c):
    for dr in [-1, 1]:
        for dc in [-1, 1]:
            count = 0
            for i in range(3):
                for j in range(3):
                    row = r + dr * i
                    col = c + dc * j
                    if is_within_bounds(grid, row,col) and (row,col) != (r,c):
                        if grid[row,col] == 1:
                            count +=1
            if count == 8: # this blue is the corner cell of a 3x3 block.
              return True
    return False

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # change output pixels 
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 1:
                if check_blue_block(input_grid, r, c) or check_3x3_corner(input_grid,r,c):
                    output_grid[r, c] = 2
                else:
                    output_grid[r,c] = 1

    for r in range(rows):
        for c in range(cols):
            if input_grid[r,c] == 0:
                for nr, nc in get_neighbors(input_grid, r, c):
                    if input_grid[nr,nc] == 1:
                        output_grid[r,c] = 1
                    
    for r in range(rows):
        for c in range(cols):
            if input_grid[r,c] == 0:            
                for nr, nc in get_neighbors(input_grid, r, c):
                    if output_grid[nr,nc] == 2:
                        output_grid[r,c] = 2

    return output_grid