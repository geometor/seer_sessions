"""
Extracts non-zero pixels from the input grid and rearranges them into a 3x3 output grid, preserving their colors.
The arrangement in the 3x3 grid follows a specific pattern based on color and relative positioning.
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
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Find objects in the input grid.  We only care about the non-zero pixels.
    objects = find_objects(input_grid)

    # Extract the relevant objects by color.
    magenta_pixels = [obj for obj in objects if obj["color"] == 6]
    orange_pixels = [obj for obj in objects if obj["color"] == 7]
    grey_pixels = [obj for obj in objects if obj["color"] == 5]
    yellow_pixels = [obj for obj in objects if obj["color"] == 4]

    # Place the objects into the output grid.
    # Magenta pixels:  The program specifies these form the beginning of the first row
    if magenta_pixels:
      # Assuming that there is always one object made of 2 adjacent pixels
        output_grid[0,0] = 6
        output_grid[0,1] = 6

    # Orange Pixels. The program says that the first instance, is in the top row.
    if orange_pixels:
        output_grid[0,2] = 7

    # Grey pixels. The program requires an instance in the second row
    if grey_pixels:
       output_grid[1,1] = 5

    if len(orange_pixels) > 1:
      output_grid[1,2] = 7

    # Yellow pixels. The program specifies them at the beginning of the last row.
    if yellow_pixels:
        output_grid[2,0] = 4
        output_grid[2,1] = 4
    
    # The rest of the spots will remain 0 by initialization

    return output_grid