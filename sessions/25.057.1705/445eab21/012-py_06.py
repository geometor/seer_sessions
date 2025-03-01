"""
1.  **Identify Objects:** Find all contiguous regions (objects) of the same color in the input grid.  Consider adjacent pixels (up, down, left, right).
2.  **Find 2x2 Squares:** Check if any of the identified objects are 2x2 squares.
3.  **Prioritize and Select:**
    *   If multiple 2x2 squares exist, select the top-left-most square.
    *   If one 2x2 square, select.
    *   If no 2x2 squares exist, select a single yellow pixel if available. If not, select a single orange pixel.
4.  **Create Output:**
    *   If a 2x2 square was selected, create a 2x2 output grid of the same color and position as the selected square.
    *   If a single pixel was selected, create a 1x1 output grid with the selected color.
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
            if (row, col) not in visited:
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

def find_top_left_square(objects):
    """Finds the top-left-most 2x2 square among all objects."""
    top_left_square = None
    min_row, min_col = float('inf'), float('inf')

    for color, object_list in objects.items():
        for obj_coords in object_list:
            if is_square(obj_coords):
                rows, cols = zip(*obj_coords)
                curr_min_row, curr_min_col = min(rows), min(cols)
                if curr_min_row < min_row or (curr_min_row == min_row and curr_min_col < min_col):
                    min_row, min_col = curr_min_row, curr_min_col
                    top_left_square = (color, obj_coords)
    return top_left_square

def transform(input_grid):
    """
    Transforms the input grid according to the rules.
    """
    objects = find_objects(input_grid)
    top_left_square = find_top_left_square(objects)

    if top_left_square:
        # Create a 2x2 output grid
        color, _ = top_left_square
        output_grid = np.full((2, 2), color, dtype=int)
        return output_grid
    else:
        # Find single yellow or orange pixels
        if 4 in objects:  # Yellow
           output_grid = np.array([[4]])
           return output_grid
        
        if 7 in objects: # Orange
            output_grid = np.array([[7]])
            return output_grid
        
        # default
        return np.zeros((1,1), dtype=int)