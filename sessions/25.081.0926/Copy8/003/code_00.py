"""
The transformation rule involves identifying contiguous blocks of non-zero colored pixels (objects) in the input grid.
Isolated pixels of color 3 are duplicated to the right of the rightmost contiguous block of color 4.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies and returns a list of objects in the grid.
    Each object is represented by a list of (row, col) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape
    
    def dfs(row, col, current_object):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] == 0:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append((grid[r,c],current_object)) # save value with the object
    return objects

def find_isolated_pixels(grid, color):
    """Finds isolated pixels of a given color."""
    isolated = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] == color:
                # Check if isolated (above and below are 0 or out of bounds)
                is_isolated = True
                if r > 0 and grid[r-1, c] != 0:
                    is_isolated = False
                if r < rows - 1 and grid[r+1, c] != 0:
                    is_isolated = False
                if is_isolated:
                    isolated.append((r, c))
    return isolated
                    
def find_rightmost_block_column(grid, color):
    """Finds the rightmost column of a contiguous block of the given color."""
    objects = get_objects(grid)
    rightmost_column = -1
    
    for obj_color, obj_coords in objects:
        if obj_color == color:
            cols = [c for _, c in obj_coords]
            if cols:
                max_col = max(cols)
                if max_col > rightmost_column:
                    rightmost_column = max_col
    return rightmost_column
    

def transform(input_grid):
    """
    Transforms the input grid according to the rule: 
    Isolated pixels of color 3 are duplicated to the right of the rightmost contiguous object of color 4.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    
    # Find isolated pixels of color 3
    isolated_pixels_3 = find_isolated_pixels(input_grid, 3)

    #find the rightmost block of color 4
    rightmost_col_4 = find_rightmost_block_column(input_grid, 4)
    
    
    # Duplicate isolated pixels of color 3
    for r, c in isolated_pixels_3:
        target_col = rightmost_col_4 + (c - rightmost_col_4) if rightmost_col_4 >0 else c # handle no color 4
        if target_col+1 < output_grid.shape[1]:            
             output_grid[r,target_col+1 ] = 3

    return output_grid