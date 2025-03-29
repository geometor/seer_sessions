import numpy as np
from collections import deque

"""
Identifies a 'frame' object (color 2) and 'content' objects (color 5) initially located inside the frame.
The transformation involves:
1. Erasing the content objects from their original positions inside the frame (setting them to background color 0).
2. Determining the closest boundary (top, bottom, left, or right) of the frame to each content object.
3. Reflecting each content object horizontally if the closest boundary is left/right, or vertically if the closest boundary is top/bottom.
4. Placing the reflected content object outside the frame, adjacent to the boundary it was reflected from, with a one-pixel gap.
The frame itself remains unchanged.
"""

def find_objects(grid, color):
    """Finds all connected objects of a given color."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.popleft()
                    obj_coords.append((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                objects.append({
                    'coords': obj_coords,
                    'bbox': {'min_r': min_r, 'max_r': max_r, 'min_c': min_c, 'max_c': max_c},
                    'color': color
                })
    return objects

def get_bounding_box(coords):
    """Calculates the bounding box for a set of coordinates."""
    if not coords:
        return None
    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)
    return {'min_r': min_r, 'max_r': max_r, 'min_c': min_c, 'max_c': max_c}


def transform(input_grid):
    """
    Moves and reflects gray objects found inside a red frame to the outside.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    height, width = output_grid.shape

    # --- Step 1 & 2: Identify Frame and Content Objects ---
    frame_objects = find_objects(input_grid_np, 2) # Red color
    content_objects = find_objects(input_grid_np, 5) # Gray color

    # Assume there is only one frame object for simplicity
    if not frame_objects:
        return output_grid # No frame, nothing to do

    frame = frame_objects[0]
    frame_bbox = frame['bbox']
    frame_coords_set = set(frame['coords']) # For quick lookup

    internal_objects_to_process = []

    # Identify content objects *inside* the frame
    # An object is inside if all its pixels are within the frame's bbox *and* not part of the frame itself
    for obj in content_objects:
        is_inside = True
        for r, c in obj['coords']:
            if not (frame_bbox['min_r'] < r < frame_bbox['max_r'] and
                    frame_bbox['min_c'] < c < frame_bbox['max_c']):
                 is_inside = False
                 break
            # Double check it's not accidentally overlapping a thick frame part
            # This check might be redundant if frame finding is robust and only finds the outer layer
            # if (r,c) in frame_coords_set:
            #     is_inside = False
            #     break
        if is_inside:
            internal_objects_to_process.append(obj)

    # --- Step 4: Erase Content Inside Frame ---
    for obj in internal_objects_to_process:
        for r, c in obj['coords']:
            output_grid[r, c] = 0 # Set to background white

    # --- Step 5: Transform and Relocate Content ---
    for obj in internal_objects_to_process:
        coords = obj['coords']
        obj_bbox = obj['bbox']
        obj_height = obj_bbox['max_r'] - obj_bbox['min_r'] + 1
        obj_width = obj_bbox['max_c'] - obj_bbox['min_c'] + 1

        # --- Step 5a: Find Nearest Boundary ---
        dist_top = obj_bbox['min_r'] - frame_bbox['min_r']
        dist_bottom = frame_bbox['max_r'] - obj_bbox['max_r']
        dist_left = obj_bbox['min_c'] - frame_bbox['min_c']
        dist_right = frame_bbox['max_c'] - obj_bbox['max_c']

        distances = {
            'top': dist_top,
            'bottom': dist_bottom,
            'left': dist_left,
            'right': dist_right
        }
        # Find the minimum non-negative distance. Handle cases where object touches boundary (dist=1)
        min_dist = float('inf')
        nearest_boundary = None
        for boundary, dist in distances.items():
             # Consider only positive distances (pixels inside the frame bbox edges)
             if dist > 0 and dist < min_dist:
                 min_dist = dist
                 nearest_boundary = boundary
             # If multiple boundaries have the same minimum distance, prioritize (e.g., top > bottom > left > right)
             elif dist > 0 and dist == min_dist:
                 priority = {'top': 4, 'bottom': 3, 'left': 2, 'right': 1}
                 if priority.get(boundary, 0) > priority.get(nearest_boundary, 0):
                     nearest_boundary = boundary

        if nearest_boundary is None: # Should not happen for objects strictly inside
            continue

        # --- Step 5b: Reflect ---
        reflected_coords_relative = []
        for r, c in coords:
            rel_r = r - obj_bbox['min_r']
            rel_c = c - obj_bbox['min_c']

            if nearest_boundary in ['left', 'right']: # Horizontal reflection
                reflected_c = (obj_width - 1) - rel_c
                reflected_coords_relative.append((rel_r, reflected_c))
            else: # Vertical reflection ('top', 'bottom')
                reflected_r = (obj_height - 1) - rel_r
                reflected_coords_relative.append((reflected_r, rel_c))

        # --- Step 5c: Calculate New Position ---
        new_top_left_r, new_top_left_c = -1, -1 # Initialize invalid

        if nearest_boundary == 'left':
            new_top_left_r = obj_bbox['min_r']
            new_top_left_c = frame_bbox['min_c'] - 1 - obj_width
        elif nearest_boundary == 'right':
            new_top_left_r = obj_bbox['min_r']
            new_top_left_c = frame_bbox['max_c'] + 2
        elif nearest_boundary == 'top':
            new_top_left_r = frame_bbox['min_r'] - 1 - obj_height
            new_top_left_c = obj_bbox['min_c']
        elif nearest_boundary == 'bottom':
            new_top_left_r = frame_bbox['max_r'] + 2
            new_top_left_c = obj_bbox['min_c']

        # --- Step 5d: Draw ---
        if new_top_left_r >= 0 and new_top_left_c >= 0: # Check if position is valid
            for rel_r, rel_c in reflected_coords_relative:
                draw_r, draw_c = new_top_left_r + rel_r, new_top_left_c + rel_c
                # Check bounds before drawing
                if 0 <= draw_r < height and 0 <= draw_c < width:
                    output_grid[draw_r, draw_c] = obj['color'] # Draw gray pixel

    return output_grid.tolist()