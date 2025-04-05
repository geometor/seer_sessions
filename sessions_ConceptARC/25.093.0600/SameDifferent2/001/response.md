```python
"""
The transformation rule operates on a 2D grid of integers (colors). It identifies connected components (objects) of the same non-zero color and selectively removes some objects based on their color, their neighbors, and whether the grid contains single or multiple distinct colors.

1.  **Object Identification:** Find all connected components (objects) of the same non-zero color using 4-connectivity (up, down, left, right).
2.  **Color Analysis:** Determine the set of unique non-zero colors present in the grid.
3.  **Conditional Logic:**
    *   **Single-Color Case:** If only one non-zero color exists in the grid:
        *   An object is REMOVED if it does NOT touch any of the grid boundaries (top, bottom, left, or right edge).
        *   Objects touching the boundary are KEPT.
    *   **Multi-Color Case:** If more than one non-zero color exists:
        *   **Neighbor Identification:** For each object, identify all neighboring objects (objects of different colors that share at least one edge).
        *   **Interaction Rules:** Apply specific removal rules based on pairs of interacting colors:
            *   If an object of color 7 touches an object of color 1, the color 7 object is marked for removal.
            *   If an object of color 1 touches an object of color 8, the color 1 object is marked for removal.
            *   If an object of color 3 touches an object of color 2, the color 3 object is marked for removal.
            *   (Note: These interactions are checked for all pairs. An object might be marked multiple times but is removed only once).
        *   **Special Rule for Color 1:** After applying interaction rules, check every object of color 1:
            *   If a color 1 object has NO neighbors OR only neighbors of color 1, it is marked for removal. This rule applies even if it wasn't marked by the interaction rules.
4.  **Output Generation:** Create a copy of the input grid. For every object marked for removal, set all its corresponding pixels in the output grid to 0.
"""

import numpy as np
from collections import deque

def find_objects(grid):
    """Finds all connected components (objects) in the grid."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    object_id_map = np.zeros_like(grid, dtype=int) # Map pixel to object index + 1
    
    object_index = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    coords.append((row, col))
                    object_id_map[row, col] = object_index + 1 # Store object index + 1
                    
                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                objects.append({'id': object_index, 'color': color, 'coords': coords})
                object_index += 1
                
    return objects, object_id_map

def get_neighbors(grid, objects, object_id_map):
    """Finds neighbors for each object."""
    rows, cols = grid.shape
    neighbors = {obj['id']: set() for obj in objects} # Stores neighbor object ids
    neighbor_colors = {obj['id']: set() for obj in objects} # Stores neighbor colors

    for obj in objects:
        obj_id = obj['id']
        obj_color = obj['color']
        
        for r, c in obj['coords']:
            # Check adjacent cells
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    neighbor_val = grid[nr, nc]
                    if neighbor_val != 0 and neighbor_val != obj_color:
                        neighbor_obj_id = object_id_map[nr, nc] - 1 # Get neighbor object index
                        if neighbor_obj_id != obj_id and neighbor_obj_id >= 0 : # Ensure it's a valid, different object
                           neighbors[obj_id].add(neighbor_obj_id)
                           neighbor_colors[obj_id].add(grid[nr,nc]) # store color of neighbour

    # Add neighbor colors info to the objects list
    for obj in objects:
        obj['neighbor_ids'] = neighbors[obj['id']]
        obj['neighbor_colors'] = neighbor_colors[obj['id']]
        # Get the actual colors of the neighbor objects
        #obj['neighbor_colors'] = {objects[nid]['color'] for nid in neighbors[obj['id']]}

    return objects


def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    """
    grid = np.array(input_grid)
    rows, cols = grid.shape
    
    # 1. Find Objects
    objects, object_id_map = find_objects(grid)
    if not objects:
        return grid.tolist() # Return original if no objects

    # 2. Color Analysis
    unique_colors = set(obj['color'] for obj in objects)
    num_unique_colors = len(unique_colors)

    # 3. Initialize Removal Set
    objects_to_remove = set() # Store ids of objects to remove

    # Add neighbor information to objects
    objects = get_neighbors(grid, objects, object_id_map)

    # 4. Conditional Logic
    if num_unique_colors == 1:
        # Single-Color Case
        for obj in objects:
            touches_boundary = False
            for r, c in obj['coords']:
                if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                    touches_boundary = True
                    break
            if not touches_boundary:
                objects_to_remove.add(obj['id'])
    else:
        # Multi-Color Case
        
        # Apply Interaction Rules
        processed_interactions = set() # To avoid processing A-B and B-A separately for removal logic
        for obj_A in objects:
            obj_A_id = obj_A['id']
            obj_A_color = obj_A['color']
            
            for neighbor_id in obj_A['neighbor_ids']:
                obj_B = objects[neighbor_id] # Find the neighbor object
                obj_B_color = obj_B['color']
                
                # Ensure we process each pair once and colors are different
                interaction_pair = tuple(sorted((obj_A_id, neighbor_id)))
                if interaction_pair in processed_interactions:
                    continue
                processed_interactions.add(interaction_pair)

                colors_involved = {obj_A_color, obj_B_color}

                # Rule: 7 touches 1 -> remove 7
                if colors_involved == {1, 7}:
                    if obj_A_color == 7: objects_to_remove.add(obj_A_id)
                    if obj_B_color == 7: objects_to_remove.add(neighbor_id)
                        
                # Rule: 1 touches 8 -> remove 1
                if colors_involved == {1, 8}:
                    if obj_A_color == 1: objects_to_remove.add(obj_A_id)
                    if obj_B_color == 1: objects_to_remove.add(neighbor_id)

                # Rule: 3 touches 2 -> remove 3
                if colors_involved == {2, 3}:
                    if obj_A_color == 3: objects_to_remove.add(obj_A_id)
                    if obj_B_color == 3: objects_to_remove.add(neighbor_id)

        # Apply Special Rule for Color 1
        for obj in objects:
            if obj['color'] == 1:
                # Check if it touches any non-1 color
                touches_non_1 = any(nc != 1 for nc in obj['neighbor_colors'])
                # Remove if it does NOT touch any non-1 color (i.e., isolated or only touches other 1s)
                if not touches_non_1:
                     objects_to_remove.add(obj['id'])


    # 5. Construct Output
    output_grid = np.copy(grid)
    for obj_id in objects_to_remove:
        # Find the object with this id (could optimize with a dict lookup)
        obj_to_remove = next((obj for obj in objects if obj['id'] == obj_id), None)
        if obj_to_remove:
            for r, c in obj_to_remove['coords']:
                output_grid[r, c] = 0
                
    return output_grid.tolist()
```