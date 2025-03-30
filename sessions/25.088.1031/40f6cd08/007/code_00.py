import numpy as np
from collections import deque

"""
Identifies distinct non-background connected components (objects) in the input grid.
Determines the 'primary color' for each object (color of its top-leftmost pixel).
Classifies objects into 'sources' (contain pixels different from primary color) and 'targets' (contain only primary color pixels).
Groups objects by primary color.
For groups with exactly one source and one or more targets:
  Iterates through the pixels within the source object.
  If a pixel in the source belongs to the source component and its color is NOT the primary color (i.e., it's part of the internal pattern):
    Calculates its relative position within the source's bounding box.
    Determines the corresponding absolute position within each target object's bounding box.
    Crucially, checks if this target position actually belongs to the target object's pixel set.
    If it does, copies the source pattern pixel's color to that target pixel location in the output grid.
The output grid starts as a copy of the input grid and is modified only where internal pattern pixels are copied onto valid target pixels.
"""

def find_component_bfs(grid, start_r, start_c, visited):
    """
    Finds a connected component of non-background pixels using BFS,
    starting from (start_r, start_c). Determines the component's
    bounding box and the set of pixels belonging to it.

    Args:
        grid (np.array): The input grid.
        start_r (int): Starting row index.
        start_c (int): Starting column index.
        visited (np.array): Boolean array tracking visited pixels.

    Returns:
        tuple: (component_pixels, bbox)
               component_pixels: set of (r, c) tuples for pixels in the component.
               bbox: (min_r, min_c, max_r, max_c) bounding box.
               Returns (None, None) if the start pixel is background or already visited.
    """
    rows, cols = grid.shape
    # Check if the starting point is valid (within bounds, not background, not visited)
    if not (0 <= start_r < rows and 0 <= start_c < cols) or visited[start_r, start_c] or grid[start_r, start_c] == 0:
        return None, None

    # Initialize BFS queue and component properties
    q = deque([(start_r, start_c)])
    visited[start_r, start_c] = True
    component_pixels = set([(start_r, start_c)])
    min_r, min_c = start_r, start_c
    max_r, max_c = start_r, start_c

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
                 visited[nr, nc] = True
                 q.append((nr, nc))
                 component_pixels.add((nr, nc))

    bbox = (min_r, min_c, max_r, max_c)
    return component_pixels, bbox

def get_top_left_pixel(pixel_set):
    """Finds the top-leftmost pixel in a set of (row, col) tuples."""
    if not pixel_set:
        return None
    min_r = min(r for r, c in pixel_set)
    min_c = min(c for r, c in pixel_set if r == min_r)
    return (min_r, min_c)

def transform(input_grid):
    """
    Applies the source-target pattern copy transformation.
    """
    # 1. Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    visited = np.zeros_like(input_grid, dtype=bool)
    objects_data = []

    # 2. Find all distinct objects (connected components)
    for r in range(rows):
        for c in range(cols):
            # If pixel is non-background and not yet visited (part of a found component)
            if input_grid[r, c] != 0 and not visited[r, c]:
                # 3a. Find the component pixels and bounding box using BFS
                component_pixels, bbox = find_component_bfs(input_grid, r, c, visited)

                if component_pixels:
                    # 3b. Determine the primary color from the top-left pixel of the component
                    tl_pixel = get_top_left_pixel(component_pixels)
                    primary_color = input_grid[tl_pixel]

                    # 3c. Classify as source or target
                    is_source = False
                    for rr, cc in component_pixels:
                        if input_grid[rr, cc] != primary_color:
                            is_source = True
                            break

                    # Store object info
                    obj_info = {
                        'bbox': bbox,
                        'pixels': component_pixels,
                        'primary_color': primary_color,
                        'is_source': is_source # True if source, False if target
                    }
                    objects_data.append(obj_info)

    # 4. Group objects by primary color.
    objects_by_color = {}
    for obj in objects_data:
        color = obj['primary_color']
        if color not in objects_by_color:
            objects_by_color[color] = []
        objects_by_color[color].append(obj)

    # 5. Iterate through each color group.
    for color, object_list in objects_by_color.items():
        sources = [obj for obj in object_list if obj['is_source']]
        targets = [obj for obj in object_list if not obj['is_source']]

        # 6. If a group has exactly one source and >= 1 target:
        if len(sources) == 1 and len(targets) > 0:
            src_obj = sources[0]
            P = src_obj['primary_color'] # Primary color of the group
            min_r_src, min_c_src, _, _ = src_obj['bbox']
            src_pixels = src_obj['pixels'] # Set of (r, c) tuples for the source

            # 6a. For each target object T in the group:
            for tgt_obj in targets:
                min_r_tgt, min_c_tgt, _, _ = tgt_obj['bbox']
                target_pixels = tgt_obj['pixels'] # Set of (r, c) tuples for the target

                # 6b. Iterate through each pixel *belonging to the source object*.
                for sr, sc in src_pixels:
                    src_color = input_grid[sr, sc]

                    # 6c. If the source pixel is part of the internal pattern (not primary color):
                    if src_color != P:
                        # 6d. Calculate relative coordinates within the source bounding box.
                        dr = sr - min_r_src
                        dc = sc - min_c_src

                        # 6e. Calculate corresponding absolute target coordinates.
                        tr = min_r_tgt + dr
                        tc = min_c_tgt + dc

                        # 6f. **Crucial Check**: Ensure the target coordinate is valid *and* part of the target object's shape.
                        if (tr, tc) in target_pixels:
                             # 6g. Copy the pattern color to the output grid at the valid target location.
                             output_grid[tr, tc] = src_color

    # 7. Return the modified output grid.
    return output_grid