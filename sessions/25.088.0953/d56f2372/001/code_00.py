import numpy as np
from collections import deque

"""
Identify all distinct non-background objects in the input grid. Analyze each object to find its color, pixel count, top-most row (start_row), bottom-most row (end_row), and left-most column (start_col). Determine the overall minimum start_row and maximum end_row across all objects. Select a target object based on the following prioritized rules:
1. If exactly one object starts at the minimum start_row AND exactly one object ends at the maximum end_row, compare their pixel counts. Select the larger object. If sizes are equal, select the object starting at the minimum start_row.
2. If only one object starts at the minimum start_row, select that object.
3. If only one object ends at the maximum end_row, select that object.
4. If multiple objects start at the minimum start_row (and rules 1-3 don't apply), select the one among them with the smallest start_col (left-most).
Finally, extract the selected target object into a new grid sized to its minimal bounding box, preserving its shape and color against a background of 0.
"""

def find_objects(grid):
    """
    Finds all distinct contiguous objects of non-zero color in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains its 'color', 'pixels' (list of (r, c) tuples),
              'pixel_count', 'start_row', 'end_row', and 'start_col'.
              Returns an empty list if no objects are found.
    """
    objects = []
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    
    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c
                
                while q:
                    row, col = q.popleft()
                    pixels.append((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)
                    
                    # Check neighbors (4-directional adjacency)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if pixels:
                    objects.append({
                        'color': color,
                        'pixels': pixels,
                        'pixel_count': len(pixels),
                        'start_row': min_r,
                        'end_row': max_r,
                        'start_col': min_c,
                        # Also store bounding box for convenience later
                        'bounding_box': (min_r, min_c, max_r, max_c) 
                    })
                    
    return objects

def transform(input_grid):
    """
    Transforms the input grid by identifying objects, selecting one based on positional
    uniqueness and size, and extracting it to a new grid.

    Args:
        input_grid (np.array): The 2D input grid.

    Returns:
        np.array: The 2D output grid containing the selected object.
    """
    # 1. Identify Objects
    objects = find_objects(np.array(input_grid))

    # Handle case with no objects
    if not objects:
        return np.array([[]], dtype=int) # Or potentially return an empty 1x1 grid: np.zeros((1,1), dtype=int)

    # Handle case with only one object
    if len(objects) == 1:
        target_object = objects[0]
    else:
        # 2. Analyze Objects & 3. Find Extremes
        min_start_row = min(obj['start_row'] for obj in objects)
        max_end_row = max(obj['end_row'] for obj in objects)

        # 4. Identify Top/Bottom Objects
        top_objects = [obj for obj in objects if obj['start_row'] == min_start_row]
        bottom_objects = [obj for obj in objects if obj['end_row'] == max_end_row]

        # 5. Select the Target Object
        target_object = None
        
        # Rule A (Unique Top & Bottom)
        if len(top_objects) == 1 and len(bottom_objects) == 1:
            top_obj = top_objects[0]
            bottom_obj = bottom_objects[0]
            if top_obj['pixel_count'] >= bottom_obj['pixel_count']:
                target_object = top_obj
            else:
                target_object = bottom_obj
        # Rule B (Unique Top Only)
        elif len(top_objects) == 1:
            target_object = top_objects[0]
        # Rule C (Unique Bottom Only)
        elif len(bottom_objects) == 1:
             target_object = bottom_objects[0]
        # Rule D (Top Tie-breaker)
        else: # Implies len(top_objects) > 1 (and potentially len(bottom_objects) is also > 1 or 0)
            target_object = min(top_objects, key=lambda obj: obj['start_col'])

    # 6. Extract and Output
    if target_object is None: 
         # Should ideally not happen if logic covers all cases, but as a fallback
         # maybe return the first object or an empty grid? Let's pick first obj.
         if objects: target_object = objects[0] 
         else: return np.array([[]], dtype=int) # Should have been caught earlier


    min_r, min_c, max_r, max_c = target_object['bounding_box']
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # Create a new grid with the dimensions of the target object's bounding box
    output_grid = np.zeros((height, width), dtype=int)

    # Copy the pixels of the target object into the new grid
    for r, c in target_object['pixels']:
        output_grid[r - min_r, c - min_c] = target_object['color']

    return output_grid.tolist() # Convert back to list of lists if required by the framework