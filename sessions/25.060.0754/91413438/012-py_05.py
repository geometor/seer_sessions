"""
The transformation replicates each object in the input grid four times, placing the copies above, below, to the left, and to the right of the original object. The distance between the original object and each copy appears to be equal to the object's size (bounding box height/width). Overlapping replications favor the object appearing later in the input object list.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies distinct objects within a grid.  An object is a contiguous region of the same color.
    Returns a list of objects, where each object is a dictionary with:
      - color: The color (value) of the object.
      - coordinates: A list of (row, col) tuples representing the object's pixels.
      - position: top-left coordinate (bounding box)
      - size: bounding box height and width
      - shape: bounding box dimensions as a tuple
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, coordinates):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        coordinates.append((row, col))
        dfs(row + 1, col, color, coordinates)
        dfs(row - 1, col, color, coordinates)
        dfs(row, col + 1, color, coordinates)
        dfs(row, col - 1, color, coordinates)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                color = grid[row, col]
                if color != 0:  # Ignore background
                    coordinates = []
                    dfs(row, col, color, coordinates)
                    # find bounding box
                    min_row = min(c[0] for c in coordinates)
                    max_row = max(c[0] for c in coordinates)
                    min_col = min(c[1] for c in coordinates)
                    max_col = max(c[1] for c in coordinates)
                    
                    object_info = {
                        "color": color,
                        "coordinates": coordinates,
                        "position": (min_row, min_col),
                        "size": (max_row - min_row + 1, max_col - min_col + 1),
                        "shape": (max_row - min_row + 1, max_col - min_col + 1)
                    }

                    objects.append(object_info)
    return objects

def transform(input_grid):
    # Identify objects in the input grid.
    input_objects = get_objects(input_grid)

    # Initialize output grid with background color (0).
    # size of output grid needs to consider the input grid plus replication factor
    # find maximum extent an object replication will extend to
    max_row_extent = 0
    max_col_extent = 0

    for obj in input_objects:
      max_row_extent = max(max_row_extent, obj['position'][0] + obj['size'][0] * 2) # original + down
      max_col_extent = max(max_col_extent, obj['position'][1] + obj['size'][1] * 2) # original + right
    
    output_grid = np.zeros((max_row_extent+1, max_col_extent+1), dtype=int)

    # Iterate through each object and replicate it.
    for obj in input_objects:
        color = obj["color"]
        coords = obj["coordinates"]
        size_y, size_x = obj["size"]


        # Original object
        for row, col in coords:
          output_grid[row,col] = color

        # Replicate above.
        for row, col in coords:
            new_row = row - size_y
            if new_row >= 0:
                output_grid[new_row, col] = color

        # Replicate below.
        for row, col in coords:
            new_row = row + size_y
            if new_row < output_grid.shape[0]:
                output_grid[new_row, col] = color

        # Replicate to the left.
        for row, col in coords:
            new_col = col - size_x
            if new_col >= 0:
                output_grid[row, new_col] = color

        # Replicate to the right.
        for row, col in coords:
            new_col = col + size_x
            if new_col < output_grid.shape[1]:
                output_grid[row, new_col] = color
    return output_grid