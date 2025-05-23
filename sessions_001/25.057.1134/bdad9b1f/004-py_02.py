"""
1.  **Identify Objects:** Locate all distinct contiguous colored regions (objects) in the input grid.
2.  **Preserve Unchanged Objects:** Copy any objects from input that do not interact with other to the output grid, maintaining their original positions and colors.
3. **Horizontal Extension**: Extend *each* identified horizontal object to the right.
4. **Meeting Point:** The extending stops when it encounters an object.
5. **New Object Creation:** When extension stops, a yellow (4) is created on the extended object's last position
6.  **Fill Remaining:** Fill any remaining cells in the output grid with the default value of 0 (white).
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1]
                or visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                obj = []
                dfs(row, col, grid[row, col], obj)
                objects.append(obj)
    return objects


def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Copy and extend objects
    for obj in objects:
        first_pixel = obj[0]
        color = input_grid[first_pixel]

        # if is a horizontal object
        is_horizontal = all(pixel[0] == first_pixel[0] for pixel in obj)

        if is_horizontal:
          #copy the horizontal object
          for r,c in obj:
            output_grid[r,c] = input_grid[r,c]

          #start extending it.
          row = first_pixel[0]
          col = obj[-1][1] #last pixel to start extending
          while col+1 < output_grid.shape[1]:
            col = col + 1
            if input_grid[row,col] != 0 and input_grid[row,col]!=color:
              output_grid[row,col-1]=4 #meeting point color
              break;
            else:
              output_grid[row,col]=color

        else:
          #copy other object type
          for r,c in obj:
            output_grid[r,c] = input_grid[r,c]
          

    return output_grid