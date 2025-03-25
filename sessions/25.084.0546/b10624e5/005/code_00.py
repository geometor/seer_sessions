"""
Transforms an input grid by mirroring objects across a central blue line and
recoloring/shifting some of them. Objects are mirrored based on their distance
from the blue line. Specific recoloring and shifting rules are applied based on
the object's original color and position relative to the blue line.
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
    output_grid = np.copy(input_grid) # Start with a copy of the input
    rows, cols = input_grid.shape

    # Find the blue line
    blue_line_row = find_blue_line(input_grid)
    if blue_line_row == -1:
        return input_grid  # Return original if no blue line

    # Get objects
    objects = get_objects(input_grid)

    # Mirror and recolor/shift
    for obj in objects:
        # Skip the blue line itself
        if all(input_grid[r, c] == 1 for r, c in obj):
            continue

        for r, c in obj:
            original_color = input_grid[r,c]

            if r < blue_line_row:  # Above the blue line
                dist = blue_line_row - r
                new_r = blue_line_row + dist

                if new_r < rows: # prevent out of range
                    output_grid[new_r, c] = original_color # default mirror

                    # Specific color/shifting rules
                    if original_color == 3:
                        output_grid[new_r, c] = 3
                        if new_r < rows-1:
                           output_grid[new_r + 1, c] = 3  # shift down by one
                    elif original_color == 2:
                        output_grid[new_r, c] = 2


            elif r > blue_line_row:  # Below the blue line
                dist = r - blue_line_row
                new_r = blue_line_row - dist
                if new_r >=0:
                   output_grid[new_r,c] = original_color

                   if original_color == 3 :
                      output_grid[new_r,c] = 3
                      if new_r > 0:
                         output_grid[new_r - 1, c] = 3  # Shift up by one

                   elif original_color == 2:
                        output_grid[new_r,c] = 2


    return output_grid