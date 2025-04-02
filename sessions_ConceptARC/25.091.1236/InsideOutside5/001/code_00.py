import numpy as np
from collections import deque

"""
Transformation Rule:
1. Identify all distinct non-white objects (connected components of the same color) in the input grid.
2. For each object, determine if it is contained within another object. An object 'A' is considered contained within object 'B' if all pixels of 'A' are within the bounding box of 'B', and no pixel of 'A' is adjacent (including diagonally) to any pixel of 'B'.
3. Identify objects that are contained within at least one other object.
4. Identify objects that contain at least one other object.
5. Select only those objects that are contained but do not themselves contain any other object (i.e., the innermost contained objects).
6. Create an output grid of the same dimensions as the input, initialized with the background color (white, 0).
7. Draw the selected innermost objects onto the output grid in their original positions and colors. Discard all other objects.
"""

def _get_neighbors(r, c, rows, cols):
    """ Get 8-connectivity neighbors within grid bounds """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def _find_objects(grid):
    """ Finds all connected components (objects) of non-background colors. """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    object_id_counter = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    curr_r, curr_c = q.popleft()
                    obj_coords.add((curr_r, curr_c))
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)

                    # Find neighbors of the same color using 4-connectivity for object definition
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                         nr, nc = curr_r + dr, curr_c + dc
                         if 0 <= nr < rows and 0 <= nc < cols and \
                            not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                objects.append({
                    'id': object_id_counter,
                    'color': color,
                    'coords': obj_coords,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
                object_id_counter += 1
    return objects

def _is_strictly_contained(obj_a, obj_b, grid_shape):
    """ Checks if obj_a is strictly contained within obj_b without touching. """
    coords_a = obj_a['coords']
    coords_b = obj_b['coords']
    bbox_a = obj_a['bbox']
    bbox_b = obj_b['bbox']
    rows, cols = grid_shape

    # 1. Bounding box check: A's bbox must be strictly inside B's bbox
    if not (bbox_b[0] < bbox_a[0] and bbox_b[1] < bbox_a[1] and \
            bbox_a[2] < bbox_b[2] and bbox_a[3] < bbox_b[3]):
         # Allow bbox edges to touch if frame is thin
         if not (bbox_b[0] <= bbox_a[0] and bbox_b[1] <= bbox_a[1] and \
                 bbox_a[2] <= bbox_b[2] and bbox_a[3] <= bbox_b[3]):
            return False
         # If bounding boxes touch or overlap exactly, still need further checks


    # 2. Adjacency check: No pixel in A should be adjacent (8-way) to any pixel in B
    for r_a, c_a in coords_a:
        for nr, nc in _get_neighbors(r_a, c_a, rows, cols):
            if (nr, nc) in coords_b:
                return False # Adjacent to B

    # 3. Ensure A is actually "inside" B.
    # A simple proxy: check if any point in A can reach the boundary of B's bbox
    # without crossing B. A more robust check involves pathfinding, but let's
    # assume the adjacency check is sufficient for typical frame structures.
    # If A's bbox is inside B's bbox and they are not adjacent, it implies containment for simple shapes.

    # Check if A's coordinates are all contained within B's bounding box
    for r_a, c_a in coords_a:
        if not (bbox_b[0] <= r_a <= bbox_b[2] and bbox_b[1] <= c_a <= bbox_b[3]):
            return False # A pixel of A is outside B's bounding box

    return True


def transform(input_grid):
    """
    Identifies objects contained within other objects but not containing any themselves,
    and places these innermost objects on a new grid.
    """
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # 1. Find all objects
    objects = _find_objects(input_grid)
    if not objects:
        return output_grid

    num_objects = len(objects)
    is_contained_by = [set() for _ in range(num_objects)] # Stores IDs of containers for each object
    contains = [set() for _ in range(num_objects)]       # Stores IDs of contained objects for each object

    # 2. Determine containment relationships
    for i in range(num_objects):
        for j in range(num_objects):
            if i == j:
                continue
            obj_a = objects[i]
            obj_b = objects[j]
            # Check if object i is strictly contained within object j
            if _is_strictly_contained(obj_a, obj_b, (rows, cols)):
                is_contained_by[i].add(j)
                contains[j].add(i)

    # 3. Identify innermost objects
    innermost_objects = []
    for i in range(num_objects):
        # Object i is contained (is_contained_by[i] is not empty)
        # AND Object i does not contain any other object (contains[i] is empty)
        if is_contained_by[i] and not contains[i]:
            innermost_objects.append(objects[i])

    # 4. Construct the output grid
    for obj in innermost_objects:
        color = obj['color']
        for r, c in obj['coords']:
            output_grid[r, c] = color

    return output_grid