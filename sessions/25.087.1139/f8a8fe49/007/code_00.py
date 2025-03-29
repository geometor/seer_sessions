import numpy as np
from collections import deque

"""
Identifies a red rectangular frame (color 2) and internal gray content objects (color 5).
The transformation involves moving and reflecting these internal objects based on the aspect ratio of the frame's inner space.

1.  **Identify Frame & Inner Space:** Locate the bounding box of all red (2) pixels. Define the 'inner space' as the area one pixel inside this bounding box. If no frame exists or the inner space is invalid, return the original grid.
2.  **Determine Reflection Rule:** Calculate the height (H) and width (W) of the inner space.
    *   If W >= H (wider or square): Reflection axis is vertical (objects reflect horizontally). Placement will be Left/Right.
    *   If H > W (taller): Reflection axis is horizontal (objects reflect vertically). Placement will be Top/Bottom.
3.  **Identify & Filter Internal Content:** Find all gray (5) objects (4-connectivity). Select only those strictly inside the frame's outer bounding box.
4.  **Process Each Internal Object:**
    *   Calculate the object's center relative to the inner space's center.
    *   Erase the object from its original position within the output grid.
    *   Create a subgrid containing just the object.
    *   **If Horizontal Reflection (W >= H):**
        *   Reflect the object subgrid horizontally (np.fliplr).
        *   Determine placement side based on the object's horizontal position relative to the inner space center:
            *   If object center is left of or at the inner center column: Place Left.
            *   If object center is right of the inner center column: Place Right.
        *   Calculate the top-left corner for the reflected object:
            *   Left Placement: Column = frame_min_c - 1 - object_width. Row = object_min_r.
            *   Right Placement: Column = frame_max_c + 2. Row = object_min_r.
    *   **If Vertical Reflection (H > W):**
        *   Reflect the object subgrid vertically (np.flipud).
        *   Determine placement side based on the object's vertical position relative to the inner space center:
            *   If object center is above or at the inner center row: Place Top.
            *   If object center is below the inner center row: Place Bottom.
        *   Calculate the top-left corner for the reflected object:
            *   Top Placement: Row = frame_min_r - 1 - object_height. Column = object_min_c.
            *   Bottom Placement: Row = frame_max_r + 2. Column = object_min_c.
    *   Draw the reflected object onto the output grid at the calculated position, ensuring it doesn't overwrite the frame and stays within grid bounds.
5.  Objects outside the frame and the frame itself remain unchanged in the output grid.
"""

import numpy as np
from collections import deque

def find_objects(grid, color, connectivity=4):
    """
    Finds all connected objects of a given color using Breadth-First Search (BFS).

    Args:
        grid (np.ndarray): The input grid.
        color (int): The color of the objects to find.
        connectivity (int): 4 or 8 for neighbor connectivity.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'coords' (list of (r, c) tuples),
              'bbox' (dictionary with min_r, max_r, min_c, max_c), and 'color'.
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
    Returns None if no frame pixels are found.
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
    """
    Applies the reflection transformation based on frame inner aspect ratio.
    """
    
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
        return input_grid # Return original list grid

    # --- Step 2: Define Inner Space ---
    inner_min_r = frame_bbox['min_r'] + 1
    inner_max_r = frame_bbox['max_r'] - 1
    inner_min_c = frame_bbox['min_c'] + 1
    inner_max_c = frame_bbox['max_c'] - 1

    # Check if inner space is valid (frame must be at least 3x3)
    if inner_min_r > inner_max_r or inner_min_c > inner_max_c:
         # Frame too small for an inner space, return original grid.
         return input_grid # Return original list grid

    # --- Step 3: Determine Reflection Rule ---
    inner_height = inner_max_r - inner_min_r + 1
    inner_width = inner_max_c - inner_min_c + 1
    
    # Reflect horizontally if wider or square (placement Left/Right)
    reflect_horizontally = (inner_width >= inner_height) 
    inner_center_c = (inner_min_c + inner_max_c) / 2.0
    inner_center_r = (inner_min_r + inner_max_r) / 2.0

    # --- Step 4: Identify Content Objects ---
    content_objects = find_objects(input_grid_np, content_color, connectivity=4)

    # --- Step 5: Filter Internal Objects ---
    internal_objects = []
    for obj in content_objects:
        is_internal = True
        if not obj['coords']: 
             is_internal = False
        else:
            # Check if all coordinates are strictly inside the frame's outer box
            for r, c in obj['coords']:
                if not (frame_bbox['min_r'] < r < frame_bbox['max_r'] and
                        frame_bbox['min_c'] < c < frame_bbox['max_c']):
                    is_internal = False
                    break
        if is_internal:
            internal_objects.append(obj)

    # --- Step 6: Process Each Internal Object ---
    for obj in internal_objects:
        coords = obj['coords']
        obj_bbox = obj['bbox']
        obj_height = obj_bbox['max_r'] - obj_bbox['min_r'] + 1
        obj_width = obj_bbox['max_c'] - obj_bbox['min_c'] + 1
        
        # Calculate object center
        obj_center_c = (obj_bbox['min_c'] + obj_bbox['max_c']) / 2.0
        obj_center_r = (obj_bbox['min_r'] + obj_bbox['max_r']) / 2.0

        # --- Step 6a: Erase Original ---
        for r, c in coords:
            output_grid[r, c] = background_color

        # --- Step 6b: Create object subgrid ---
        obj_grid = np.zeros((obj_height, obj_width), dtype=int)
        for r, c in coords:
            rel_r = r - obj_bbox['min_r']
            rel_c = c - obj_bbox['min_c']
            # Ensure relative coordinates are within the subgrid bounds
            if 0 <= rel_r < obj_height and 0 <= rel_c < obj_width:
                 obj_grid[rel_r, rel_c] = content_color
        
        # --- Step 6c: Apply Reflection and Determine Placement ---
        reflected_obj_grid = None
        new_top_left_r, new_top_left_c = -1, -1
        
        if reflect_horizontally: # Reflect horizontally, place Left/Right
            reflected_obj_grid = np.fliplr(obj_grid)
            # Determine placement based on object center vs inner center column
            if obj_center_c <= inner_center_c: # Place Left (tie goes to Left)
                new_top_left_r = obj_bbox['min_r'] # Align vertically
                new_top_left_c = frame_bbox['min_c'] - 1 - obj_width # Place left of frame with 1 gap
            else: # Place Right
                new_top_left_r = obj_bbox['min_r'] # Align vertically
                new_top_left_c = frame_bbox['max_c'] + 2 # Place right of frame with 1 gap
        
        else: # Reflect Vertically (H > W), place Top/Bottom
            reflected_obj_grid = np.flipud(obj_grid)
            # Determine placement based on object center vs inner center row
            if obj_center_r <= inner_center_r: # Place Top (tie goes to Top)
                new_top_left_r = frame_bbox['min_r'] - 1 - obj_height # Place above frame with 1 gap
                new_top_left_c = obj_bbox['min_c'] # Align horizontally
            else: # Place Bottom
                new_top_left_r = frame_bbox['max_r'] + 2 # Place below frame with 1 gap
                new_top_left_c = obj_bbox['min_c'] # Align horizontally

        # --- Step 6d: Draw Moved Object ---
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
                            # (Check the *original* grid value at the target location 
                            # to allow drawing over erased areas, but not the frame)
                            if input_grid_np[draw_r, draw_c] != frame_color:
                                 output_grid[draw_r, draw_c] = content_color
                            # else: Skip drawing if it would overwrite the frame
                                
    # --- Step 7: Return Result ---
    # Convert back to list of lists for the expected output format
    return output_grid.tolist()