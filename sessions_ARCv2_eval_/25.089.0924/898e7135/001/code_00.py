import numpy as np
from collections import deque

"""
Transformation Rule Description:

1.  **Identify Objects:** Find all contiguous objects of non-white (0) colors in the input grid. For each object, determine its color, area (number of pixels), and bounding box.
2.  **Filter Noise:** Remove objects with an area of 1 pixel ("noise").
3.  **Find Largest Object:** Among the remaining objects, identify the one with the largest area (L). If there's a tie in area, the one encountered first (e.g., by top-left coordinate) is chosen. Note its color (C_bg) and the dimensions of its bounding box (Hl, Wl).
4.  **Identify Kept Objects:** All other non-noise objects (K_i) are designated as "kept" objects, which will be drawn onto the output grid.
5.  **Calculate Output Size:** Determine the output grid dimensions (H_out, W_out) based on the largest object's bounding box dimensions (Hl, Wl) using the following rule:
    *   H_out = max(1, 2 * Hl if Hl % 2 == 0 else 2 * (Hl - 1))
    *   W_out = max(1, 2 * Wl if Wl % 2 == 0 else 2 * (Wl - 1))
6.  **Initialize Output Grid:** Create an output grid of size (H_out, W_out) and fill it entirely with the background color C_bg.
7.  **Determine Kept Objects' Combined Bounding Box:** If there are any kept objects (K_i), calculate the minimal bounding box (KBB_all) that encloses all of them. Find its top-left corner (rk_all, ck_all). If there are no kept objects, the output grid remains as initialized.
8.  **Draw Kept Objects:** For each kept object K_i:
    *   Iterate through each pixel `(r, c)` belonging to K_i in the input grid.
    *   Calculate the pixel's position relative to the top-left corner of the combined kept objects' bounding box: `rel_r = r - rk_all`, `rel_c = c - ck_all`.
    *   Calculate the target output position by adding a fixed offset of (2, 2): `out_r = rel_r + 2`, `out_c = rel_c + 2`.
    *   If the calculated `(out_r, out_c)` coordinates are within the bounds of the output grid, set the pixel at `output_grid[out_r, out_c]` to the color of K_i.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of non-background (0) colors in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color', 'pixels' (set of (r, c) tuples),
              'area', and 'bbox' (min_r, min_c, max_r, max_c).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c
                
                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)
                    
                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'area': len(obj_pixels),
                    'bbox': (min_r, min_c, max_r, max_c)
                })
                
    # Sort objects primarily by area (descending), then by position (top-left)
    objects.sort(key=lambda o: (-o['area'], o['bbox'][0], o['bbox'][1]))
    return objects

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    
    # 1. Find all non-background objects
    all_objects = find_objects(input_grid_np)
    
    # 2. Filter out noise (area = 1)
    non_noise_objects = [obj for obj in all_objects if obj['area'] > 1]
    
    # Handle cases with no non-noise objects
    if not non_noise_objects:
        # If there are no objects or only noise, output might be empty or based on input size?
        # Based on the examples, it seems unlikely. Let's assume at least one valid object exists
        # or return a default small grid if truly empty.
        # For now, let's handle the case where *only* the largest object exists.
        # If NO objects > area 1, perhaps return a 1x1 grid of white? Or maybe just the largest object logic handles this.
         if not all_objects:
             return np.array([[0]], dtype=int) # Default for truly empty input
         else: # Only noise objects exist
            # Let's default to a 1x1 white grid if only noise was present
             return np.array([[0]], dtype=int)


    # 3. Find the largest object (first in the sorted list)
    largest_object = non_noise_objects[0]
    bg_color = largest_object['color']
    l_min_r, l_min_c, l_max_r, l_max_c = largest_object['bbox']
    l_h = l_max_r - l_min_r + 1
    l_w = l_max_c - l_min_c + 1
    
    # 4. Identify kept objects
    kept_objects = non_noise_objects[1:] # All non-noise objects except the largest

    # 5. Calculate output grid size
    h_out = max(1, 2 * l_h if l_h % 2 == 0 else 2 * (l_h - 1))
    w_out = max(1, 2 * l_w if l_w % 2 == 0 else 2 * (l_w - 1))
    
    # 6. Initialize output grid
    output_grid = np.full((h_out, w_out), bg_color, dtype=int)
    
    # If there are no kept objects, return the background grid
    if not kept_objects:
        return output_grid.tolist() # Convert back to list of lists for standard ARC format
        
    # 7. Determine Kept Objects' Combined Bounding Box
    k_min_r, k_min_c = float('inf'), float('inf')
    k_max_r, k_max_c = float('-inf'), float('-inf')
    for obj in kept_objects:
        min_r, min_c, max_r, max_c = obj['bbox']
        k_min_r = min(k_min_r, min_r)
        k_min_c = min(k_min_c, min_c)
        k_max_r = max(k_max_r, max_r)
        k_max_c = max(k_max_c, max_c)
        
    rk_all, ck_all = k_min_r, k_min_c # Top-left corner of the combined bbox

    # 8. Draw Kept Objects
    fixed_offset_r, fixed_offset_c = 2, 2
    for obj in kept_objects:
        obj_color = obj['color']
        for r, c in obj['pixels']:
            # Calculate relative position within the combined kept bbox
            rel_r = r - rk_all
            rel_c = c - ck_all
            
            # Calculate output position with fixed offset
            out_r = rel_r + fixed_offset_r
            out_c = rel_c + fixed_offset_c
            
            # Draw if within bounds
            if 0 <= out_r < h_out and 0 <= out_c < w_out:
                output_grid[out_r, out_c] = obj_color
                
    return output_grid.tolist() # Convert back to list of lists