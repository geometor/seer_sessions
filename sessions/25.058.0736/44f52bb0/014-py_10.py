"""
Finds the object intersecting the vertical center line of the input grid,
and counts the number of pixels of that object's color on the left side
of the dividing line. If no object intersects the center line, counts pixels
of the first object found on the left side. Outputs the count in a 1x1 grid.
"""

import numpy as np

def find_objects(input_grid):
    """
    Finds all contiguous objects in a grid.
    Returns a list of (color, size, bounding_box) tuples.
    bounding_box is ((min_row, max_row), (min_col, max_col))
    """
    objects = []
    visited = np.zeros_like(input_grid, dtype=bool)

    def dfs(row, col, color):
        if (row < 0 or row >= input_grid.shape[0] or col < 0 or col >= input_grid.shape[1]
                or visited[row, col] or input_grid[row, col] != color):
            return 0, (row, row), (col, col)  # Return 0 and identity bounding box
        visited[row, col] = True
        count = 1
        min_row, max_row = row, row
        min_col, max_col = col, col

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = row + dr, col + dc
            size, (nr1, nr2), (nc1, nc2) = dfs(new_row, new_col, color)
            count += size
            min_row = min(min_row, nr1, new_row)  # Update min_row
            max_row = max(max_row, nr2, new_row) # Update max_row
            min_col = min(min_col, nc1, new_col) # Update min_col
            max_col = max(max_col, nc2, new_col) # Update max_col

        return count, (min_row, max_row), (min_col, max_col)

    for row in range(input_grid.shape[0]):
        for col in range(input_grid.shape[1]):
            if not visited[row, col]:
                color = input_grid[row, col]
                size, (min_row, max_row), (min_col, max_col) = dfs(row, col, color)
                if size > 0:
                    objects.append((color, size, ((min_row, max_row), (min_col, max_col))))
    return objects

def transform(input_grid):
    """
    Transforms the grid by finding object, determining intersection with
    vertical center line and returning half the object size or checking
    left side for objects
    """
    # Find all objects
    objects = find_objects(input_grid)

    # find vertical center line
    center_col = input_grid.shape[1] // 2

    # Find the object intersected by the center line
    intersected_object = None

    for obj_color, obj_size, ((min_row, max_row), (min_col, max_col)) in objects:
        if min_col <= center_col <= max_col:
            intersected_object = (obj_color, obj_size, ((min_row, max_row), (min_col, max_col)))
            break  # Stop after finding the FIRST intersecting object

    # Count pixels on the left side
    count = 0
    if intersected_object is not None:
        obj_color = intersected_object[0]
        for r in range(input_grid.shape[0]):
            for c in range(center_col):
                if input_grid[r,c] == obj_color:
                    count += 1

    else: # check for left side objects
        for obj_color, obj_size, ((min_row, max_row), (min_col, max_col)) in objects:
            if max_col < center_col:
               count = obj_size
               break # first object to the left of center only

    # Initialize the 1x1 output grid.
    output_grid = np.array([[count]])

    return output_grid