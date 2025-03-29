import numpy as np
from collections import deque

def find_objects(grid):
    """
    Identifies connected components of non-background pixels in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of objects. Each object is represented as a dictionary
              containing 'pixels' (a list of (r, c, color) tuples) and
              bounding box information ('min_r', 'max_r', 'min_c', 'max_c').
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    background_color = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color and not visited[r, c]:
                obj_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    curr_r, curr_c = q.popleft()
                    color = grid[curr_r, curr_c]
                    obj_pixels.append((curr_r, curr_c, color))

                    # Update bounds
                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)

                    # Check neighbors (4-directional connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != background_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                objects.append({
                    'pixels': obj_pixels,
                    'min_r': min_r,
                    'max_r': max_r,
                    'min_c': min_c,
                    'max_c': max_c
                })
    return objects

def transform(input_grid):
    """
    Shifts non-background objects horizontally to the right until they hit
    the grid boundary or another object. When objects moving rightward would
    collide in the same row(s), the object that started further left stops
    just before colliding with the final position of the object that started
    further to the right.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    rows, cols = input_grid.shape
    background_color = 0
    output_grid = np.full((rows, cols), background_color, dtype=input_grid.dtype)

    # 1. Identify all distinct objects and their properties
    objects = find_objects(input_grid)
    if not objects:
        return output_grid # Return empty grid if no objects

    # 2. Calculate initial potential shift for each object
    for i, obj in enumerate(objects):
        obj['id'] = i # Assign an ID for tracking
        potential_shift = cols - 1 - obj['max_c']
        obj['final_shift'] = potential_shift # Initialize final_shift

    # 3. Iteratively resolve collisions until shifts stabilize
    shifts_changed = True
    while shifts_changed:
        shifts_changed = False
        # Sort objects primarily by initial min_c (left-to-right) to potentially
        # speed up convergence, though the logic should handle any order.
        # objects.sort(key=lambda o: o['min_c']) # Optional sort

        for i in range(len(objects)):
            obj_a = objects[i]
            potential_a_min_c = obj_a['min_c'] + obj_a['final_shift']
            potential_a_max_c = obj_a['max_c'] + obj_a['final_shift']

            for j in range(len(objects)):
                if i == j:
                    continue
                obj_b = objects[j]

                # Check for row overlap
                rows_overlap = max(obj_a['min_r'], obj_b['min_r']) <= min(obj_a['max_r'], obj_b['max_r'])
                if not rows_overlap:
                    continue

                potential_b_min_c = obj_b['min_c'] + obj_b['final_shift']
                potential_b_max_c = obj_b['max_c'] + obj_b['final_shift']

                # Check for potential horizontal collision (only if A is to the left of B initially)
                # A potential collision occurs if A's potential final position overlaps or is to the right of B's
                if obj_a['min_c'] < obj_b['min_c']:
                    # Check if A's potential end position would collide with B's potential end position
                    # A collision happens if A's right edge would be >= B's left edge in their potential final positions
                    if potential_a_max_c >= potential_b_min_c:
                         # A is blocked by B. Calculate the maximum shift A can make.
                         # A's rightmost column (max_c) must end up at B's leftmost column (min_c) - 1
                         max_allowed_shift_for_a = potential_b_min_c - 1 - obj_a['max_c']

                         # Ensure shift doesn't become negative if objects are already touching/overlapping somehow (shouldn't happen with rightward shift)
                         max_allowed_shift_for_a = max(0, max_allowed_shift_for_a)

                         # Update A's shift if the calculated limit is smaller than its current shift
                         if max_allowed_shift_for_a < obj_a['final_shift']:
                             obj_a['final_shift'] = max_allowed_shift_for_a
                             shifts_changed = True # Mark that a shift was adjusted

    # 4. Create the output grid by placing objects at their final positions
    for obj in objects:
        shift = obj['final_shift']
        for r, c, color in obj['pixels']:
            new_c = c + shift
            # Ensure the new position is within bounds (should be guaranteed by logic, but good practice)
            if 0 <= r < rows and 0 <= new_c < cols:
                output_grid[r, new_c] = color

    return output_grid