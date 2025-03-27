Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np
from collections import deque

"""
Identifies 'H' shapes made of a single color in the input grid. An 'H' shape 
is defined as a contiguous object of a single color that completely encloses 
exactly two distinct regions of white (color 0) pixels. 

The transformation rule fills these enclosed white regions based on the color 
of the 'H' shape and its aspect ratio:
- Green (3) H-shape: Fill with Green (3).
- Azure (8) H-shape: Fill with Blue (1).
- Red (2) H-shape: Fill with Orange (7).
- Yellow (4) H-shape:
    - If height > width: Fill with Magenta (6).
    - If width > height: Fill with Gray (5).
    - If height == width: No fill.
- H-shapes of other colors (e.g., Orange 7, Gray 5) are not filled.
- Objects that are not H-shapes (do not enclose exactly two white regions) are 
  left unchanged.
- White regions not enclosed by a single object are left unchanged.

Enclosure check: A white region is considered enclosed by an object if it does 
not touch the grid boundary and all its adjacent (4-directionally) non-white 
neighbors belong to that single object.
"""

def find_objects_and_map(grid, H, W):
    """
    Finds all contiguous non-white objects using 8-way connectivity.
    Returns:
        objects (dict): {object_id: {'coords': set((r,c)), 'color': int}}
        object_map (np.array): Grid where each cell contains the object_id it belongs to, or -1.
    """
    object_map = np.full((H, W), -1, dtype=int)
    objects = {}
    visited = np.zeros((H, W), dtype=bool)
    object_id_counter = 0

    for r in range(H):
        for c in range(W):
            if not visited[r, c] and grid[r, c] != 0:
                color = grid[r, c]
                component_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                current_id = object_id_counter

                while q:
                    row, col = q.popleft()
                    component_coords.add((row, col))
                    object_map[row, col] = current_id
                    
                    # 8-way connectivity for object pixels
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < H and 0 <= nc < W and \
                               not visited[nr, nc] and grid[nr, nc] == color:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                
                objects[current_id] = {'coords': component_coords, 'color': color}
                object_id_counter += 1
                
    return objects, object_map

def find_enclosed_white_regions(grid, H, W, object_map):
    """
    Finds white regions enclosed by single objects.
    Uses 4-way connectivity for white regions and neighbor checking.
    Returns:
        enclosed_regions_by_object (dict): {object_id: [set((r,c)), ...]}
    """
    visited_white = np.zeros((H, W), dtype=bool)
    enclosed_regions_by_object = {} 

    for r in range(H):
        for c in range(W):
            if not visited_white[r, c] and grid[r, c] == 0:
                white_component_coords = set()
                q = deque([(r, c)])
                visited_white[r, c] = True
                is_on_boundary = False
                neighbor_object_ids = set()

                component_queue_for_neighbor_check = deque([(r,c)]) # Keep track for neighbor check after finding component

                while q:
                    row, col = q.popleft()
                    white_component_coords.add((row, col))

                    if row == 0 or row == H - 1 or col == 0 or col == W - 1:
                        is_on_boundary = True # Mark but continue BFS to find full component

                    # 4-way connectivity for white region pixels
                    for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < H and 0 <= nc < W:
                            if grid[nr, nc] == 0:
                                if not visited_white[nr, nc]:
                                    visited_white[nr, nc] = True
                                    q.append((nr, nc))
                                    component_queue_for_neighbor_check.append((nr,nc))
                            # else: # Non-white neighbor, check handled below
                                
                # After finding the component, check its neighbors if not on boundary
                if not is_on_boundary:
                    unique_neighbor_id = -1
                    is_enclosed_
---
