"""
1.  **Input:** Receive an input grid.
2.  **Object Identification:** Identify all contiguous regions (objects) of the same color.
3.  **Output Grid Initialization:** Create an empty 3x4 output grid.
4.  **Top Row Construction:**
    *   Identify the unique colors present in the input grid.
    *   Create the first row of the output by taking the first object pixel encountered in each column, select the first pixel from each unique color.
5.  **Second Row Construction:**
    *   Find the object pixels in row 1.  Select the second row from the bounding box of each of those objects.
6.  **Third Row Construction**:
    *   Find the object pixels in row 2.  Select the next row of pixels from the bounding box, if available.
7.  **Return:** The populated 3x4 output grid.
"""

import numpy as np

def get_objects(grid):
    """Identifies contiguous regions (objects) of the same color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(row, col, color, object_pixels):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        object_pixels.append((row, col))
        dfs(row + 1, col, color, object_pixels)
        dfs(row - 1, col, color, object_pixels)
        dfs(row, col + 1, color, object_pixels)
        dfs(row, col - 1, color, object_pixels)

    for row in range(rows):
        for col in range(cols):
            if not visited[row, col] and grid[row, col] != 0:
                color = grid[row, col]
                object_pixels = []
                dfs(row, col, color, object_pixels)
                if object_pixels:
                    min_row, min_col = np.min(object_pixels, axis=0)
                    max_row, max_col = np.max(object_pixels, axis=0)
                    objects.append({
                        'color': color,
                        'bounding_box': (min_row, min_col, max_row + 1, max_col + 1),
                        'pixels': object_pixels
                    })
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 4), dtype=int)
    input_grid = np.array(input_grid)

    # Object Identification
    objects = get_objects(input_grid)

    # Top Row Construction
    unique_colors = []
    for col in range(input_grid.shape[1]):
      for row in range(input_grid.shape[0]):
        color = input_grid[row,col]
        if color != 0 and color not in unique_colors:
          unique_colors.append(color)
          break

    output_col = 0
    for color in unique_colors:
        if output_col < 4:
            output_grid[0, output_col] = color
            output_col += 1

    # Second Row Construction
    for col in range(output_grid.shape[1]):
        color = output_grid[0, col]
        if color != 0:
          for obj in objects:
            if obj['color'] == color:
              min_row, min_col, max_row, max_col = obj['bounding_box']
              if min_row + 1 < max_row:
                output_grid[1,col] = color

    # Third Row Construction
    for col in range(output_grid.shape[1]):
        color = output_grid[1,col]
        if color == 0:
          color = output_grid[0,col]
        if color != 0:
          for obj in objects:
            if obj['color'] == color:
              min_row, min_col, max_row, max_col = obj['bounding_box']
              if min_row + 1 < max_row and output_grid[1,col] != 0:
                output_grid[2, col] = color
              elif min_row < max_row:
                output_grid[2,col] = color
    return output_grid