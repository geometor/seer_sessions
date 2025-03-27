"""
Transforms an input grid by mirroring objects across a central blue line and recoloring some of them.
"""

import numpy as np

def find_blue_line(grid):
    # Find the row index of the horizontal blue line (all 1s)
    for i, row in enumerate(grid):
        if np.all(row == 1):
            return i
    return -1  # Return -1 if no blue line is found

def get_objects(grid):
    """
    Identifies contiguous objects in the grid.
    Returns a list of objects, where each object is a list of (row, col) tuples.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                if current_object:
                    objects.append(current_object)
    return objects



def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Find the blue line
    blue_line_row = find_blue_line(input_grid)

    # Get objects
    objects = get_objects(input_grid)

    # Mirror and recolor
    if blue_line_row != -1:
        for obj in objects:
            for r, c in obj:
                if r < blue_line_row: # Above the blue line
                    dist = blue_line_row - r
                    new_r = blue_line_row + dist

                    if new_r < rows: # prevent out of range
                        #simple mirror
                        output_grid[new_r,c] = input_grid[r,c]
                elif r > blue_line_row: # below the blue line
                    dist = r - blue_line_row
                    new_r = blue_line_row - dist
                    if new_r > 0:  # prevent out of range
                       #simple mirror
                       output_grid[new_r,c] = input_grid[r,c]


    return output_grid