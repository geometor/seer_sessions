"""
1. Identify Target Colors: Examine the input grid and identify the pixels with colors that form a contiguous shape, excluding those which only neighbour color 0 or edge/corner.
2. Arrange in Order: The colors may not be in order. Therefore, once the colors are found, put them in numerical order.
3. Construct Output Grid: Create a 5x3 grid.
4. Populate Columns: Fill the first column with the color 4, repeated five times. Fill the second column with the color 6, repeated five times. Fill the third column with the color 8, repeated five times.
"""

import numpy as np

def get_objects(grid):
    """
    Find contiguous objects in the grid.
    Returns a dictionary of objects keyed by color.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, obj):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color:
            return
        visited.add((row, col))
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0:
                color = grid[r, c]
                obj = []
                dfs(r, c, color, obj)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj)

    return objects

def is_on_edge(grid, cell):
    """
    Check if given cell are on the edge of the grid
    """
    rows, cols = grid.shape
    r, c = cell
    return r == 0 or r == rows - 1 or c == 0 or c == cols - 1


def neighbours_only_zero(grid, object_pixels):
    """
    Checks all pixels to see if it only has zero or edge neighbours.
    """

    rows, cols = grid.shape
    for r,c in object_pixels:
      for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1,1), (1,-1), (-1, 1), (-1, -1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
          if grid[nr,nc]!=0 and grid[nr,nc]!=grid[r,c]:
            return False
    return True


def transform(input_grid):
    # Find objects in the input grid.
    objects = get_objects(input_grid)

    # Identify target colors (those that form shapes, not isolated, and don't just have 0 neighbours).
    target_colors = []
    for color, object_list in objects.items():
        for obj_pixels in object_list:
           if not neighbours_only_zero(input_grid,obj_pixels) and not any(is_on_edge(input_grid, cell) for cell in obj_pixels):
                target_colors.append(color)
                break # Go to check next color

    # Remove duplicates and sort to maintain the order found on the first example
    target_colors = sorted(list(set(target_colors)))

    # Construct output grid (5x3).
    output_grid = np.zeros((5, len(target_colors)), dtype=int)

    # Populate columns with target colors.
    for i, color in enumerate(target_colors):
        output_grid[:, i] = color

    return output_grid