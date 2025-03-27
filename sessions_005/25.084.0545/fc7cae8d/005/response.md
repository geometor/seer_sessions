```python
"""
The transformation identifies objects based on a combination of containment and color/shape patterns. It appears that the innermost objects, or specific parts of contained structures, are extracted and arranged based on their original relative positions. The output grid focuses on specific colors within contained shapes and arranges them.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous regions of the same color in a grid.
    Returns a list of objects, where each object is a list of (row, col) coordinates.
    """
    objects = []
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

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                color = grid[row, col]
                obj = []
                dfs(row, col, color, obj)
                if obj:
                    objects.append((color, obj))
    return objects

def get_bounding_box(obj):
    """
    Returns the bounding box of an object (list of coordinates).
    """
    min_row = min(coord[0] for coord in obj)
    max_row = max(coord[0] for coord in obj)
    min_col = min(coord[1] for coord in obj)
    max_col = max(coord[1] for coord in obj)
    return (min_row, min_col, max_row, max_col)

def is_contained(inner_obj, outer_obj):
    """
    Checks if inner_obj is completely contained within outer_obj.
    """
    inner_min_row, inner_min_col, inner_max_row, inner_max_col = get_bounding_box(inner_obj)
    outer_min_row, outer_min_col, outer_max_row, outer_max_col = get_bounding_box(outer_obj)

    return (outer_min_row <= inner_min_row and outer_min_col <= inner_min_col and
            outer_max_row >= inner_max_row and outer_max_col >= inner_max_col)

def get_innermost_objects(objects):
    """
    Identifies objects that are not contained by any other object.
    """

    innermost_objects = []
    for color1, obj1 in objects:
        contained = False
        for color2, obj2 in objects:
            if obj1 != obj2 and is_contained(obj1,obj2):
                contained = True
                break
        if not contained:
            innermost_objects.append((color1, obj1))

    return innermost_objects
    

def transform(input_grid):
    input_grid = np.array(input_grid)
    objects = find_objects(input_grid)

    # 1. Prioritize contained objects. If an object contains other objects,
    # focus on the *contained* objects.  If no objects are contained, return an empty array.
    contained_objects = []
    for color1, obj1 in objects:
        for color2, obj2 in objects:
            if obj1 != obj2 and is_contained(obj1, obj2):
               contained_objects.append((color1,obj1))

    if not contained_objects:
        return np.array([]).tolist()

    # 2. Within contained objects, look at specific colors.  In example 1,
    # colors 1,2,3, and 8 are selected, while others are ignored. Example 3 contains
    # 3,6,8,9 and selects 8,9,3,6. Example 2 contains 2,4,8 and picks them.
    # It appears that the code selects *all* objects contained by another.
    
    #get bounding box.
    combined_coords = []
    for _, obj_coords in contained_objects:
        combined_coords.extend(obj_coords)

    if not combined_coords:
       return np.array([]).tolist()

    min_row, min_col, max_row, max_col = get_bounding_box(combined_coords)
    output_grid = np.zeros((max_row - min_row + 1, max_col - min_col + 1), dtype=int)

    # Draw target objects onto output grid
    for color, obj_coords in contained_objects:
      for row, col in obj_coords:
          output_grid[row - min_row, col - min_col] = color

    return output_grid.tolist()
```