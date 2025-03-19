"""
1.  **Identify Objects:** Find all contiguous regions (objects) of the same color within the input grid. Consider only non-black colors.
2.  **Select Square:** If any of the identified objects are 2x2 squares, select it.
3. **Output:** Create a 2x2 output with matching color and location as the
   selected object.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies distinct objects in a grid based on color contiguity.
    Returns a dictionary of objects, where the key is the color 
    and the value is a list of (row, col) coordinates.
    """
    objects = {}
    visited = set()

    def dfs(row, col, color, obj_coords):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        obj_coords.append((row, col))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(row + dr, col + dc, color, obj_coords)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            color = grid[row, col]
            if color != 0 and (row, col) not in visited:  # Exclude background color 0
                obj_coords = []
                dfs(row, col, color, obj_coords)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj_coords)
    return objects

def is_square(obj_coords, size=2):
    """
    Checks if the given object coordinates form a 2x2 square.
    """
    if len(obj_coords) != size * size:
        return False

    rows, cols = zip(*obj_coords)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    if max_row - min_row + 1 != size or max_col - min_col + 1 != size:
        return False
    
    # Check if all expected cells exist
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
          if (r,c) not in obj_coords:
            return False

    return True


def transform(input_grid):
    """
    Transforms the input grid by finding and returning the first 2x2 square.
    """
    # Find all objects
    objects = find_objects(input_grid)

    # Find a 2x2 square object
    for color, object_list in objects.items():
        for obj_coords in object_list:
            if is_square(obj_coords):
                # Create a 2x2 output grid with the square's color
                output_grid = np.full((2, 2), color, dtype=int)
                return output_grid

    # If no 2x2 square is found, return a default 2x2 empty grid (all zeros)
    return np.zeros((2, 2), dtype=int)