"""
The transformation rule involves identifying yellow objects and adding red pixels based on their position relative to the grid boundaries. If a yellow object touches a boundary, a mirrored copy of the object (in red) is created on the opposite side of the grid. If the yellow object doesn't touch any boundary, it's extended in two opposite directions by creating a red copy of the object shape at the minimum and maximum rows or columns.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous objects of a specified color in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
        """Depth-First Search to find contiguous pixels."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return

        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)

    return objects

def reflect_or_extend(grid, yellow_object):
    """
    Reflects the object if it touches a boundary, extends it otherwise.
    """
    output_coords = []

    # Check if the object touches the boundary, collect info
    top_touch, bottom_touch, left_touch, right_touch = False, False, False, False
    min_row = min(y for y,x in yellow_object)
    max_row = max(y for y,x in yellow_object)
    min_col = min(x for y,x in yellow_object)
    max_col = max(x for y,x in yellow_object)
    if min_row == 0:
        top_touch = True
    if max_row == grid.shape[0] - 1:
        bottom_touch = True
    if min_col == 0:
        left_touch = True
    if max_col == grid.shape[1] -1:
        right_touch = True

    # mirror at boundary
    if top_touch:
        for y, x in yellow_object:
            output_coords.append( (grid.shape[0]-1 - (y-min_row), x) )
    if bottom_touch:
        for y, x in yellow_object:
            output_coords.append( (min_row - 1- (y - max_row) , x) ) # use min_row for offset
    if left_touch:
        for y, x in yellow_object:
            output_coords.append( (y, grid.shape[1]-1 - (x - min_col) ) )
    if right_touch:
        for y, x in yellow_object:
            output_coords.append( (y, min_col - 1 - (x-max_col)) )

    # if not on boundary, then pick the two sides which maximizes distance to a boundary
    if not (top_touch or bottom_touch or left_touch or right_touch):

        # calculate distance to each boundary
        dist_top = min_row
        dist_bottom = grid.shape[0] - 1 - max_row
        dist_left = min_col
        dist_right = grid.shape[1] - 1 - max_col

        # extend in the two directions of largest distance
        distances = [ ("top",dist_top), ("bottom",dist_bottom), ("left", dist_left), ("right", dist_right)]
        distances.sort(key=lambda x: x[1], reverse=True)
        direction1 = distances[0][0]
        direction2 = distances[1][0]

        if "top" == direction1 or "top" == direction2:
            for y, x in yellow_object:
                output_coords.append( (min_row - 1 - (y-min_row), x) )  # extend above
        if "bottom" == direction1 or "bottom" == direction2:
            for y, x in yellow_object:
               output_coords.append( (max_row + 1 + (y - min_row), x) )  # extend below
        if "left" == direction1 or "left" == direction2:
            for y, x in yellow_object:
                output_coords.append( (y, min_col - 1 - (x - min_col)) ) # extend left
        if "right" == direction1 or "right" == direction2:
            for y, x in yellow_object:
                output_coords.append( (y, max_col + 1 + (x - min_col)) )   # extend right
    return output_coords
            

def transform(input_grid):
    """
    Identifies yellow objects and adds red pixels that reflect or expand 
    related to the yellow objects, considering grid boundaries.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find yellow objects
    yellow_objects = find_objects(input_grid, 4)

    # For each yellow object, add reflected/extended red pixels
    for yellow_object in yellow_objects:
        red_coords = reflect_or_extend(input_grid, yellow_object)
        for r, c in red_coords:
            if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:  # Boundary check
                output_grid[r, c] = 2

    return output_grid