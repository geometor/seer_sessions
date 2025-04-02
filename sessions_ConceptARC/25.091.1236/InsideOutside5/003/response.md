Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np
from collections import deque

"""
Transformation Rule:
1. Identify all distinct non-white objects (connected components using 4-connectivity).
2. Determine all pairs of objects (A, B) where A is strictly contained within B.
   Strict containment requires:
   - A's bounding box must be within or identical to B's bounding box.
   - No pixel of A can be adjacent (8-way connectivity) to any pixel of B.
   - A flood fill starting from any pixel of A, moving only onto background (0) or other pixels of A, must not be able to reach the grid boundary without crossing object B or any other object.
3. Check if any Azure (color 8) object is involved in any such containment relationship found in step 2 (either as the container 'B' or the contained object 'A').
4. **Conditional Output Generation:**
   a. **If any Azure object was involved in containment:** The output grid contains *only* those Azure (8) objects that were identified as being part of a containment relationship (either containing or being contained). All other pixels are background (0).
   b. **If NO Azure object was involved in containment:** The output grid contains only the "innermost" objects. An object is innermost if it is contained by at least one other object, but does not itself contain any other object. All other pixels are background (0).
5. Draw the selected objects onto the output grid in their original positions and colors.
"""

def _get_neighbors(r, c, rows, cols, connectivity=8):
    """ Get neighbors within grid bounds based on connectivity. """
    neighbors = []
    if connectivity == 8:
        deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    else: # 4-connectivity
        deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in deltas:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def _find_objects(grid):
    """ Finds all connected components (objects) of non-background colors using 4-connectivity. """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    object_id_counter = 0

    for r in range(rows):
        for c in range(cols):
            # If pixel is non-background and not yet visited as part of an object
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_coords = set()
                # Use BFS to find all connected pixels of the same color (4-connectivity)
                q = deque([(r, c)])
                visited[r, c] = True # Mark as visited for the main loop
                component_visited = set([(r,c)]) # Track visited for this specific component BFS

                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    curr_r, curr_c = q.popleft()
                    obj_coords.add((curr_r, curr_c))
                    # Update bounding box
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)

                    # Explore 4-connected neighbors
                    for nr, nc in _get_neighbors(curr_r, curr_c, rows, cols, connectivity=4):
                         # Check if neighbor is within bounds, same color, and not visited for this component
                         if (nr, nc) not in component_visited and grid[nr, nc] == color:
                            visited[nr, nc] = True # Mark globally visited
                            component_visited.add((nr, nc))
                            q.append((nr, nc))

                # Store the found object if it has coordinates
                if obj_coords:
                    objects.append({
                        'id': object_id_counter,
                        'color': color,
                        'coords': obj_coords,
                        'bbox': (min_r, min_c, max_r, max_c) # Store as (min_row, min_col, max_row, max_col)
                    })
                    object_id_counter += 1
    return objects

def _is_strictly_contained(obj_a, obj_b, grid):
    """ Checks if obj_a is strictly contained within obj_b without touching, using flood fill reachability. """
    rows, cols = grid.shape
    coords_a = obj_a['coords']
    coords_b = obj_b['coords']
    bbox_a = obj_a['bbox']
    bbox_b = obj_b['bbox']
    color_a = obj_a['color']

    # --- Quick Checks ---
    # 1. Bounding Box Check: A's bbox must be inside or touching B's bbox.
    if not (bbox_b[0] <= bbox_a[0] and bbox_b[1] <= bbox_a[1] and \
            bbox_a[2] <= bbox_b[2] and bbox_a[3] <= bbox_b[3]):
        return False # A is not even within B's bounding box area.

    # 2. Adjacency Check: No pixel in A should be adjacent (8-way) to any pixel in B.
    for r_a, c_a in coords_a:
        for nr, nc in _get_neighbors(r_a, c_a, rows, cols, connectivity=8):
            if (nr, nc) in coords_b:
                return False # A is touching B.

    # --- Reachability Check (Flood Fill) ---
    # Goal: Can we reach the grid edge starting from A, moving only on background (0) or A's pixels?
    # If yes, A is not contained. If no, A is contained.
    # We treat B and all other objects as impassable walls.

    # Optimization: If A touches the grid edge directly, it cannot be contained.
    for r_a, c_a in coords_a:
         if r_a == 0 or r_a == rows - 1 or c_a == 0 or c_a == cols - 1:
             return False # Object A touches the edge, cannot be contained.

    # Prepare for flood fill
    q = deque()
    visited_fill = set()

    # Start fill from one pixel of A (any pixel will do)
    start_r, start_c = next(iter(coords_a))
    q.append((start_r, start_c))
    visited_fill.add((start_r, start_c))
    visited_fill.update(coords_a) # Treat all of A's pixels as visited initially to allow movement within A

    while q:
        r, c = q.popleft()

        # Check neighbors (use 4-connectivity for flood fill path)
        for nr, nc in _get_neighbors(r, c, rows, cols, connectivity=4):
            if (nr, nc) not in visited_fill:
                # Check if the neighbor is on the grid edge
                if nr == 0 or nr == rows - 1 or nc == 0 or nc == cols - 1:
                    # Reachable only if it's background (0)
                    
---
