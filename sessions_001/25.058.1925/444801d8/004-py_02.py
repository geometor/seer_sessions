"""
Identifies a blue shape in the input grid and fills the area it encloses, starting from a seed red pixel, with red.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    return coords

def flood_fill(grid, start_row, start_col, target_color, replacement_color):
    """Performs a flood fill, replacing target_color with replacement_color."""
    rows, cols = grid.shape
    if not (0 <= start_row < rows and 0 <= start_col < cols):
        return  # Out of bounds

    if grid[start_row, start_col] != target_color:
        return  # Not the target color

    grid[start_row, start_col] = replacement_color
    # Recursively fill adjacent pixels
    flood_fill(grid, start_row + 1, start_col, target_color, replacement_color)
    flood_fill(grid, start_row - 1, start_col, target_color, replacement_color)
    flood_fill(grid, start_row, start_col + 1, target_color, replacement_color)
    flood_fill(grid, start_row, start_col - 1, target_color, replacement_color)

def is_within_blue_shape(grid, row, col, blue_coords):
    # Check if the position is within blue shape using flood fill approach.
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    
    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols
    
    def dfs(r,c):
       
        if not is_valid(r,c) or visited[r,c] or grid[r,c] == 1:
            return True
        
        if grid[r,c] == 0 and (r == 0 or c == 0 or r == rows-1 or c == cols -1):
            return False
        
        visited[r,c] = True

        return dfs(r + 1, c) and dfs(r - 1, c) and dfs(r, c + 1) and dfs(r, c - 1)


    return dfs(row,col)



def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find the red pixel (seed).
    red_coords = find_object(input_grid, 2)
    if len(red_coords) == 0:
       return output_grid # if no red pixel return grid
    
    red_row, red_col = red_coords[0]

    # find the blue pixels
    blue_coords = find_object(input_grid, 1)
    if len(blue_coords) == 0:
        return output_grid # if no blue pixels, return grid

    # Expand the fill to cover any white pixels within.
    rows, cols = output_grid.shape
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 0 and is_within_blue_shape(output_grid,r,c, blue_coords):
                output_grid[r,c] = 2
    
    output_grid[red_row, red_col] = 2 #ensure that original red pixel stays red, even with simplified shape check

    return output_grid