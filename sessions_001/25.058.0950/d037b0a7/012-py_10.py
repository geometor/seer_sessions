"""
1.  **Identify Objects:** Find all contiguous regions of the same color. These are the objects.
2.  **Find Leftmost/Rightmost Objects:** Among the identified objects find the object with the right most and left most extent.
3.  **Propagate Downward:** The color of each object propagates downward, starting from the object's top row and continuing to the bottom row of the grid. If an object is below another, it is overwritten.
4. All other cells that have not been overwritten are unchanged.
"""

import numpy as np

def find_objects(grid):
    """
    Finds all contiguous regions of the same color.
    Returns a list of objects, where each object is a dictionary
    containing the color and a list of (row, col) coordinates.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(row, col, color, object_coords):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        object_coords.append((row, col))
        dfs(row + 1, col, color, object_coords)
        dfs(row - 1, col, color, object_coords)
        dfs(row, col + 1, color, object_coords)
        dfs(row, col - 1, color, object_coords)

    for row in range(rows):
        for col in range(cols):
            if not visited[row, col]:
                color = grid[row, col]
                object_coords = []
                dfs(row, col, color, object_coords)
                if object_coords:
                    objects.append({"color": color, "coords": object_coords})
    return objects

def find_leftmost_rightmost_objects(objects):
    """
    Finds the leftmost and rightmost objects among a list of objects.
    """
    if not objects:
        return None, None

    leftmost_object = min(objects, key=lambda obj: min(c[1] for c in obj["coords"]))
    rightmost_object = max(objects, key=lambda obj: max(c[1] for c in obj["coords"]))

    return leftmost_object, rightmost_object


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, _ = output_grid.shape

    # Find objects
    objects = find_objects(input_grid)
    
    # Propagate each object's color downwards
    for obj in objects:
        color = obj["color"]
        min_row = min(coord[0] for coord in obj["coords"])
        for row in range(min_row, rows):
            for col in [coord[1] for coord in obj["coords"] if coord[0] >= min_row]:
                output_grid[row, col] = color

    return output_grid