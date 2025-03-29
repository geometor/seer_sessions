```python
import numpy as np
from collections import deque

"""
The transformation rule operates based on the adjacency of specific object types:

1.  **Single Pixel Expansion:** If two single pixels (1x1 objects) of different colors (A and B) are adjacent (sharing an edge or corner), pixel B expands into a 3x3 cross shape of its original color, centered at its original position. Pixel A remains unchanged.

2.  **Adjacent Square Transformation:** If two solid square objects (X and Y) of the *same size* (NxN) but potentially different colors are adjacent along a full edge:
    a.  A new (3N)x(3N) area is defined, centered where square Y was located.
    b.  This area is filled with the color of square X.
    c.  Square Y (its color and NxN size) is placed back into the central NxN block of this area.
    d.  The NxN block within the (3N)x(3N) area that is in the *opposite* direction from the center compared to X's original position relative to Y (e.g., if X was Above Y, the block Below Y is targeted) is filled with white (0).
    e.  This new pattern replaces the original area in the output grid, effectively removing X and modifying the area around Y.

3.  **Default Copy:** Any object not participating in one of the above transformations is copied directly from the input to the output.

The rules are applied prioritizing rule 1, then rule 2. Once an object participates in a transformation, it cannot participate in another. Transformations must respect grid boundaries.
"""

# Helper function to find connected components (objects)
def find_objects(grid):
    """
    Identifies distinct contiguous objects of non-background colors in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, each representing an object with its properties:
              'id': A unique identifier.
              'color': The color of the object.
              'pixels': A set of (row, col) tuples representing the object's pixels.
              'bbox': A tuple (min_row, min_col, max_row, max_col) for the bounding box.
              'shape': 'single_pixel', 'square', or 'other'.
              'size': N if shape is 'square', 1 if 'single_pixel', None otherwise.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape
    obj_id_counter = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                obj_id_counter += 1
                color = grid[r, c]
                pixels = set()
                q = deque([(r, c)])
                visited.add((r, c))
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    pixels.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors (8 directions)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == color and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                q.append((nr, nc))

                # Determine shape and size
                obj_shape = 'other'
                obj_size = None
                if len(pixels) == 1:
                    obj_shape = 'single_pixel'
                    obj_size = 1
                else:
                    height = max_r - min_r + 1
                    width = max_c - min_c + 1
                    if height == width and len(pixels) == height * width:
                         # Check if all pixels within bbox are part of the object
                         is_solid = True
                         for br in range(min_r, max_r + 1):
                             for bc in range(min_c, max_c + 1):
                                 if (br, bc) not in pixels:
                                     is_solid = False
                                     break
                             if not is_solid:
                                 break
                         if is_solid:
                            obj_shape = 'square'
                            obj_size = height # N

                objects.append({
                    'id': obj_id_counter,
                    'color': color,
                    'pixels': pixels,
                    'bbox': (min_r, min_c, max_r, max_c),
                    'shape': obj_shape,
                    'size': obj_size
                })
    return objects

# Helper function to check adjacency (8 directions)
def are_adjacent(obj1, obj2):
    """Checks if two objects are adjacent (sharing edge or corner)."""
    for r1, c1 in obj1['pixels']:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r1 + dr, c1 + dc
                if (nr, nc) in obj2['pixels']:
                    return True
    return False

# Helper function to check edge adjacency (4 directions)
def have_edge_adjacency(obj1, obj2):
    """Checks if two objects share a full edge (orthogonal adjacency)."""
    for r1, c1 in obj1['pixels']:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r1 + dr, c1 + dc
            if (nr, nc) in obj2['pixels']:
                return True
    return False

# Helper function to get relative position for edge-adjacent squares
def get_relative_position(ref_obj, other_obj):
    """Determines relative position (Above, Below, Left, Right) of other_obj w.r.t ref_obj."""
    ref_min_r, ref_min_c, _, _ = ref_obj['bbox']
    other_min_r, other_min_c, _, _ = other_obj['bbox']

    if other_min_r < ref_min_r: return "Above"
    if other_min_r > ref_min_r: return "Below"
    if other_min_c < ref_min_c: return "Left"
    if other_min_c > ref_min_c: return "Right"
    return None # Should not happen for edge-adjacent squares

def transform(input_grid):
    """
    Applies the transformation rules based on object adjacency.

    Args:
        input_grid (np.ndarray): The input 2D numpy array.

    Returns:
        np.ndarray: The transformed 2D numpy array.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    objects = find_objects(input_grid)
    processed_object_ids = set()

    # --- Rule 1: Single Pixel Expansion ---
    pixel_pairs_to_process = []
    object_map = {obj['id']: obj for obj in objects}

    # Find candidate pairs first
    for i in range(len(objects)):
        obj_a = objects[i]
        if obj_a['shape'] != 'single_pixel' or obj_a['id'] in processed_object_ids:
            continue
        for j in range(i + 1, len(objects)):
            obj_b = objects[j]
            if obj_b['shape'] != 'single_pixel' or obj_b['id'] in processed_object_ids:
                continue

            if are_adjacent(obj_a, obj_b):
                # Order doesn't strictly matter here, but let's pick one to expand
                # The examples suggest *one* of the pair expands. Let's arbitrarily
                # choose the one with the higher ID to expand for consistency,
                # although the examples aren't explicit on *which* one expands.
                # Let's re-examine Example 2: red (2) and azure (8) -> azure expands.
                # Example 3: green (3) and red (2) -> green expands.
                # Example 3: azure (8) and red (2) -> no expansion (not single pixels)
                # It seems the choice might depend on colors or positions, but let's
                # try expanding the second one found (obj_b).
                # No, let's follow the observation: object B expands.
                # In train_2: red=A(2), azure=B(8). Azure expands.
                # In train_3: green=A(3), red=B(2). Green expands. Hmm, rule isn't simple A/B.
                # Let's stick to: if two adjacent single pixels found, one expands.
                # We'll pick B (the second one in the loop) to expand for now.
                pixel_pairs_to_process.append((obj_a['id'], obj_b['id']))


    # Apply transformations for single pixels
    for id_a, id_b in pixel_pairs_to_process:
         if id_a not in processed_object_ids and id_b not in processed_object_ids:
            obj_a = object_map[id_a]
            obj_b = object_map[id_b]

            # Get the single pixel coordinate for B
            (r_b, c_b) = next(iter(obj_b['pixels']))
            color_b = obj_b['color']

            # Draw 3x3 cross of color_b centered at (r_b, c_b)
            # Center pixel
            if 0 <= r_b < rows and 0 <= c_b < cols:
                 output_grid[r_b, c_b] = color_b # Ensure center is correct color
            # Orthogonal neighbors
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r_b + dr, c_b + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    output_grid[nr, nc] = color_b

            # Mark both as processed
            processed_object_ids.add(id_a)
            processed_object_ids.add(id_b)


    # --- Rule 2: Adjacent Square Transformation ---
    square_pairs_to_process = []
    # Find candidate pairs
    for i in range(len(objects)):
        obj_x = objects[i]
        if obj_x['shape'] != 'square' or obj_x['id'] in processed_object_ids:
            continue
        for j in range(len(objects)): # Check all others, not just i+1
            if i == j: continue
            obj_y = objects[j]
            if obj_y['shape'] != 'square' or obj_y['id'] in processed_object_ids:
                continue

            # Check for same size and edge adjacency
            if obj_x['size'] == obj_y['size'] and have_edge_adjacency(obj_x, obj_y):
                square_pairs_to_process.append((obj_x['id'], obj_y['id']))

    # Apply transformations for squares
    for id_x, id_y in square_pairs_to_process:
        if id_x not in processed_object_ids and id_y not in processed_object_ids:
            obj_x = object_map[id_x]
            obj_y = object_map[id_y]

            n = obj_x['size'] # or obj_y['size'], they are the same
            color_x = obj_x['color']
            color_y = obj_y['color']
            min_r_y, min_c_y, max_r_y, max_c_y = obj_y['bbox']

            # Determine center of the 3Nx3N area (relative to Y's top-left)
            center_r_3n = min_r_y - n
            center_c_3n = min_c_y - n

            # Fill the 3Nx3N area with color_x
            for r in range(center_r_3n, center_r_3n + 3 * n):
                for c in range(center_c_3n, center_c_3n + 3 * n):
                    if 0 <= r < rows and 0 <= c < cols:
                        output_grid[r, c] = color_x

            # Place object Y back in the center
            for r in range(min_r_y, max_r_y + 1):
                for c in range(min_c_y, max_c_y + 1):
                     if 0 <= r < rows and 0 <= c < cols: # Should always be true if Y was in grid
                         output_grid[r, c] = color_y

            # Determine relative position of X to Y
            relative_pos = get_relative_position(obj_y, obj_x) # Position of X relative to Y

            # Calculate coordinates for the "opposite" NxN block to clear
            clear_r_start, clear_c_start = -1, -1
            if relative_pos == "Above":   clear_r_start, clear_c_start = min_r_y + n, min_c_y # Below
            elif relative_pos == "Below": clear_r_start, clear_c_start = min_r_y - n, min_c_y # Above
            elif relative_pos == "Left":  clear_r_start, clear_c_start = min_r_y, min_c_y + n # Right
            elif relative_pos == "Right": clear_r_start, clear_c_start = min_r_y, min_c_y - n # Left

            # Clear the opposite block
            if clear_r_start != -1:
                for r in range(clear_r_start, clear_r_start + n):
                    for c in range(clear_c_start, clear_c_start + n):
                        if 0 <= r < rows and 0 <= c < cols:
                            output_grid[r, c] = 0 # white background

            # Mark both as processed
            processed_object_ids.add(id_x)
            processed_object_ids.add(id_y)


    # Objects not processed by rule 1 or 2 are implicitly kept
    # because we started with a copy of the input grid and only modified
    # the relevant areas for the processed objects.
    # For Rule 2, object X *is* effectively removed/overwritten by the new pattern.

    return output_grid

```