import numpy as np
from collections import deque

"""
Identifies a red rectangular frame (color 2) and internal gray content objects (color 5).
The transformation involves moving and reflecting these internal objects based on the aspect ratio of the frame's inner space.

1.  **Identify Frame & Inner Space:** Locate the bounding box of all red (2) pixels. Define the 'inner space' as the area one pixel inside this bounding box.
2.  **Determine Reflection Rule:** Calculate the height (H) and width (W) of the inner space.
    *   If W >= H (wider or square): Reflect objects horizontally.
    *   If H > W (taller): Reflect objects vertically.
3.  **Identify & Filter Internal Content:** Find all gray (5) objects (4-connectivity). Select only those strictly inside the frame's outer bounding box.
4.  **Process Each Internal Object:**
    *   Erase the object from its original position.
    *   Calculate distances from the object's bounding box to the four inner boundaries (Top, Bottom, Left, Right).
    *   **If Horizontal Reflection:**
        *   Choose placement side: Left if distance to Left inner boundary <= distance to Right; otherwise Right.
        *   Reflect the object horizontally.
        *   Place the reflected object outside the frame, adjacent to the chosen side (Left/Right) with a 1-pixel gap, aligned vertically with its original position.
    *   **If Vertical Reflection:**
        *   Choose placement side: Top if distance to Top inner boundary <= distance to Bottom; otherwise Bottom.
        *   Reflect the object vertically.
        *   Place the reflected object outside the frame, adjacent to the chosen side (Top/Bottom) with a 1-pixel gap, aligned horizontally with its original position.
5.  Objects outside the frame and the frame itself remain unchanged.
"""

def find_objects(grid, color, connectivity=4):
    """
    Finds all connected objects of a given color using Breadth-First Search (BFS).

    Args:
        grid (np.ndarray): The input grid.
        color (int): The color of the objects to find.
        connectivity (int): 4 or 8 for neighbor connectivity.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'coords' (list of (r, c) tuples) and
              'bbox' (dictionary with min_r, max_r, min_c, max_c).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    if connectivity == 4:
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    else: # Assume 8-connectivity
        neighbors = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]

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

                    for dr, dc in neighbors:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if obj_coords: # Only add if we found coordinates
                    objects.append({
                        'coords': obj_coords,
                        'bbox': {'min_r': min_r, 'max_r': max_r, 'min_c': min_c, 'max_c': max_c},
                        'color': color
                    })
    return objects

def get_frame_bbox(grid, frame_color=2):
    """
    Determines the bounding box of the frame structure.
    Assumes the frame is formed by the extent of all pixels of frame_color.
    """
    coords = np.argwhere(grid == frame_color)
    if coords.size == 0:
        return None
    min_r = np.min(coords[:, 0])
    max_r = np.max(coords[:, 0])
    min_c = np.min(coords[:, 1])
    max_c = np.max(coords[:, 1])
    return {'min_r': min_r, 'max_r': max_r, 'min_c': min_c, 'max_c': max_c}

def transform(input_grid):
    """Applies the reflection transformation based on frame inner aspect ratio."""
    
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    height, width = output_grid.shape
    frame_color = 2
    content_color = 5
    background_color = 0

    # --- Step 1: Identify the Frame ---
    frame_bbox = get_frame_bbox(input_grid_np, frame_color)
    if frame_bbox is None:
        # No frame found, return original grid
        return input_grid 

    # --- Step 2: Define Inner Space ---
    inner_min_r = frame_bbox['min_r'] + 1
    inner_max_r = frame_bbox['max_r'] - 1
    inner_min_c = frame_bbox['min_c'] + 1
    inner_max_c = frame_bbox['max_c'] - 1

    # Check if inner space is valid (frame must be at least 3x3)
    if inner_min_r > inner_max_r or inner_min_c > inner_max_c:
         # Frame too small for an inner space, treat as no transform needed? Or return original.
         return input_grid

    # --- Step 3: Determine Reflection Rule ---
    inner_height = inner_max_r - inner_min_r + 1
    inner_width = inner_max_c - inner_min_c + 1
    
    reflect_horizontally = (inner_width >= inner_height) # Reflect horizontally if wider or square

    # --- Step 4: Identify Content Objects ---
    content_objects = find_objects(input_grid_np, content_color, connectivity=4)

    # --- Step 5: Filter Internal Objects ---
    internal_objects = []
    for obj in content_objects:
        is_internal = True
        if not obj['coords']: 
             is_internal = False
        else:
            for r, c in obj['coords']:
                # Check if strictly inside the frame's outer bounding box
                if not (frame_bbox['min_r'] < r < frame_bbox['max_r'] and
                        frame_bbox['min_c'] < c < frame_bbox['max_c']):
                    is_internal = False
                    break
        if is_internal:
            internal_objects.append(obj)

    # --- Step 6 & 7: Process Each Internal Object ---
    for obj in internal_objects:
        coords = obj['coords']
        obj_bbox = obj['bbox']
        obj_height = obj_bbox['max_r'] - obj_bbox['min_r'] + 1
        obj_width = obj_bbox['max_c'] - obj_bbox['min_c'] + 1

        # --- Step 7a: Erase Original ---
        for r, c in coords:
            output_grid[r, c] = background_color

        # --- Step 7b: Calculate Distances to Inner Boundaries ---
        dist_T = max(0, obj_bbox['min_r'] - inner_min_r)
        dist_B = max(0, inner_max_r - obj_bbox['max_r'])
        dist_L = max(0, obj_bbox['min_c'] - inner_min_c)
        dist_R = max(0, inner_max_c - obj_bbox['max_c'])

        # --- Create object subgrid ---
        obj_grid = np.zeros((obj_height, obj_width), dtype=int)
        for r, c in coords:
            rel_r = r - obj_bbox['min_r']
            rel_c = c - obj_bbox['min_c']
            if 0 <= rel_r < obj_height and 0 <= rel_c < obj_width:
                 obj_grid[rel_r, rel_c] = content_color
        
        # --- Step 7c: Apply Reflection and Determine Placement ---
        reflected_obj_grid = None
        new_top_left_r, new_top_left_c = -1, -1
        
        if reflect_horizontally:
            # Reflect horizontally
            reflected_obj_grid = np.fliplr(obj_grid)
            # Determine placement: Left or Right
            if dist_L <= dist_R: # Place Left (tie goes to Left)
                placement_side = 'left'
                new_top_left_r = obj_bbox['min_r'] # Align vertically
                new_top_left_c = frame_bbox['min_c'] - 1 - obj_width # Place left of frame with 1 gap
            else: # Place Right
                placement_side = 'right'
                new_top_left_r = obj_bbox['min_r'] # Align vertically
                new_top_left_c = frame_bbox['max_c'] + 2 # Place right of frame with 1 gap
        else: # Reflect Vertically (H > W)
            # Reflect vertically
            reflected_obj_grid = np.flipud(obj_grid)
            # Determine placement: Top or Bottom
            if dist_T <= dist_B: # Place Top (tie goes to Top)
                placement_side = 'top'
                new_top_left_r = frame_bbox['min_r'] - 1 - obj_height # Place above frame with 1 gap
                new_top_left_c = obj_bbox['min_c'] # Align horizontally
            else: # Place Bottom
                placement_side = 'bottom'
                new_top_left_r = frame_bbox['max_r'] + 2 # Place below frame with 1 gap
                new_top_left_c = obj_bbox['min_c'] # Align horizontally

        # --- Step 7d: Draw Moved Object ---
        if reflected_obj_grid is not None and new_top_left_r != -1:
            reflected_height, reflected_width = reflected_obj_grid.shape
            for r_rel in range(reflected_height):
                for c_rel in range(reflected_width):
                    if reflected_obj_grid[r_rel, c_rel] == content_color:
                        draw_r = new_top_left_r + r_rel
                        draw_c = new_top_left_c + c_rel
                        # Check bounds before drawing
                        if 0 <= draw_r < height and 0 <= draw_c < width:
                            # Avoid overwriting the frame itself 
                            if output_grid[draw_r, draw_c] != frame_color:
                                 output_grid[draw_r, draw_c] = content_color
                            # else: (optional) handle potential collision with frame - current logic just skips draw
                                
    # --- Step 8: Return Result ---
    return output_grid.tolist()