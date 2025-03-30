```python
import numpy as np
from collections import deque

"""
Identify all distinct non-background objects (contiguous blocks of the same color) in the input grid. 
Determine the top-most row containing any object pixel (min_start_row) and the bottom-most row containing any object pixel (max_end_row).
Identify the set of objects that have at least one pixel in the min_start_row ('top_objects') and the set of objects that have at least one pixel in the max_end_row ('bottom_objects').

Select a single target object based on the following prioritized rules:

1.  **Unique Top & Unique Bottom:** If there is exactly one top_object and exactly one bottom_object:
    a. If they are the same object, select it.
    b. If they are different objects, compare their pixel counts. Select the object with the larger pixel count. 
    c. If their pixel counts are equal, select the top_object.

2.  **Unique Top Only:** If there is exactly one top_object, select it (regardless of how many bottom_objects there are, unless Rule 1 applied).

3.  **Multiple Top Objects:** If there are multiple top_objects: Select the top_object that has the smallest starting column index (left-most).

4.  **Unique Bottom Only:** (Only if rules 1-3 do not apply, meaning zero top_objects which shouldn't happen if there are objects, or multiple top_objects were already handled) If there is exactly one bottom_object, select it.

5.  **Fallback (Should not be reached with ARC constraints and above rules):** If no object is selected by the above rules (e.g. multiple top and multiple bottom objects, but none are unique top/bottom according to rule 1), select the first object found by the object detection algorithm.

Finally, create a new grid containing only the selected target object, cropped to its minimal bounding box, preserving its shape and color against a background of white (0).
"""

# Imports included within the function where needed to adhere to template request
# Helper function outside transform for clarity

def find_objects(grid):
    """
    Finds all distinct contiguous objects of non-background color in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains its 'color', 'pixels' (list of (r, c) tuples),
              'pixel_count', 'start_row' (min row), 'end_row' (max row), 
              'start_col' (min col), and 'bounding_box' (min_r, min_c, max_r, max_c).
              Returns an empty list if no objects are found.
    """
    # from collections import deque - Import implicitly available or assumed top-level
    # import numpy as np - Import implicitly available or assumed top-level
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
                
                pixel_set = set() # Use set for efficient coordinate tracking during BFS
                pixel_set.add((r,c))

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
                            if (nr, nc) not in pixel_set: # Check if already added to queue/visited in this object's BFS
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                pixel_set.add((nr, nc))
                            
                if pixels:
                    # Ensure pixels list contains unique coordinates before counting
                    unique_pixels = list(pixel_set) 
                    objects.append({
                        'id': len(objects), # Add a unique ID for comparison
                        'color': color,
                        'pixels': unique_pixels, 
                        'pixel_count': len(unique_pixels),
                        'start_row': min_r,
                        'end_row': max_r,
                        'start_col': min_c,
                        'bounding_box': (min_r, min_c, max_r, max_c) 
                    })
                    
    return objects

def transform(input_grid):
    """
    Transforms the input grid by identifying objects, selecting one based on positional
    rules (top-most, bottom-most, left-most) and size, and extracting it to a new grid.
    """
    # import numpy as np - Import implicitly available or assumed top-level
    
    grid_np = np.array(input_grid, dtype=int)
    
    # 1. Identify all objects
    objects = find_objects(grid_np)

    # Handle edge case: no objects found
    if not objects:
        # Return an empty grid or a small default grid as appropriate
        return np.array([[]], dtype=int).tolist() 
        # Alternative: return np.zeros((1, 1), dtype=int).tolist() 

    # Handle edge case: only one object found
    if len(objects) == 1:
        target_object = objects[0]
    else:
        # 2. Determine overall top-most and bottom-most rows
        min_start_row = min(obj['start_row'] for obj in objects)
        max_end_row = max(obj['end_row'] for obj in objects)

        # 3. Identify objects touching the top-most row and bottom-most row
        top_objects = [obj for obj in objects if obj['start_row'] == min_start_row]
        bottom_objects = [obj for obj in objects if obj['end_row'] == max_end_row]

        # 4. Apply selection rules
        target_object = None

        # Rule 1: Unique Top & Unique Bottom
        if len(top_objects) == 1 and len(bottom_objects) == 1:
            top_obj = top_objects[0]
            bottom_obj = bottom_objects[0]
            # Check if they are the same object
            if top_obj['id'] == bottom_obj['id']:
                 target_object = top_obj # Rule 1a
            # If different objects, compare sizes
            elif top_obj['pixel_count'] >= bottom_obj['pixel_count']:
                target_object = top_obj # Rule 1c (includes equality)
            else:
                target_object = bottom_obj # Rule 1b
        
        # Rule 2: Unique Top Only (and Rule 1 did not apply)
        elif target_object is None and len(top_objects) == 1:
            target_object = top_objects[0]
            
        # Rule 3: Multiple Top Objects (and Rules 1, 2 did not apply)
        elif target_object is None and len(top_objects) > 1:
            # Select the one with the minimum start_col (left-most)
            target_object = min(top_objects, key=lambda obj: obj['start_col'])

        # Rule 4: Unique Bottom Only (and Rules 1-3 did not apply)
        # This case implies len(top_objects) is 0 or >1, but rule 3 handles >1.
        # So this primarily covers the case where no objects start at min_start_row (unlikely if objects exist)
        # OR where rule 1 didn't apply (e.g. multiple bottom objects) but we still need a selection.
        # Re-evaluating: The logic flow means if we reach here, either:
        #   a) len(top) == 0 (impossible if objects exist)
        #   b) len(top) > 1 (handled by rule 3)
        #   c) len(top) == 1 BUT len(bottom) != 1 (handled by rule 2)
        # Therefore, this rule might be redundant or cover an edge case not present in examples.
        # Let's keep the logic as intended by the natural language description for now.
        elif target_object is None and len(bottom_objects) == 1:
             target_object = bottom_objects[0]

        # Rule 5: Fallback (if no object selected yet)
        if target_object is None:
            # This case should ideally not be reached given the prior rules and typical ARC task structures.
            # If it is, we default to the first object found.
             target_object = objects[0] 

    # 5. Extract the selected object into a new grid
    min_r, min_c, max_r, max_c = target_object['bounding_box']
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # Create the output grid initialized to background color (white=0)
    output_grid = np.zeros((height, width), dtype=int)

    # Place the object's pixels onto the output grid relative to its bounding box
    for r, c in target_object['pixels']:
        # Calculate relative coordinates within the output grid
        relative_r = r - min_r
        relative_c = c - min_c
        # Ensure coordinates are within bounds (should be, but good practice)
        if 0 <= relative_r < height and 0 <= relative_c < width:
             output_grid[relative_r, relative_c] = target_object['color']

    # Return the result as a list of lists
    return output_grid.tolist()
```