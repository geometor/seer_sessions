"""
Identify the yellow region within the input grid. Count the number of yellow pixels. Create a new rectangular grid filled with yellow pixels, with dimensions as close to a square as possible, and having an area equal to number of yellow pixels
"""

import numpy as np

def find_objects(grid):
    # Find contiguous regions of the same color
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, object_pixels):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        object_pixels.append((row, col))
        dfs(row + 1, col, color, object_pixels)
        dfs(row - 1, col, color, object_pixels)
        dfs(row, col + 1, color, object_pixels)
        dfs(row, col - 1, color, object_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                color = grid[row, col]
                object_pixels = []
                dfs(row, col, color, object_pixels)
                if object_pixels and color != 0:  # Ignore background
                    objects.append({"color": color, "pixels": object_pixels})
    return objects

def get_rectangle_dimensions(count):
    if count == 0:
        return 0, 0

    # Find dimensions closest to a square
    for width in range(int(count**0.5), 0, -1):
          if count % width == 0:
              height = count // width
              return height, width

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find objects
    objects = find_objects(input_grid)

    # Find the yellow object
    yellow_object = None
    for obj in objects:
        if obj["color"] == 4:
            yellow_object = obj
            break

    if yellow_object is None:
        return []

    # Count yellow pixels
    yellow_pixel_count = len(yellow_object["pixels"])

    # Determine output dimensions
    height, width = get_rectangle_dimensions(yellow_pixel_count)


    # Create output grid
    output_grid = np.full((height, width), 4, dtype=int)

    return output_grid.tolist()