
Previous Code:
```python
import numpy as np
from collections import deque

"""
Identifies distinct non-background connected components (objects) in the input grid.
For each object, determines its 'primary color' (color of the first pixel found during detection).
Classifies objects into 'sources' and 'targets' based on their content:
  - A 'source' object contains at least one pixel whose color is different from its primary color.
  - A 'target' object contains only pixels of its primary color.
Groups objects by their primary color.
Within each color group, if there is exactly one source object and one or more target objects:
  - Extracts the rectangular pattern defined by the bounding box of the source object from the input grid.
  - Copies this pattern onto the output grid, positioning the top-left corner of the pattern at the top-left corner of each target object's bounding box. The pattern overwrites any existing pixels in the target area.
The output grid initially mirrors the input grid and is modified by these copy operations.
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
                visited[nr, nc] = True
                q.append((nr, nc))
                component_pixels.add((nr, nc))

    bbox = (min_r, min_c, max_r, max_c)
    return bbox, component_pixels, primary_color


def transform(input_grid):
    """
    Transforms the input grid by identifying source and target objects
    and copying the source pattern onto the targets.

    Args:
        input_grid (np.array): The 2D input grid.

    Returns:
        np.array: The transformed 2D output grid.
    """
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    # Keep track of visited pixels during component finding
    visited = np.zeros_like(input_grid, dtype=bool)
    
    objects_data = []

    # 1. Find all distinct non-background components (objects)
    for r in range(rows):
        for c in range(cols):
            # If pixel is non-background and not yet visited, start BFS
            if input_grid[r, c] != 0 and not visited[r, c]:
                bbox, component_pixels, primary_color = find_component(input_grid, r, c, visited)
                
                # If a valid component was found
                if bbox:
                    # 2. Determine if the object is a 'source' or 'target'
                    is_source = False
                    # Check if any pixel *within the component* has a different color
                    for rr, cc in component_pixels:
                        # Note: component pixels are guaranteed non-zero by find_component
                        if input_grid[rr, cc] != primary_color: 
                            is_source = True
                            break
                            
                    # Store object information
                    obj_info = {
                        'bbox': bbox, 
                        'pixels': component_pixels, 
                        'primary_color': primary_color, 
                        'is_source': is_source # True if source, False if target
                    }
                    objects_data.append(obj_info)

    # 3. Group objects by their primary color
    objects_by_color = {}
    for obj in objects_data:
        color = obj['primary_color']
        if color not in objects_by_color:
            objects_by_color[color] = []
        objects_by_color[color].append(obj)

    # 4. Process each color group
    for color, object_list in objects_by_color.items():
        # Separate sources and targets within the group
        sources = [obj for obj in object_list if obj['is_source']]
        targets = [obj for obj in object_list if not obj['is_source']]

        # 5. Apply transformation if exactly one source and at least one target exists
        if len(sources) == 1 and len(targets) > 0:
            src_obj = sources[0]
            min_r_src, min_c_src, max_r_src, max_c_src = src_obj['bbox']
            
            # Extract the pattern from the source object's bounding box
            pattern = input_grid[min_r_src : max_r_src + 1, min_c_src : max_c_src + 1]
            height_src, width_src = pattern.shape

            # Iterate through each target object
            for tgt_obj in targets:
                # Get the top-left corner of the target's bounding box
                min_r_tgt, min_c_tgt, _, _ = tgt_obj['bbox'] 

                # Define the destination slice in the output grid
                end_r_tgt = min_r_tgt + height_src
                end_c_tgt = min_c_tgt + width_src
                
                # Determine the actual portion of the pattern that fits within the grid boundaries
                effective_height = min(height_src, rows - min_r_tgt)
                effective_width = min(width_src, cols - min_c_tgt)

                # Copy the (potentially clipped) pattern if it has positive dimensions
                if effective_height > 0 and effective_width > 0:
                     # Slice the pattern to match the effective dimensions
                     pattern_slice = pattern[0:effective_height, 0:effective_width]
                     # Place the pattern slice onto the output grid, overwriting existing content
                     output_grid[min_r_tgt : min_r_tgt + effective_height, min_c_tgt : min_c_tgt + effective_width] = pattern_slice

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
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 4 4 4 4 4 4 4 4 4 4 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 4 4 4 4 4 4 4 4 4 4 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 1 1 1 1 1 1 1 1 4 4 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 1 1 1 1 1 1 1 1 4 4 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 56
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 13.827160493827137

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
0 0 0 6 6 6 6 6 6 6 6 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 6 6 6 6 6 6 6 6 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 6 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 6 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 6 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2
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
Pixels Off: 72
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 16.0

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
0 0 0 0 8 8 4 4 4 4 4 4 4 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8
0 0 0 0 8 8 4 2 2 2 2 2 4 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8
0 0 0 0 8 8 4 2 2 2 2 2 4 8 8 0 0 0 0 8 8 4 4 4 4 4 4 4 8 8
0 0 0 0 8 8 4 2 2 2 2 2 4 8 8 0 0 0 0 8 8 4 2 2 2 2 2 4 8 8
0 0 0 0 8 8 4 4 4 4 4 4 4 8 8 0 0 0 0 8 8 4 2 2 2 2 2 4 8 8
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 4 2 2 2 2 2 4 8 8
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 4 4 4 4 4 4 4 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8
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
Pixels Off: 110
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 24.444444444444457
