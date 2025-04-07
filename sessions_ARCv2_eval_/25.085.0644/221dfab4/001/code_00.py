import numpy as np
from collections import deque

"""
Transformation Rule:

1. Identify the unique "key" object which has color 4 (Yellow). Determine its horizontal column span, defined by its minimum and maximum column indices (`key_min_col`, `key_max_col`).
2. Determine the "target" color. This is the color of the objects that will be processed, other than the key object and the background color. Identify the target objects, which are connected components of the target color.
3. Determine the "background" color, which is the most frequent color in the grid excluding the key and target colors.
4. Initialize the output grid as a copy of the input grid.
5. For each distinct target object:
    a. Find all coordinates `(r, c)` belonging to this object.
    b. Determine the minimum and maximum row indices spanned by the object (`obj_min_row`, `obj_max_row`).
    c. Check if *any* pixel of the object falls within the key's column span (i.e., if there exists a pixel `(r, c)` in the object such that `key_min_col <= c <= key_max_col`).
    d. If there IS an overlap with the key column span:
        i. The "paint color" is Yellow (4).
        ii. For every row `r` from `obj_min_row` to `obj_max_row`, set the pixels in the output grid from column `key_min_col` to `key_max_col` to the paint color (Yellow).
        iii. Pixels of the original target object that fall *outside* the key column span retain their original target color in the output. Pixels *inside* the key column span are overwritten by the Yellow paint. (Step ii handles the overwrite implicitly if the output starts as a copy).
    e. If there is NO overlap with the key column span:
        i. The "paint color" is Green (3).
        ii. For every row `r` from `obj_min_row` to `obj_max_row`, set the pixels in the output grid from column `key_min_col` to `key_max_col` to the paint color (Green).
        iii. All pixels of the original target object are changed to the background color in the output grid.
6. The key object itself remains unchanged in the output grid.
"""

def find_objects(grid, color):
    """Finds all connected components of a given color using BFS."""
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                obj_coords.add((r, c))

                while q:
                    row, col = q.popleft()
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            obj_coords.add((nr, nc))
                
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def get_colors(grid):
    """Identifies key, target, and background colors."""
    unique_colors, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))

    key_color = 4
    
    # Remove key color if present
    if key_color in color_counts:
        del color_counts[key_color]
        
    if not color_counts: # Should not happen in this task based on examples
        return key_color, None, None 

    # Assume background is the most frequent remaining color
    background_color = max(color_counts, key=color_counts.get)
    del color_counts[background_color]

    # Assume target is the only remaining color (or one of them if multiple)
    target_color = list(color_counts.keys())[0] if color_counts else None # Takes the first if multiple targets exist

    return key_color, target_color, background_color


def transform(input_grid):
    """Applies the transformation rule to the input grid."""
    
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_grid = np.copy(input_np)

    # 1. Identify key object and its column span
    key_color, target_color, background_color = get_colors(input_np)
    
    if target_color is None: # No target objects to process
        return output_grid.tolist()
        
    key_coords = np.argwhere(input_np == key_color)
    if key_coords.size == 0:
         # No key object found, maybe return input or handle error
         # Based on the problem description, let's assume a key object always exists.
         # If not, this part needs specific error handling.
         # For now, return original grid if no key.
         return output_grid.tolist()

    key_min_col = np.min(key_coords[:, 1])
    key_max_col = np.max(key_coords[:, 1])

    # 2 & 6. Find target objects
    target_objects = find_objects(input_np, target_color)

    # 5. Process each target object
    for obj_coords in target_objects:
        if not obj_coords:
            continue

        rows = [r for r, c in obj_coords]
        cols = [c for r, c in obj_coords]
        
        obj_min_row = min(rows)
        obj_max_row = max(rows)

        # 5c. Check for overlap
        has_overlap = any(key_min_col <= c <= key_max_col for r, c in obj_coords)

        if has_overlap:
            # 5d. Overlap case: Paint Yellow
            paint_color = 4 # Yellow
            for r in range(obj_min_row, obj_max_row + 1):
                for c in range(key_min_col, key_max_col + 1):
                    output_grid[r, c] = paint_color
            # Original pixels outside key columns retain target color (already copied)
            # Original pixels inside key columns are overwritten above.
            
        else:
            # 5e. No overlap case: Paint Green, erase original object
            paint_color = 3 # Green
            for r in range(obj_min_row, obj_max_row + 1):
                for c in range(key_min_col, key_max_col + 1):
                    output_grid[r, c] = paint_color
            # Erase original object pixels
            for r_orig, c_orig in obj_coords:
                 output_grid[r_orig, c_orig] = background_color


    return output_grid.tolist()