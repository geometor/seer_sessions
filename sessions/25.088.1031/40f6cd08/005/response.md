```python
import numpy as np
from collections import deque

"""
Identifies distinct non-background connected components (objects) in the input grid.
Determines the 'primary color' for each object (color of the first pixel found).
Classifies objects into 'sources' (contain pixels different from primary color) and 'targets' (contain only primary color pixels).
Groups objects by primary color.
For groups with exactly one source and one or more targets:
  Iterates through the pixels within the source object's bounding box.
  If a pixel in the source belongs to the source component and its color is NOT the primary color (i.e., it's part of the internal pattern):
    Copies this pixel's color to the corresponding relative position within each target object's bounding box in the output grid.
The output grid starts as a copy of the input grid and is modified only where internal pattern pixels are copied into targets.
"""

def find_component(grid, start_r, start_c, visited):
    """
    Finds a connected component of non-background pixels using BFS,
    starting from (start_r, start_c). Determines the component's
    bounding box, the set of pixels belonging to it, and its primary color.

    Args:
        grid (np.array): The input grid.
        start_r (int): Starting row index.
        start_c (int): Starting column index.
        visited (np.array): Boolean array tracking visited pixels.

    Returns:
        tuple: (bbox, component_pixels, primary_color)
               bbox: (min_r, min_c, max_r, max_c) bounding box.
               component_pixels: set of (r, c) tuples for pixels in the component.
               primary_color: The color of the starting pixel (start_r, start_c).
               Returns (None, None, None) if the start pixel is background or already visited.
    """
    rows, cols = grid.shape
    # Check if the starting point is valid
    if not (0 <= start_r < rows and 0 <= start_c < cols) or visited[start_r, start_c] or grid[start_r, start_c] == 0:
        return None, None, None

    # Initialize BFS queue and component properties
    q = deque([(start_r, start_c)])
    visited[start_r, start_c] = True
    component_pixels = set([(start_r, start_c)])
    min_r, min_c = start_r, start_c
    max_r, max_c = start_r, start_c
    primary_color = grid[start_r, start_c] # Use starting pixel's color as primary

    # Perform BFS
    while q:
        r, c = q.popleft()

        # Update bounding box
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)

        # Explore neighbors (4-directional: up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check if neighbor is within grid, not visited, and not background
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr, nc] and grid[nr, nc] != 0:
                 # Check if the neighbor has the *same* color for component definition
                 # Updated based on refined understanding: component is connected non-background, not necessarily same-color
                 #if grid[nr, nc] == primary_color: # Original constraint - might be too strict for multi-color objects
                 # Relaxing constraint: any non-background neighbour belongs to the component
                 visited[nr, nc] = True
                 q.append((nr, nc))
                 component_pixels.add((nr, nc))


    bbox = (min_r, min_c, max_r, max_c)
    return bbox, component_pixels, primary_color


def transform(input_grid):
    # 1. Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    visited = np.zeros_like(input_grid, dtype=bool)
    objects_data = []

    # 2. Identify all distinct connected components (objects)
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0 and not visited[r, c]:
                # 3. Determine primary color, bounding box, and pixel set for each object.
                bbox, component_pixels, primary_color = find_component(input_grid, r, c, visited)
                
                if bbox:
                    # 4. Classify each object as source or target.
                    is_source = False
                    for rr, cc in component_pixels:
                        if input_grid[rr, cc] != primary_color:
                            is_source = True
                            break
                            
                    obj_info = {
                        'bbox': bbox, 
                        'pixels': component_pixels, 
                        'primary_color': primary_color, 
                        'is_source': is_source # True if source, False if target
                    }
                    objects_data.append(obj_info)

    # 5. Group objects by primary color.
    objects_by_color = {}
    for obj in objects_data:
        color = obj['primary_color']
        if color not in objects_by_color:
            objects_by_color[color] = []
        objects_by_color[color].append(obj)

    # 6. Iterate through each color group.
    for color, object_list in objects_by_color.items():
        sources = [obj for obj in object_list if obj['is_source']]
        targets = [obj for obj in object_list if not obj['is_source']]

        # 7. If a group has exactly one source and >= 1 target:
        if len(sources) == 1 and len(targets) > 0:
            src_obj = sources[0]
            P = src_obj['primary_color'] # Primary color of the group
            min_r_src, min_c_src, max_r_src, max_c_src = src_obj['bbox']
            src_pixels = src_obj['pixels']
            height_src = max_r_src - min_r_src + 1
            width_src = max_c_src - min_c_src + 1

            # 7a. For each target object T in the group:
            for tgt_obj in targets:
                min_r_tgt, min_c_tgt, _, _ = tgt_obj['bbox'] 

                # 7b. Iterate through relative coordinates within the source bounding box.
                for dr in range(height_src):
                    for dc in range(width_src):
                        # 7c. Calculate absolute source coordinates.
                        sr = min_r_src + dr
                        sc = min_c_src + dc

                        # 7d. Calculate absolute target coordinates.
                        tr = min_r_tgt + dr
                        tc = min_c_tgt + dc
                        
                        # 7e. Check if source pixel is part of the component AND is internal pattern.
                        # Make sure the source coordinate is actually part of the *component* pixels,
                        # not just within the bounding box but outside the actual shape.
                        if (sr, sc) in src_pixels and input_grid[sr, sc] != P:
                             # 7f. If it's internal pattern AND target coords are valid, copy to output.
                             if 0 <= tr < rows and 0 <= tc < cols:
                                 output_grid[tr, tc] = input_grid[sr, sc]

    # 8. Return the modified output grid.
    return output_grid
```