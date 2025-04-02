import numpy as np
from collections import deque

"""
1. Identify all distinct, connected groups of non-white pixels (objects) in the input grid.
2. Calculate the area (pixel count) for each object.
3. Determine the maximum area among all objects.
4. Count how many objects share this maximum area.
5. Apply the following rule:
   - If exactly one object has the maximum area, keep only that object.
   - If two or more objects share the maximum area, keep all objects *except* those that touch the top or bottom border of the grid.
6. Construct the output grid with the same dimensions as the input, containing only the kept objects on a white background.
"""

def find_objects(grid):
    """
    Identifies all connected objects of non-background colors in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color', 'pixels' (set of (r, c) tuples), 'area',
              'touches_top', and 'touches_bottom'.
    """
    height, width = grid.shape
    visited = set()
    objects = []
    
    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                obj_pixels = set()
                q = deque([(r, c)])
                visited.add((r, c))
                touches_top = False
                touches_bottom = False

                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    if row == 0:
                        touches_top = True
                    if row == height - 1:
                        touches_bottom = True

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           (nr, nc) not in visited and grid[nr, nc] == color:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'area': len(obj_pixels),
                    'touches_top': touches_top,
                    'touches_bottom': touches_bottom
                })
                
    return objects

def transform(input_grid):
    """
    Selectively removes objects based on area and border proximity.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed output grid.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape
    
    # Initialize output grid with background color (0)
    output_grid = np.zeros_like(grid_np)

    # Find all objects in the input grid
    objects = find_objects(grid_np)

    # Handle cases with no objects
    if not objects:
        return output_grid.tolist()

    # Calculate areas and find the maximum area
    max_area = 0
    for obj in objects:
        if obj['area'] > max_area:
            max_area = obj['area']

    # Find all objects that have the maximum area
    max_area_objects = [obj for obj in objects if obj['area'] == max_area]
    count_max_area_objects = len(max_area_objects)

    # Determine which objects to keep based on the rules
    objects_to_keep = []
    if count_max_area_objects == 1:
        # Keep only the single object with the maximum area
        objects_to_keep = max_area_objects
    elif count_max_area_objects > 1:
        # Keep all objects *except* those touching the top or bottom border
        for obj in objects:
            if not obj['touches_top'] and not obj['touches_bottom']:
                objects_to_keep.append(obj)
    # else: count_max_area_objects is 0 (shouldn't happen if objects exist), or < 1 which is impossible.
    # No explicit action needed if count_max_area_objects == 0 or < 1 (already handled by initial check)
    # If count_max_area_objects > 1 and *all* objects touch top/bottom, then objects_to_keep remains empty, resulting in an empty grid.

    # Draw the kept objects onto the output grid
    for obj in objects_to_keep:
        color = obj['color']
        for r, c in obj['pixels']:
            output_grid[r, c] = color
            
    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()