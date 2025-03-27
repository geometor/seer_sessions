"""
Transforms the input grid by identifying connected regions (objects) of the same color and applying color transformations based on object adjacency, containment, and mirroring rules.
"""

import numpy as np
from collections import deque

def find_objects(grid):
    """
    Identifies connected regions (objects) of the same color in the grid.
    Returns a list of objects, where each object is a set of (row, col) coordinates.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []

    def bfs(start_row, start_col):
        """Performs Breadth-First Search to find connected pixels of the same color."""
        queue = deque([(start_row, start_col)])
        visited.add((start_row, start_col))
        object_color = grid[start_row, start_col]
        current_object = set()

        while queue:
            r, c = queue.popleft()
            current_object.add((r, c))

            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and grid[nr, nc] == object_color:
                    queue.append((nr, nc))
                    visited.add((nr, nc))
        return current_object

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                new_object = bfs(r, c)
                objects.append(new_object)
    return objects

def get_object_color(grid, obj):
   "return color"
   r,c = next(iter(obj))
   return grid[r,c]


def is_inside(inner_obj, outer_obj):
    """
    Checks if one object is completely inside another object. It simply sees if the 
    object sets intersect
    """
    if not outer_obj or not inner_obj:
        return False
    
    return inner_obj.issubset(outer_obj)

def transform(input_grid):
    """
    Transforms the input grid based on object relationships and color mapping.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    objects = find_objects(input_grid)

    color_map = {
        1: 3,
        2: 9,
        4: 6,
        9: 4,
        7: 2,
        6: 0,
        3: 1,
    }

    for obj in objects:
        obj_color = get_object_color(input_grid, obj)
        
        #basic color changes
        if obj_color in color_map:
            for r, c in obj:
                output_grid[r,c] = color_map[obj_color]
                continue

        #check for enclosure
        for other_obj in objects:
           if obj != other_obj:
                other_color = get_object_color(input_grid, other_obj)

                if is_inside(obj, other_obj):
                    
                    if obj_color in color_map:
                        for r,c in obj:
                            output_grid[r,c] = color_map[obj_color]
                            continue
                        


    return output_grid.tolist()