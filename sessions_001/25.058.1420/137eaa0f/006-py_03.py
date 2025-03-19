"""
Extracts non-zero pixels from the input grid and rearranges them into a 3x3 output grid, preserving their colors.
The arrangement in the 3x3 grid follows specific rules based on color:
- Magenta: Top row, left-aligned.
- Orange: Top row, rightmost. If two, also in the second row, rightmost.
- Grey: Second row, center.
- Yellow: Bottom row, left-aligned.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects of non-zero pixels in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, object_pixels):
        """Depth-first search to find all pixels of an object."""
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
            if grid[row, col] != 0 and not visited[row, col]:
                color = grid[row, col]
                object_pixels = []
                dfs(row, col, color, object_pixels)
                objects.append({"color": color, "pixels": object_pixels})
    return objects

def transform(input_grid):
    # Initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Find objects in the input grid.
    objects = find_objects(input_grid)

    # Place Magenta
    magenta_objects = [obj for obj in objects if obj["color"] == 6]
    if magenta_objects:
        row, col = 0, 0
        for _ in magenta_objects[0]['pixels']:
            if col < 3: # Limit to the grid width
               output_grid[row, col] = 6
               col +=1

    # Place Orange
    orange_objects = [obj for obj in objects if obj["color"] == 7]
    if len(orange_objects) >= 1:
        output_grid[0, 2] = 7
    if len(orange_objects) >= 2:
        output_grid[1, 2] = 7

    # Place Grey
    grey_objects = [obj for obj in objects if obj["color"] == 5]
    if grey_objects:
        output_grid[1, 1] = 5

    # Place Yellow
    yellow_objects = [obj for obj in objects if obj["color"] == 4]
    if yellow_objects:
        row, col = 2, 0
        for _ in yellow_objects[0]['pixels']:
            if col < 3:
               output_grid[row, col] = 4
               col+=1
    
    return output_grid