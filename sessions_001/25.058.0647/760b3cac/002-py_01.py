"""
1.  **Identify Shapes:** Locate contiguous regions of pixels of the same color. Consider each of these regions as a separate "shape."

2.  **Process Azure Shapes:** For each shape composed of azure (8) pixels:
    *   Shift all pixels of the shape to be as close as possible to the left boundary of the input grid.
    *   Preserve the relative positions (vertical stacking) of the pixels of the shape.

3.  **Preserve other Shapes:** Shapes that are not azure (8) remain unchanged in their original positions.

4.  **Output:** Construct the output grid with the modified azure shapes and the preserved other shapes.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous regions (objects) of the same color in a grid.

    Args:
        grid: A 2D numpy array representing the grid.

    Returns:
        A list of objects, where each object is a list of (row, col) coordinates.
    """
    objects = []
    visited = set()

    def dfs(row, col, color, current_object):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, color, current_object)
        dfs(row - 1, col, color, current_object)
        dfs(row, col + 1, color, current_object)
        dfs(row, col - 1, color, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited:
                current_object = []
                dfs(row, col, grid[row, col], current_object)
                if current_object:
                    objects.append(current_object)
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find objects
    objects = find_objects(input_grid)

    # process each object
    for obj in objects:
        # get the color of the object
        color = input_grid[obj[0][0], obj[0][1]]

        # process azure shapes
        if color == 8:
            # sort by column then by row
            obj.sort(key=lambda x: (x[1], x[0]))

            # find how much can be shifted by calculating min col in object pixels
            min_col = min(x[1] for x in obj)
            
            # clear old positions of shape
            for row, col in obj:
                output_grid[row, col] = 0

            # set azure shape into new position
            new_col = 0
            col_dict = {}
            for row, col in obj:
                if col not in col_dict:
                    col_dict[col] = new_col
                    new_col +=1
                output_grid[row, col_dict[col]] = 8
    
    return output_grid