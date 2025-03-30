
Previous Code:
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
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 4 4 4 4 4 4 4 4 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 4 4 4 4 4 4 4 4 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 1 1 1 1 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 1 1 1 1 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 4 4 4 4 4 4 4 4 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 4 4 4 4 4 4 4 4 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 1 1 1 1 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 1 1 1 1 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 4 4 4 4 4 4 4 4 4 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 4 4 4 4 4 4 4 4 4 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 1 1 1 1 1 1 1 4 4 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 1 1 1 1 1 1 1 4 4 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 1 1 8 8 8 1 1 4 4 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 1 1 8 8 8 1 1 4 4 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 1 1 8 8 8 1 1 4 4 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 4 4 4 4 4 4 4 4 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 4 4 4 4 4 4 4 4 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 1 1 1 1 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 1 1 1 1 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 4 4 4 4 4 4 4 4 4 4 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 4 4 4 4 4 4 4 4 4 4 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 1 1 1 1 1 1 1 1 4 4 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 1 1 1 1 1 1 1 1 4 4 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 1 1 8 8 8 8 1 1 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 1 1 8 8 8 8 1 1 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 39
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 9.629629629629619

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 6 6 6 6 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 6 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 6 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 6 6 6 6 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 6 6 6 6 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 6 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 6 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 6 6 6 6 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 6 6 6 6 6 6 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 6 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 6 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6 6 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 6 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 6 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6 6 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 6 6 6 6 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 6 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 6 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 6 6 6 6 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 6 6 6 6 6 6 6 6 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 6 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 6 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 6 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 6 6 6 6 6 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 8 8 8 8 6 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 8 8 8 8 6 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 6 6 6 6 6 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 43
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 9.555555555555571

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 4 4 4 4 4 4 4 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 4 2 2 2 2 2 4 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 4 2 2 2 2 2 4 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 4 2 2 2 2 2 4 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 4 4 4 4 4 4 4 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 4 4 4 4 4 4 4 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 4 2 2 2 2 2 4 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 4 2 2 2 2 2 4 8 8 0 0 0 0 8 8 4 4 4 4 4 4 8 8 0
0 0 0 0 8 8 4 2 2 2 2 2 4 8 8 0 0 0 0 8 8 4 2 2 2 2 4 8 8 0
0 0 0 0 8 8 4 4 4 4 4 4 4 8 8 0 0 0 0 8 8 4 4 4 4 4 4 8 8 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 4 4 4 4 4 4 4 4 4 4 4 4 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 4 2 2 2 2 2 2 2 2 2 2 4 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 4 2 2 2 2 2 2 2 2 2 2 4 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 4 2 2 2 2 2 2 2 2 2 2 4 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 4 2 2 2 2 2 2 2 2 2 2 4 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 4 2 2 2 2 2 2 2 2 2 2 4 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 4 4 4 4 4 4 4 4 4 4 4 4 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 4 4 4 4 4 4 4 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 4 2 2 2 2 2 4 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 4 2 2 2 2 2 4 8 8 0 0 0 0 8 8 4 4 4 4 4 4 4 8 0
0 0 0 0 8 8 4 2 2 2 2 2 4 8 8 0 0 0 0 8 8 4 2 2 2 2 2 4 8 0
0 0 0 0 8 8 4 4 4 4 4 4 4 8 8 0 0 0 0 8 8 4 2 2 2 2 2 4 8 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 4 2 2 2 2 2 4 8 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 4 4 4 4 4 4 4 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 4 4 4 4 4 4 4 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 4 2 2 2 2 2 4 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 4 2 2 2 2 2 4 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 4 2 2 2 2 2 4 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 4 4 4 4 4 4 4 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 81
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 18.0
## General Assessment

The previous code correctly identifies the core concept of the task: locating objects based on a primary color, distinguishing a 'source' object (containing an internal pattern of different colors) from 'target' objects (monochromatic), and copying the internal pattern from the source to the targets.

However, the implementation fails across all examples, indicated by the `Match: False` results and significant `Pixels Off` counts. The generated outputs show partial or incorrectly placed patterns within the target objects.

The key issue appears to be in the pattern copying step (step 7f in the previous code's logic). The code copies a pattern pixel from the source to the corresponding relative position in the target's bounding box, but it only checks if the target coordinates are within the overall grid boundaries. It does *not* verify if the target coordinates `(tr, tc)` actually correspond to a pixel that was part of the original target object's shape (`tgt_obj['pixels']`). This likely leads to the pattern being drawn over background pixels or missing parts of the target shape if the source and target shapes/bounding boxes differ significantly in size or alignment within their boxes.

The strategy is to refine the pattern copying logic to ensure that pattern pixels are *only* written to coordinates that originally belonged to the target object.

## Metrics and Detailed Analysis

Let's analyze each example to confirm the hypothesis. We need to understand the objects, their properties, and how the pattern transfer should occur versus how the previous code performed it.

**Example 1:**
*   **Input Objects:**
    *   Source: Green (3) object at top-left (bbox approx [2:13, 3:18]), contains Yellow (4), Blue (1), Azure (8) pattern.
    *   Target: Green (3) object at bottom-right (bbox approx [15:24, 14:29]), solid green.
*   **Expected Transformation:** The Yellow/Blue/Azure pattern from the source is copied onto the target object, replacing the green pixels at corresponding relative positions within the target's shape.
*   **Previous Code Output:** The pattern is partially copied. Notably, the bottom rows and rightmost columns of the expected pattern within the target object are missing or incorrect (still green). This aligns with the hypothesis that the code overwrites based on source bounding box dimensions without constraining writes to the target object's actual pixel set. The target object is slightly smaller/differently shaped within its bounding box compared to the source.
*   **Metrics Check:**
    *   Source BBox: (2, 3, 12, 17) -> H=11, W=15
    *   Target BBox: (15, 14, 23, 28) -> H=9, W=15
    *   The code iterates using source dimensions (H=11, W=15). When calculating target coordinates `tr = min_r_tgt + dr`, `tc = min_c_tgt + dc`, if `dr` or `dc` are large, `(tr, tc)` might fall outside the actual target shape, even if within grid bounds. The fix is to check if `(tr, tc)` is in `tgt_obj['pixels']`.

**Example 2:**
*   **Input Objects:**
    *   Source: Red (2) object at top-left (bbox approx [2:12, 3:13]), contains Magenta (6), Azure (8) pattern.
    *   Targets: Three Red (2) objects: adjacent right (bbox approx [8:17, 19:29]), bottom-middle (bbox approx [19:29, 5:21]), and one inside the source's bounding box area but separate component ([5:9, 3:11] contains the pattern, the rest [2:5, 3:13], [9:12, 3:13] etc are just red). The component finding needs to be robust. The previous `find_component` used the *start pixel* color as the primary color, which might fail if the BFS starts on a pattern pixel. Let's assume the primary color is defined more robustly (e.g., most frequent non-background color in the component). Let's redefine Source/Target based on visual inspection:
        *   Source (Pattern Holder): Red (2) object containing Magenta(6)/Azure(8) pattern. BBox approx (2, 3) to (11, 12). Primary color Red.
        *   Target 1: Red (2) object, solid. BBox approx (8, 19) to (16, 28).
        *   Target 2: Red (2) object, solid. BBox approx (19, 5) to (28, 20).
*   **Expected Transformation:** The Magenta/Azure pattern from the source is copied onto *both* solid red target objects.
*   **Previous Code Output:** Patterns are copied incorrectly/partially onto both targets. Errors are consistent with writing based on source dimensions without checking target pixel membership.
*   **Metrics Check:** The different sizes and shapes of the targets relative to the source reinforce the need to check `(tr, tc)` against `tgt_obj['pixels']`.

**Example 3:**
*   **Input Objects:**
    *   Source: Azure (8) object at top-left (bbox approx [3:12, 4:15]), contains Yellow (4), Red (2) pattern.
    *   Target 1: Azure (8) object adjacent right (bbox approx [5:12, 19:29]), solid Azure.
    *   Target 2: Azure (8) object at bottom (bbox approx [17:28, 3:19]), solid Azure.
*   **Expected Transformation:** The Yellow/Red pattern from the source is copied onto both solid Azure target objects.
*   **Previous Code Output:** Patterns are copied incorrectly/partially onto both targets. The errors are again consistent with the identified flaw.
*   **Metrics Check:** Similar issues apply. Source/Target shapes and sizes differ, requiring the target pixel check.

## YAML Facts


```yaml
task_description: Copy the internal color pattern from a 'source' object onto one or more 'target' objects that share the same primary color.

definitions:
  background_color: 0 (white)
  object: A connected component of non-background pixels. Connectivity is 4-directional (up, down, left, right).
  primary_color: The dominant color of an object's border or main body. For this task, it appears to be the color of the pixels forming the outer layer or the majority color if ambiguous. Alternatively, using the color of the top-left-most pixel of the object component works if the component finding correctly identifies all pixels.
  internal_pattern: Pixels within an object that have a color different from its primary color.
  source_object: An object that contains an internal pattern.
  target_object: An object that consists solely of its primary color (no internal pattern).

rules:
  - Identify all distinct objects (connected components of non-background pixels) in the input grid.
  - For each object:
      - Determine its set of pixels.
      - Determine its bounding box.
      - Determine its primary color (e.g., color of the top-left-most pixel of the component).
      - Classify it as 'source' (contains pixels != primary color) or 'target' (all pixels == primary color).
  - Group objects by their primary color.
  - For each group that contains exactly one source object and one or more target objects:
      - Let S be the source object and P be its primary color.
      - Let (min_r_src, min_c_src) be the top-left coordinates of S's bounding box.
      - For each target object T in the group:
          - Let (min_r_tgt, min_c_tgt) be the top-left coordinates of T's bounding box.
          - Let target_pixels be the set of (row, col) coordinates belonging to T.
          - Iterate through each pixel (sr, sc) within the source object S:
              - If the color of (sr, sc) in the input grid is *not* equal to the primary color P (i.e., it's part of the internal pattern):
                  - Calculate the relative coordinates: dr = sr - min_r_src, dc = sc - min_c_src.
                  - Calculate the corresponding potential target coordinates: tr = min_r_tgt + dr, tc = min_c_tgt + dc.
                  - Check if the coordinates (tr, tc) are within the grid boundaries AND if (tr, tc) is in the set target_pixels.
                  - If both conditions are true, update the output grid at (tr, tc) with the color of the source pixel (sr, sc).
  - The initial output grid is a copy of the input grid. Updates only happen where pattern pixels are copied onto valid target pixels.

```


## Natural Language Program

1.  Start with an output grid that is an identical copy of the input grid.
2.  Find all separate objects in the input grid. An object is a group of connected non-background pixels (use 4-way adjacency).
3.  For each object found:
    a.  Record all the pixel coordinates `(r, c)` that make up the object.
    b.  Find the object's bounding box (minimum and maximum row and column).
    c.  Determine the object's "primary color". This is the color of the pixel at the top-most, then left-most coordinate within the object.
    d.  Check if the object contains any pixels whose color is different from its primary color. If yes, classify it as a "source" object. If no (all pixels have the primary color), classify it as a "target" object.
4.  Group the identified objects based on their primary color.
5.  Examine each group:
    a.  If a group contains exactly one source object and at least one target object, proceed to step 6 for this group. Otherwise, ignore the group.
6.  For a qualifying group (one source S, one or more targets T1, T2,...):
    a.  Get the primary color P of the group.
    b.  Get the top-left coordinate `(min_r_src, min_c_src)` of the source object S's bounding box.
    c.  For *each* target object T in the group:
        i.  Get the top-left coordinate `(min_r_tgt, min_c_tgt)` of T's bounding box.
        ii. Get the set of pixel coordinates `target_pixels` belonging to T.
        iii. Iterate through every pixel coordinate `(sr, sc)` that belongs to the source object S.
        iv. If the color of the input grid at `(sr, sc)` is *not* the primary color P:
            1.  Calculate the relative offset: `dr = sr - min_r_src`, `dc = sc - min_c_src`.
            2.  Calculate the corresponding coordinate in the target's frame: `tr = min_r_tgt + dr`, `tc = min_c_tgt + dc`.
            3.  Check if the calculated coordinate `(tr, tc)` exists within the `target_pixels` set.
            4.  If it does, update the `output_grid` at `(tr, tc)` to be the color of the input grid at `(sr, sc)`.
7.  Return the final `output_grid`.
