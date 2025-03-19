"""
1.  **Find Green Objects:** Identify all distinct green (3) objects within the input grid.
2.  **Find Red Objects:** Identify all distinct red (2) objects within the input grid.
3.  **Find Rightmost Edge:** Determine the rightmost column index containing any non-white (non-zero) pixel in the input grid.
4.  **Outer Green Object:** Select the green object, if any, which encloses a red object. If multiple green objects satisfy this condition, or no green object exists, then no action. If no green objects enclose a red object, stop.
5. **Contained Red Object:** Select one red object that is contained within the selected green object.
6.  **Extend Green:** Extend the selected green object horizontally to the right, *only on the rows where green pixels exist*, up to and including the calculated rightmost edge.
7.  **Extend Red:** Extend the selected red object horizontally to the right, *only on the rows where red pixels exist*, up to and including the calculated rightmost edge, but only within the bounds of the extended green object.
8. **Preserve other pixels:** Ensure that all pixels that are not part of the selected green or red objects are copied unchanged from the input to the output.
"""

import numpy as np

def find_objects(grid, color):
    """Find contiguous regions of a specific color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, current_object):
        """Depth-first search to explore contiguous regions."""
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def get_bounding_box(obj):
    """Get the bounding box of a list of coordinates."""
    min_row = min(p[0] for p in obj)
    max_row = max(p[0] for p in obj)
    min_col = min(p[1] for p in obj)
    max_col = max(p[1] for p in obj)
    return min_row, max_row, min_col, max_col

def is_contained(inner_obj, outer_obj):
    """Check if inner_obj is fully contained within outer_obj."""
    inner_min_row, inner_max_row, inner_min_col, inner_max_col = get_bounding_box(inner_obj)
    outer_min_row, outer_max_row, outer_min_col, outer_max_col = get_bounding_box(outer_obj)
    return (inner_min_row >= outer_min_row and inner_max_row <= outer_max_row and
            inner_min_col >= outer_min_col and inner_max_col <= outer_max_col)

def find_outermost_object(objects):
    """Find the object that contains all others. Returns None if no object contains all others"""
    if not objects:
        return None
    if len(objects) == 1:
        return objects[0]
    
    outermost = None
    for obj1 in objects:
        contains_all = True
        for obj2 in objects:
            if obj1 is obj2:
                continue
            if not is_contained(obj2, obj1):
                contains_all = False
                break
        if contains_all:
            outermost = obj1
            break;
            
    #If no object contains all others, check to make sure at least one object contains the others.
    if outermost is None:
        for obj1 in objects:
            contains_others = True
            for obj2 in objects:
                if obj1 is obj2:
                    continue
                if not is_contained(obj2, obj1):
                    contains_others = False
                    break
            if contains_others:
                outermost = obj1
                break
    
    return outermost

def rightmost_colored_edge(grid):
    """Determine rightmost edge of any non-white pixel."""
    max_col = -1
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                max_col = max(max_col, c)
    return max_col

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find green and red objects.
    green_objects = find_objects(input_grid, 3)
    red_objects = find_objects(input_grid, 2)
    
    # Find rightmost colored edge (any non-zero pixel).
    right_edge = rightmost_colored_edge(input_grid)

    # Find the outermost green object.
    outermost_green = None
    for green_object in green_objects:
        contains_red = False
        for red_object in red_objects:
            if is_contained(red_object, green_object):
                contains_red = True
                break
        if contains_red:
            outermost_green = green_object
            break

    # Extend green and red, if found.
    if outermost_green is not None:
        #Find a contained red object
        contained_red = None
        for red_object in red_objects:
          if is_contained(red_object, outermost_green):
            contained_red = red_object
            break

        if contained_red is not None:
          # Extend green object on rows where it exists.
          for r, c in outermost_green:
              for c_new in range(c, right_edge + 1):
                  output_grid[r, c_new] = 3

          # Extend red object on rows where it exists, within green bounds.
          for r,c in contained_red:
            for c_new in range(c, right_edge+1):
              if output_grid[r,c_new] == 3:
                output_grid[r, c_new] = 2
    
    return output_grid