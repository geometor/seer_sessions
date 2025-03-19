"""
1. Remove Blue: Remove all blue pixels from the grid.
2. Yellow Expansion: If there's a yellow object that consists of a single horizontal line of pixels (one or more pixels in the same row), expand that line upwards by two rows, *and* downwards by one, so long as the expansion stays within the grid bounds.
3. Yellow Connection: If there are disconnected components of yellow, extend each disconnected component by one row, and connect them along the shortest path.
"""

import numpy as np

def get_objects(grid):
    """
    Identify contiguous regions of the same color as distinct objects.
    Returns a dictionary of objects keyed by color.
    """
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
            visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                color = grid[row, col]
                obj_pixels = []
                dfs(row, col, color, obj_pixels)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj_pixels)
    return objects

def transform(input_grid):
    # initialize output_grid as a copy of the input_grid
    output_grid = input_grid.copy()
    objects = get_objects(input_grid)

    # 1. Remove all blue pixels
    if 1 in objects:
        for blue_object in objects[1]:
            for pixel in blue_object:
                output_grid[pixel] = 0

    # 2. Yellow Expansion and 3. Yellow Connection
    if 4 in objects:
        new_yellow_pixels = []
        for yellow_object in objects[4]:
            rows = [pixel[0] for pixel in yellow_object]
            cols = [pixel[1] for pixel in yellow_object]
            min_row, max_row = min(rows), max(rows)
            min_col, max_col = min(cols), max(cols)

            if min_row == max_row:  # Single horizontal line
                # Expand upwards by two rows
                for r in range(max(0, min_row - 2), min_row):
                    for c in range(min_col, max_col + 1):
                        new_yellow_pixels.append((r, c))
                #expand downwards by one row
                for c in range(min_col, max_col+1):
                    new_yellow_pixels.append((min_row + 1, c)) if min_row + 1 < input_grid.shape[0] else None

            else: # disconnected objects
                # expand by one row
                for r in range(max(0, min_row-1), min_row):
                  for c in range(min_col, max_col+1):
                    new_yellow_pixels.append((r,c))
                for r in range(max_row+1, min(input_grid.shape[0], max_row+2)):
                  for c in range(min_col, max_col + 1):
                    new_yellow_pixels.append((r,c))


        # connect components
        if len(objects[4]) > 1:

            # add all current yellow objects to new_yellow_pixels
            for obj in objects[4]:
              for pixel in obj:
                new_yellow_pixels.append(pixel)

            # find shortest path - start with first two objects
            obj1 = objects[4][0]
            obj2 = objects[4][1]

            # get center of mass of each object
            obj1_center = (sum([p[0] for p in obj1]) // len(obj1), sum([p[1] for p in obj1])//len(obj1))
            obj2_center = (sum([p[0] for p in obj2]) // len(obj2), sum([p[1] for p in obj2])//len(obj2))


            row_diff = obj2_center[0] - obj1_center[0]
            col_diff = obj2_center[1] - obj1_center[1]

            current_row = obj1_center[0]
            current_col = obj1_center[1]

            # connect row
            if row_diff != 0:
              row_step = 1 if row_diff > 0 else -1
              for _ in range(abs(row_diff)):
                current_row += row_step
                new_yellow_pixels.append((current_row, current_col))

            # connect col
            if col_diff != 0:
              col_step = 1 if col_diff > 0 else -1
              for _ in range(abs(col_diff)):
                current_col += col_step
                new_yellow_pixels.append((current_row, current_col))
        
        # update the grid
        for r, c in new_yellow_pixels:
          if 0 <= r < output_grid.shape[0] and 0<= c < output_grid.shape[1]:
            output_grid[r, c] = 4

    return output_grid