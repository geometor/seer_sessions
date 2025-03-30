
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
## General Assessment

The provided code attempts to solve the task by identifying objects, classifying them as "sources" (containing multiple colors) or "targets" (containing a single color) based on a "primary color" derived from the object's pixels, and then copying a pattern from the source to the targets.

The code failed on all training examples. The results show that while the object identification and source/target classification might be conceptually correct, the specific definition of the "pattern" being copied and the method of placing it onto the target are flawed.

*   **Incorrect Pattern Extraction:** The code extracts the entire bounding box of the source object as the pattern. However, the expected outputs indicate that only the *internal* content of the source (pixels *different* from the primary/frame color) should be considered the pattern.
*   **Incorrect Pattern Placement:** The code places the extracted pattern by aligning the top-left corner of the pattern with the top-left corner of the target object's bounding box, overwriting whatever is there. The expected outputs show that the source's internal pattern should replace the *internal* content of the target, leaving the target's frame (pixels matching the primary color) intact.

**Strategy:**

1.  Refine the definition of the "source pattern": It consists only of the pixels within the source object's bounding box that *do not* match the object's primary/frame color.
2.  Refine the pattern application logic: For each target object, identify the area corresponding to its internal content. Copy the source pattern into this area, pixel by pixel, preserving the target's original frame pixels. The relative position of the pattern pixels within the source frame should be maintained when placing them inside the target frame.

## Metrics

| Example | Input Objects                                                                   | Output Objects                                                                       | Code Failure Analysis                                                                                                                               |
| :------ | :------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1       | Source: Green frame with Yellow/Blue/Azure inside. Target: Green frame.         | Source: Unchanged. Target: Green frame with Yellow/Blue/Azure pattern copied inside.   | Code copied the source's Green frame *and* its contents, overwriting the top-left part of the target frame and adjacent background.                  |
| 2       | Source: Red frame with Magenta/Azure inside. Targets: Two Red frames.           | Source: Unchanged. Targets: Both Red frames with Magenta/Azure pattern copied inside. | Code copied the source's Red frame *and* its contents onto the top-left of both target frames, overwriting parts of the target frames and background. |
| 3       | Source: Azure frame with Yellow/Red inside. Targets: Two Azure frames.          | Source: Unchanged. Targets: Both Azure frames with Yellow/Red pattern copied inside.   | Code copied the source's Azure frame *and* its contents onto the top-left of both target frames, overwriting parts of the target frames and background. |

## YAML Facts


```yaml
task_description: Copy the internal pattern from a 'source' object into one or more 'target' objects of the same primary color.

definitions:
  object: A connected component of non-background (non-white) pixels.
  primary_color: The color forming the outer frame or main body of an object. For multi-colored objects, it's typically the color of the outermost layer or the most frequent color connected to the background. For single-colored objects, it's simply that color. (Refinement: The code's method of using the first found pixel seems sufficient for these examples, as the frames are uniform).
  source_object: An object containing pixels of its primary color AND pixels of other color(s) internally.
  target_object: An object containing *only* pixels of its primary color.
  internal_pattern: The configuration of pixels within the source object's bounding box whose color is *different* from the source object's primary color.
  frame_pixels: Pixels within an object's bounding box whose color *matches* the object's primary color.

observations:
  - The grid contains one or more objects, identifiable by their color and connectivity.
  - Objects can be grouped by their primary color (e.g., all green-framed objects).
  - Within each color group, there is typically one source object and one or more target objects.
  - The source object contains an internal pattern composed of colors different from its primary color.
  - Target objects are composed solely of their primary color and share the same shape/size as the source object's frame in these examples.

actions:
  - Identify all objects and determine their primary color, bounding box, and pixel set.
  - Classify objects into sources and targets based on whether they contain colors other than their primary color.
  - Group objects by primary color.
  - For each group containing exactly one source and at least one target:
    - Define the source's internal pattern (pixels within the source bbox != primary color).
    - For each target object in the group:
      - Iterate through the positions within the source object's bounding box.
      - If a pixel at a relative position `(dr, dc)` within the source bounding box belongs to the *internal pattern* (i.e., its color is not the primary color):
        - Copy this pixel's color to the corresponding relative position `(dr, dc)` within the *target* object's bounding box in the output grid.
      - Pixels corresponding to the source's frame pixels are *not* copied; the target's frame pixels remain unchanged in the output grid.
  - The output grid starts as a copy of the input grid and is modified by these copy operations.

```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all distinct connected components (objects) of non-background (non-white) pixels in the input grid.
3.  For each object, determine its primary color (the color of its frame or main body, identifiable as the color of the first pixel encountered during object detection) and its bounding box.
4.  Classify each object:
    *   An object is a "source" if it contains at least one pixel whose color is different from its primary color.
    *   An object is a "target" if all its pixels have the same color (its primary color).
5.  Group the identified objects based on their primary color.
6.  Iterate through each group of objects sharing the same primary color.
7.  If a group contains exactly one source object and one or more target objects:
    a.  Let `S` be the source object and `P` be its primary color. Let `(min_r_src, min_c_src)` be the top-left corner of `S`'s bounding box.
    b.  For each target object `T` in the group:
        i.  Let `(min_r_tgt, min_c_tgt)` be the top-left corner of `T`'s bounding box.
        ii. Iterate through all relative coordinates `(dr, dc)` within the dimensions of the source object's bounding box.
        iii. Calculate the corresponding coordinates in the source: `sr = min_r_src + dr`, `sc = min_c_src + dc`.
        iv. Calculate the corresponding coordinates in the target: `tr = min_r_tgt + dr`, `tc = min_c_tgt + dc`.
        v.  Check if the pixel `input_grid[sr, sc]` is part of the source's *internal pattern* (i.e., `input_grid[sr, sc] != P`).
        vi. If it is part of the internal pattern AND the target coordinates `(tr, tc)` are within the grid bounds, update the output grid: `output_grid[tr, tc] = input_grid[sr, sc]`. (This overwrites the original content inside the target frame with the source's internal pattern).
8.  Return the modified output grid.
