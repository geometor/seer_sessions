import numpy as np
from collections import deque

"""
Identifies distinct non-background rectangular objects in the input grid.
Groups these objects based on their primary color (the color of the first pixel encountered during object detection).
Within each color group, finds a unique 'pattern source' object (containing pixels of colors other than its primary color and background within its bounding box) 
and one or more 'target' objects (containing only the primary color or background within their bounding box).
Copies the entire content of the source object's bounding box onto the bounding box area of each target object, provided their dimensions match.
"""

def find_component(grid, start_r, start_c, visited):
    """
    Finds a connected component of non-background pixels using BFS.

    Args:
        grid (np.array): The input grid.
        start_r (int): Starting row index.
        start_c (int): Starting column index.
        visited (np.array): Boolean array tracking visited pixels.

    Returns:
        tuple: (min_r, min_c, max_r, max_c) bounding box of the component.
               Returns None if the start pixel is background or already visited.
    """
    rows, cols = grid.shape
    if not (0 <= start_r < rows and 0 <= start_c < cols) or visited[start_r, start_c] or grid[start_r, start_c] == 0:
        return None

    q = deque([(start_r, start_c)])
    visited[start_r, start_c] = True
    min_r, min_c = start_r, start_c
    max_r, max_c = start_r, start_c

    while q:
        r, c = q.popleft()

        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)

        # Explore neighbors (4-directional)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr, nc] and grid[nr, nc] != 0:
                visited[nr, nc] = True
                q.append((nr, nc))

    return min_r, min_c, max_r, max_c


def transform(input_grid):
    """
    Transforms the input grid by copying patterns from source objects to target objects.

    Args:
        input_grid (np.array): The 2D input grid.

    Returns:
        np.array: The transformed 2D output grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    visited = np.zeros_like(input_grid, dtype=bool)
    
    objects_data = []

    # 1. Identify all distinct non-background components and their properties
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0 and not visited[r, c]:
                primary_color = input_grid[r, c] # Use the color of the first pixel found as the primary color
                bbox = find_component(input_grid, r, c, visited)
                
                if bbox:
                    min_r, min_c, max_r, max_c = bbox
                    
                    # Determine if the object has an internal pattern within its bounding box
                    has_pattern = False
                    for rr in range(min_r, max_r + 1):
                        for cc in range(min_c, max_c + 1):
                            # Check for colors other than primary or background *within* the bounding box
                            if input_grid[rr, cc] != primary_color and input_grid[rr, cc] != 0:
                                has_pattern = True
                                break
                        if has_pattern:
                            break
                            
                    obj_info = {'bbox': bbox, 'primary_color': primary_color, 'has_pattern': has_pattern}
                    objects_data.append(obj_info)

    # 2. Group objects by primary color
    objects_by_color = {}
    for obj in objects_data:
        color = obj['primary_color']
        if color not in objects_by_color:
            objects_by_color[color] = []
        objects_by_color[color].append(obj)

    # 3. Process each color group to find source and targets, then copy patterns
    for color, object_list in objects_by_color.items():
        sources = [obj for obj in object_list if obj['has_pattern']]
        targets = [obj for obj in object_list if not obj['has_pattern']]

        # Check if there is exactly one source and at least one target
        if len(sources) == 1 and len(targets) > 0:
            src_obj = sources[0]
            min_r_src, min_c_src, max_r_src, max_c_src = src_obj['bbox']
            height_src = max_r_src - min_r_src + 1
            width_src = max_c_src - min_c_src + 1

            # Iterate through targets and copy the pattern if dimensions match
            for tgt_obj in targets:
                min_r_tgt, min_c_tgt, max_r_tgt, max_c_tgt = tgt_obj['bbox']
                height_tgt = max_r_tgt - min_r_tgt + 1
                width_tgt = max_c_tgt - min_c_tgt + 1

                if height_src == height_tgt and width_src == width_tgt:
                    # Copy the entire bounding box content from source to target
                    for dr in range(height_src):
                        for dc in range(width_src):
                            r_src_idx = min_r_src + dr
                            c_src_idx = min_c_src + dc
                            r_tgt_idx = min_r_tgt + dr
                            c_tgt_idx = min_c_tgt + dc
                            
                            # Ensure indices are within grid bounds (should be if bbox is correct)
                            if 0 <= r_tgt_idx < rows and 0 <= c_tgt_idx < cols:
                                output_grid[r_tgt_idx, c_tgt_idx] = input_grid[r_src_idx, c_src_idx]

    return output_grid