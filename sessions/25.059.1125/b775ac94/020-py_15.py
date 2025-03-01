"""
1.  **Identify Objects:** Find all distinct colored regions (objects) in the input grid. These are contiguous areas of non-zero pixels.

2.  **Expansion of single pixels:** Locate all single pixels of colors blue (1) or red (2) and expand to 3x3 squares of the same color.

3.  **Yellow Expansion:** Locate any horizontal yellow bar and extend the bar to the right edge of the grid, maintaining the original height.

4.  **Azure Mirroring:** Locate the 2x1 azure (color 8) object. Copy this object to the right edge of the grid, aligning the top edge.

5. **Magenta Expansion:** Locate any magenta pixel (color 6) and add one magenta pixel to the right.
"""

import numpy as np

def find_objects(grid):
    """Finds distinct colored regions (objects) in the grid."""
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_coords):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_coords.append((row, col))
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != 0 and not visited[row, col]:
                color = grid[row, col]
                obj_coords = []
                dfs(row, col, color, obj_coords)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj_coords)
    return objects

def is_single_pixel(obj):
    """Checks if an object is a single pixel."""
    return len(obj) == 1

def expand_to_3x3(grid, row, col, color):
    """Expands a single pixel to a 3x3 square."""
    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
                grid[r, c] = color

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid)

    # Expansion of single pixels (blue and red)
    for color in [1, 2]:  # Blue and Red
        if color in objects:
            for obj in objects[color]:
                if is_single_pixel(obj):
                    row, col = obj[0]
                    expand_to_3x3(output_grid, row, col, color)

    # Yellow Expansion
    if 4 in objects:
        for obj in objects[4]:
            # Check if it's a horizontal bar (more than one pixel in a row)
            rows = [r for r, _ in obj]
            if len(set(rows)) == 1 and len(obj) > 1 :  # Check for same row and length > 1
                min_row = min(r for r, c in obj)
                min_col = min(c for r, c in obj)
                for c in range(min_col, output_grid.shape[1]):
                    output_grid[min_row, c] = 4

    # Azure Mirroring
    if 8 in objects:
        for obj in objects[8]:
          #check if it is a 2x1 object
          if len(obj) == 2:
            min_row = min(r for r, c in obj)
            max_row = max(r for r, c in obj)
            min_col = min(c for r, c in obj)
            max_col = max(c for r, c in obj)

            width = max_col - min_col + 1
            height = max_row - min_row + 1

            if width == 1 and height == 2:
                for r in range(min_row, max_row + 1):
                  for c in range(output_grid.shape[1] - width, output_grid.shape[1]):
                      output_grid[r, c] = 8

    # Magenta Expansion
    if 6 in objects:
        for obj in objects[6]:
            for r, c in obj:
                if c + 1 < output_grid.shape[1]:
                    output_grid[r, c + 1] = 6

    return output_grid