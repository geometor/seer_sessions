"""
Transforms an input grid based on rules involving colors 7, 9, 0, and 2. Color 7 acts as a boundary and remains unchanged. Color 9 changes to 1 at a specific location or remains unchanged. Color 0 changes to 9 based on adjacency to horizontal lines of 7 and to color 9 pixels. Color 2 changes to 9 based on being below horizontal lines of 7.
"""

import numpy as np

def find_horizontal_lines(grid, color):
    """Finds complete horizontal lines of a specified color."""
    rows, cols = grid.shape
    lines = []
    for row in range(rows):
        if np.all(grid[row, :] == color):
            lines.append(row)
    return lines

def find_color_objects(grid, color):
     rows, cols = grid.shape
     objects = []
     visited = np.zeros((rows, cols), dtype=bool)

     def dfs(row, col, current_object):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return

        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

     for row in range(rows):
        for col in range(cols):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
     return objects

def transform(input_grid):
    # Initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Boundary Preservation (Color 7 remains unchanged)
    # (Implicitly handled by copying the input grid)

    # Find complete horizontal lines of 7
    horizontal_lines_7 = find_horizontal_lines(input_grid, 7)
    objects_9 = find_color_objects(input_grid, 9)

    # 2. Object 9 Transformation (9 to 1)
    for obj in objects_9:
      if all(input_grid[p[0],:]==9 for p in obj ): # horizontal line of 9s
        right_most = max(p[1] for p in obj)
        for r,c in obj:
            if c == right_most:
              output_grid[r,c] = 1


    # 3. Object 0 Transformation (0 to 9)
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 0:
                # Check for adjacency to complete horizontal lines of 7
                adjacent_to_7_line = False
                for line_row in horizontal_lines_7:
                  horizontal_segment = []
                  for c in range(cols):
                      if input_grid[line_row,c] == 7:
                          horizontal_segment.append(c)
                      elif len(horizontal_segment)>1:
                          if row == line_row + 1 or row == line_row-1:
                             if col in horizontal_segment:
                               adjacent_to_7_line = True
                               break;
                      else:
                          horizontal_segment = []
                  if adjacent_to_7_line:
                      break

                #check for vertical adjacency with color 9
                adjacent_to_9 = False
                if row > 0 and input_grid[row - 1, col] == 9:
                    adjacent_to_9 = True
                if row < rows - 1 and input_grid[row + 1, col] == 9:
                    adjacent_to_9 = True

                if adjacent_to_7_line or adjacent_to_9:
                    output_grid[row, col] = 9

    # 4. Object 2 Transformation (2 to 9)
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 2:
              for line_row in horizontal_lines_7:
                  horizontal_segment = []
                  for c in range(cols):
                      if input_grid[line_row,c] == 7:
                          horizontal_segment.append(c)
                      elif len(horizontal_segment)>1:
                          if row == line_row + 1:
                             if col in horizontal_segment:
                               output_grid[row,col] = 9
                               break;
                      else:
                          horizontal_segment = []


    return output_grid