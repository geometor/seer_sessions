**General Assessment and Strategy**

The previous code attempt correctly identified the core concept: transferring an internal pattern from a source object to a target object. It successfully solved Example 1. However, it failed on Example 2, producing an extra pattern pixel outside the intended target area.

The failure occurred because the chosen transfer method (aligning bounding box centers and translating absolute pattern coordinates) placed one translated pixel outside the target object's original bounding box. The expected output clearly shows the pattern should only be imprinted *within* the bounds of the target object.

**Strategy:**

1.  Maintain the overall approach: identify the two largest objects, determine source/target/pattern, calculate bounding box centers, and find the translation vector.
2.  Refine the final step: When applying the translation to each source pattern pixel's absolute coordinates, calculate the potential target coordinates.
3.  **Crucially, add a validation step:** Before modifying the output grid, verify that the calculated target coordinates fall BOTH within the overall grid dimensions AND within the bounding box of the *target* object.
4.  Only modify the output grid pixel if both validation checks pass. This prevents the pattern from "spilling" outside the target object's area.

**Metrics Gathering**

Let's verify object properties and the transformation specifics for each example.

``` python
import numpy as np
from collections import Counter
from skimage.measure import label, regionprops

def analyze_example(input_grid_list, output_grid_list):
    input_grid = np.array(input_grid_list)
    output_grid = np.array(output_grid_list)
    rows, cols = input_grid.shape
    analysis = {'input_shape': (rows, cols)}

    # --- Object Detection ---
    labeled_grid = label(input_grid > 0, connectivity=2)
    regions = regionprops(labeled_grid, intensity_image=input_grid)
    objects = []
    for region in regions:
        pixels = tuple(map(tuple, region.coords.T))
        if not pixels: continue
        non_white_colors = [c for c in region.intensity_image[region.image].flatten() if c != 0]
        if not non_white_colors: continue
        primary_color = Counter(non_white_colors).most_common(1)[0][0]
        objects.append({
            'id': region.label,
            'pixels_count': region.area,
            'bbox': region.bbox, # (min_r, min_c, max_r, max_c) - exclusive max
            'primary_color': primary_color,
        })
    objects.sort(key=lambda o: o['pixels_count'], reverse=True)
    analysis['objects'] = objects

    if len(objects) < 2:
        analysis['error'] = "Less than two objects found."
        return analysis

    # --- Identify Source/Target/Pattern ---
    obj_a = objects[0]
    obj_b = objects[1]
    source_obj_info = None
    target_obj_info = None
    pattern_color = None
    pattern_coords_abs = []

    def find_pattern(potential_source):
        bbox = potential_source['bbox']
        min_r, min_c, max_r, max_c = bbox
        primary_color = potential_source['primary_color']
        f_pattern_color = -1
        f_coords = []
        found = False
        for r in range(min_r, max_r):
            for c in range(min_c, max_c):
                if 0 <= r < rows and 0 <= c < cols:
                    color = input_grid[r, c]
                    if color != 0 and color != primary_color:
                        if not found:
                            f_pattern_color = color
                            found = True
                        if color == f_pattern_color:
                            f_coords.append((r, c))
                        else: # Inconsistent pattern colors
                             return False, -1, []
        return found, f_pattern_color, f_coords

    found_a, color_a, coords_a = find_pattern(obj_a)
    if found_a:
        source_obj_info = obj_a
        target_obj_info = obj_b
        pattern_color = color_a
        pattern_coords_abs = coords_a
    else:
        found_b, color_b, coords_b = find_pattern(obj_b)
        if found_b:
            source_obj_info = obj_b
            target_obj_info = obj_a
            pattern_color = color_b
            pattern_coords_abs = coords_b

    if not source_obj_info:
        analysis['error'] = "Could not identify source/target/pattern."
        return analysis

    analysis['source_object'] = source_obj_info
    analysis['target_object'] = target_obj_info
    analysis['pattern_color'] = pattern_color
    analysis['pattern_coords_absolute'] = pattern_coords_abs

    # --- Calculate Centers and Delta ---
    def calculate_center(bbox):
        min_r, min_c, max_r, max_c = bbox
        return (min_r + (max_r - min_r) / 2.0, min_c + (max_c - min_c) / 2.0)

    source_center = calculate_center(source_obj_info['bbox'])
    target_center = calculate_center(target_obj_info['bbox'])
    delta = (target_center[0] - source_center[0], target_center[1] - source_center[1])
    analysis['source_center'] = source_center
    analysis['target_center'] = target_center
    analysis['translation_delta'] = delta

    # --- Find Output Pattern Coords ---
    output_pattern_coords = []
    target_bbox = target_obj_info['bbox']
    min_rt, min_ct, max_rt, max_ct = target_bbox

    for r in range(rows):
        for c in range(cols):
            # Find pixels in output that have pattern color AND were different in input
            # AND fall within the target's original bounding box
            if output_grid[r,c] == pattern_color and input_grid[r,c] != pattern_color:
                 if min_rt <= r < max_rt and min_ct <= c < max_ct:
                     output_pattern_coords.append((r,c))
            # Alternative check: is it pattern color AND was it part of the original target pixels?
            # This is harder to check efficiently. Sticking with bbox check.

    analysis['output_pattern_coords'] = sorted(output_pattern_coords) # Sort for consistent comparison

    # --- Verify Transformation via Simulation ---
    simulated_output_coords = []
    for src_r, src_c in pattern_coords_abs:
        target_r = round(src_r + delta[0])
        target_c = round(src_c + delta[1])

        # Check grid bounds AND target bbox bounds
        if (0 <= target_r < rows and 0 <= target_c < cols and
            min_rt <= target_r < max_rt and min_ct <= target_c < max_ct):
            simulated_output_coords.append((target_r, target_c))

    analysis['simulated_output_coords'] = sorted(simulated_output_coords)
    analysis['simulation_matches_output'] = (analysis['simulated_output_coords'] == analysis['output_pattern_coords'])

    return analysis

# Example 1 Data
input1 = [
    [6, 3, 6, 6, 6, 6, 0, 7, 7, 7, 7, 7, 7],
    [6, 0, 3, 0, 0, 6, 0, 7, 0, 0, 0, 0, 7],
    [6, 0, 0, 3, 0, 6, 0, 7, 0, 0, 0, 0, 7],
    [6, 0, 0, 0, 3, 6, 0, 7, 0, 0, 0, 0, 7],
    [6, 0, 0, 0, 0, 3, 0, 7, 0, 0, 0, 0, 7],
    [6, 6, 6, 6, 6, 6, 0, 7, 7, 7, 7, 7, 7]
]
output1 = [
    [6, 3, 6, 6, 6, 6, 0, 7, 3, 7, 7, 7, 7],
    [6, 0, 3, 0, 0, 6, 0, 7, 0, 3, 0, 0, 7],
    [6, 0, 0, 3, 0, 6, 0, 7, 0, 0, 3, 0, 7],
    [6, 0, 0, 0, 3, 6, 0, 7, 0, 0, 0, 3, 7],
    [6, 0, 0, 0, 0, 3, 0, 7, 0, 0, 0, 0, 3],
    [6, 6, 6, 6, 6, 6, 0, 7, 7, 7, 7, 7, 7]
]

# Example 2 Data
input2 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 4, 4, 4, 1, 0, 0, 0, 0, 0],
    [4, 4, 4, 1, 4, 0, 0, 0, 0, 0],
    [4, 4, 1, 4, 4, 0, 0, 2, 2, 2],
    [4, 1, 4, 4, 4, 0, 0, 2, 2, 2],
    [1, 4, 4, 4, 4, 0, 0, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
output2 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 4, 4, 4, 1, 0, 0, 0, 0, 0],
    [4, 4, 4, 1, 4, 0, 0, 0, 0, 0],
    [4, 4, 1, 4, 4, 0, 0, 2, 2, 1],
    [4, 1, 4, 4, 4, 0, 0, 2, 1, 2],
    [1, 4, 4, 4, 4, 0, 0, 1, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

analysis1 = analyze_example(input1, output1)
analysis2 = analyze_example(input2, output2)

print("--- Example 1 Analysis ---")
print(f"Input Shape: {analysis1['input_shape']}")
print(f"Objects Found: {len(analysis1['objects'])}")
print(f"Source Object BBox: {analysis1['source_object']['bbox']}, Primary Color: {analysis1['source_object']['primary_color']}, Size: {analysis1['source_object']['pixels_count']}")
print(f"Target Object BBox: {analysis1['target_object']['bbox']}, Primary Color: {analysis1['target_object']['primary_color']}, Size: {analysis1['target_object']['pixels_count']}")
print(f"Pattern Color: {analysis1['pattern_color']}")
print(f"Pattern Coords (Abs): {analysis1['pattern_coords_absolute']}")
print(f"Source Center: {analysis1['source_center']}")
print(f"Target Center: {analysis1['target_center']}")
print(f"Delta: {analysis1['translation_delta']}")
print(f"Output Pattern Coords: {analysis1['output_pattern_coords']}")
print(f"Simulated Output Coords (Center Align + Target BBox Clip): {analysis1['simulated_output_coords']}")
print(f"Simulation Matches Output: {analysis1['simulation_matches_output']}")

print("\n--- Example 2 Analysis ---")
print(f"Input Shape: {analysis2['input_shape']}")
print(f"Objects Found: {len(analysis2['objects'])}")
print(f"Source Object BBox: {analysis2['source_object']['bbox']}, Primary Color: {analysis2['source_object']['primary_color']}, Size: {analysis2['source_object']['pixels_count']}")
print(f"Target Object BBox: {analysis2['target_object']['bbox']}, Primary Color: {analysis2['target_object']['primary_color']}, Size: {analysis2['target_object']['pixels_count']}")
print(f"Pattern Color: {analysis2['pattern_color']}")
print(f"Pattern Coords (Abs): {analysis2['pattern_coords_absolute']}")
print(f"Source Center: {analysis2['source_center']}")
print(f"Target Center: {analysis2['target_center']}")
print(f"Delta: {analysis2['translation_delta']}")
print(f"Output Pattern Coords: {analysis2['output_pattern_coords']}")
print(f"Simulated Output Coords (Center Align + Target BBox Clip): {analysis2['simulated_output_coords']}")
print(f"Simulation Matches Output: {analysis2['simulation_matches_output']}")


```
``` failed
Traceback (most recent call last):
  File "<string>", line 3, in <module>
ModuleNotFoundError: No module named 'skimage'

```
**Revised Metrics Gathering (using fallback BFS)**
It seems `skimage` is unavailable. Rerunning analysis using the BFS object detection.

``` python
import numpy as np
from collections import deque, Counter

# --- BFS Object Detection ---
def _get_neighbors(r, c, rows, cols):
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0: continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols: neighbors.append((nr, nc))
    return neighbors

def _find_objects_bfs(grid):
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    object_id_counter = 1
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                obj_pixels = []
                obj_colors = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c, max_r, max_c = r, c, r, c
                component_color = grid[r,c] # Assume components are single-color for simplicity here
                                            # More robust: find connected region regardless of color, then analyze colors

                component_queue = deque([(r,c)])
                component_visited = set([(r,c)])

                while component_queue:
                    curr_r, curr_c = component_queue.popleft()
                    # Check grid color consistency within the component if needed,
                    # but for ARC usually objects are single-colored or have distinct internal patterns
                    if grid[curr_r, curr_c] == 0: continue # Should not happen if started on non-zero

                    obj_pixels.append((curr_r, curr_c))
                    obj_colors.append(grid[curr_r, curr_c])
                    min_r, min_c = min(min_r, curr_r), min(min_c, curr_c)
                    max_r, max_c = max(max_r, curr_r), max(max_c, curr_c)

                    for nr, nc in _get_neighbors(curr_r, curr_c, rows, cols):
                         # Connect based on non-zero, handle color variations later
                         if grid[nr, nc] != 0 and not visited[nr, nc]:
                             visited[nr, nc] = True
                             component_queue.append((nr, nc)) # Add to queue regardless of color match for full object finding
                             component_visited.add((nr,nc)) # Track visited for this object search
                         # Note: The original BFS had a bug trying to enforce same color connection AND
                         # prevent future BFS starting points. Simpler to just find connected non-zero regions.

                if obj_pixels:
                    # Recalculate primary color from actual pixels found
                    non_white_colors = [col for col in obj_colors if col != 0]
                    if not non_white_colors: continue
                    primary_color = Counter(non_white_colors).most_common(1)[0][0]
                    # Bbox: inclusive max + 1 for range/slice convention
                    bbox = (min_r, min_c, max_r + 1, max_c + 1)
                    objects.append({
                        'id': object_id_counter,
                        'pixels_count': len(obj_pixels), # Use actual pixel count
                        'bbox': bbox,
                        'primary_color': primary_color,
                    })
                    object_id_counter += 1

    objects.sort(key=lambda o: o['pixels_count'], reverse=True)
    return objects

# --- Analysis Function (using BFS) ---
def analyze_example(input_grid_list, output_grid_list):
    input_grid = np.array(input_grid_list)
    output_grid = np.array(output_grid_list)
    rows, cols = input_grid.shape
    analysis = {'input_shape': (rows, cols)}

    # Use BFS for object detection
    objects = _find_objects_bfs(input_grid)
    analysis['objects'] = objects

    if len(objects) < 2:
        analysis['error'] = "Less than two objects found."
        return analysis

    obj_a = objects[0]
    obj_b = objects[1]
    source_obj_info = None
    target_obj_info = None
    pattern_color = None
    pattern_coords_abs = []

    def find_pattern(potential_source):
        bbox = potential_source['bbox']
        min_r, min_c, max_r, max_c = bbox
        primary_color = potential_source['primary_color']
        f_pattern_color = -1
        f_coords = []
        found = False
        for r in range(min_r, max_r):
            for c in range(min_c, max_c):
                if 0 <= r < rows and 0 <= c < cols:
                    color = input_grid[r, c]
                    if color != 0 and color != primary_color:
                        if not found:
                            f_pattern_color = color
                            found = True
                        if color == f_pattern_color:
                            f_coords.append((r, c))
                        else: return False, -1, []
        return found, f_pattern_color, f_coords

    found_a, color_a, coords_a = find_pattern(obj_a)
    if found_a:
        source_obj_info = obj_a
        target_obj_info = obj_b
        pattern_color = color_a
        pattern_coords_abs = coords_a
    else:
        found_b, color_b, coords_b = find_pattern(obj_b)
        if found_b:
            source_obj_info = obj_b
            target_obj_info = obj_a
            pattern_color = color_b
            pattern_coords_abs = coords_b

    if not source_obj_info:
        analysis['error'] = "Could not identify source/target/pattern."
        return analysis

    analysis['source_object'] = source_obj_info
    analysis['target_object'] = target_obj_info
    analysis['pattern_color'] = pattern_color
    analysis['pattern_coords_absolute'] = pattern_coords_abs

    def calculate_center(bbox):
        min_r, min_c, max_r, max_c = bbox
        return (min_r + (max_r - min_r) / 2.0, min_c + (max_c - min_c) / 2.0)

    source_center = calculate_center(source_obj_info['bbox'])
    target_center = calculate_center(target_obj_info['bbox'])
    delta = (target_center[0] - source_center[0], target_center[1] - source_center[1])
    analysis['source_center'] = source_center
    analysis['target_center'] = target_center
    analysis['translation_delta'] = delta

    output_pattern_coords = []
    target_bbox = target_obj_info['bbox']
    min_rt, min_ct, max_rt, max_ct = target_bbox

    for r in range(rows):
        for c in range(cols):
            if output_grid[r,c] == pattern_color and input_grid[r,c] != pattern_color:
                 if min_rt <= r < max_rt and min_ct <= c < max_ct:
                     output_pattern_coords.append((r,c))

    analysis['output_pattern_coords'] = sorted(output_pattern_coords)

    simulated_output_coords = []
    for src_r, src_c in pattern_coords_abs:
        target_r = round(src_r + delta[0])
        target_c = round(src_c + delta[1])
        if (0 <= target_r < rows and 0 <= target_c < cols and
            min_rt <= target_r < max_rt and min_ct <= target_c < max_ct):
            simulated_output_coords.append((target_r, target_c))

    analysis['simulated_output_coords'] = sorted(simulated_output_coords)
    analysis['simulation_matches_output'] = (analysis['simulated_output_coords'] == analysis['output_pattern_coords'])

    return analysis

# Example 1 Data
input1 = [
    [6, 3, 6, 6, 6, 6, 0, 7, 7, 7, 7, 7, 7],
    [6, 0, 3, 0, 0, 6, 0, 7, 0, 0, 0, 0, 7],
    [6, 0, 0, 3, 0, 6, 0, 7, 0, 0, 0, 0, 7],
    [6, 0, 0, 0, 3, 6, 0, 7, 0, 0, 0, 0, 7],
    [6, 0, 0, 0, 0, 3, 0, 7, 0, 0, 0, 0, 7],
    [6, 6, 6, 6, 6, 6, 0, 7, 7, 7, 7, 7, 7]
]
output1 = [
    [6, 3, 6, 6, 6, 6, 0, 7, 3, 7, 7, 7, 7],
    [6, 0, 3, 0, 0, 6, 0, 7, 0, 3, 0, 0, 7],
    [6, 0, 0, 3, 0, 6, 0, 7, 0, 0, 3, 0, 7],
    [6, 0, 0, 0, 3, 6, 0, 7, 0, 0, 0, 3, 7],
    [6, 0, 0, 0, 0, 3, 0, 7, 0, 0, 0, 0, 3],
    [6, 6, 6, 6, 6, 6, 0, 7, 7, 7, 7, 7, 7]
]

# Example 2 Data
input2 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 4, 4, 4, 1, 0, 0, 0, 0, 0],
    [4, 4, 4, 1, 4, 0, 0, 0, 0, 0],
    [4, 4, 1, 4, 4, 0, 0, 2, 2, 2],
    [4, 1, 4, 4, 4, 0, 0, 2, 2, 2],
    [1, 4, 4, 4, 4, 0, 0, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
output2 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 4, 4, 4, 1, 0, 0, 0, 0, 0],
    [4, 4, 4, 1, 4, 0, 0, 0, 0, 0],
    [4, 4, 1, 4, 4, 0, 0, 2, 2, 1],
    [4, 1, 4, 4, 4, 0, 0, 2, 1, 2],
    [1, 4, 4, 4, 4, 0, 0, 1, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

analysis1 = analyze_example(input1, output1)
analysis2 = analyze_example(input2, output2)

print("--- Example 1 Analysis (BFS) ---")
print(f"Input Shape: {analysis1['input_shape']}")
print(f"Objects Found: {len(analysis1['objects'])}")
print(f"Source Object BBox: {analysis1['source_object']['bbox']}, Primary Color: {analysis1['source_object']['primary_color']}, Size: {analysis1['source_object']['pixels_count']}")
print(f"Target Object BBox: {analysis1['target_object']['bbox']}, Primary Color: {analysis1['target_object']['primary_color']}, Size: {analysis1['target_object']['pixels_count']}")
print(f"Pattern Color: {analysis1['pattern_color']}")
print(f"Pattern Coords (Abs): {analysis1['pattern_coords_absolute']}")
print(f"Source Center: {analysis1['source_center']}")
print(f"Target Center: {analysis1['target_center']}")
print(f"Delta: {analysis1['translation_delta']}")
print(f"Output Pattern Coords: {analysis1['output_pattern_coords']}")
print(f"Simulated Output Coords (Center Align + Target BBox Clip): {analysis1['simulated_output_coords']}")
print(f"Simulation Matches Output: {analysis1['simulation_matches_output']}")

print("\n--- Example 2 Analysis (BFS) ---")
print(f"Input Shape: {analysis2['input_shape']}")
print(f"Objects Found: {len(analysis2['objects'])}")
print(f"Source Object BBox: {analysis2['source_object']['bbox']}, Primary Color: {analysis2['source_object']['primary_color']}, Size: {analysis2['source_object']['pixels_count']}")
print(f"Target Object BBox: {analysis2['target_object']['bbox']}, Primary Color: {analysis2['target_object']['primary_color']}, Size: {analysis2['target_object']['pixels_count']}")
print(f"Pattern Color: {analysis2['pattern_color']}")
print(f"Pattern Coords (Abs): {analysis2['pattern_coords_absolute']}")
print(f"Source Center: {analysis2['source_center']}")
print(f"Target Center: {analysis2['target_center']}")
print(f"Delta: {analysis2['translation_delta']}")
print(f"Output Pattern Coords: {analysis2['output_pattern_coords']}")
print(f"Simulated Output Coords (Center Align + Target BBox Clip): {analysis2['simulated_output_coords']}")
print(f"Simulation Matches Output: {analysis2['simulation_matches_output']}")
```
```
--- Example 1 Analysis (BFS) ---
Input Shape: (6, 13)
Objects Found: 2
Source Object BBox: (0, 0, 6, 6), Primary Color: 6, Size: 23
Target Object BBox: (0, 7, 6, 13), Primary Color: 7, Size: 20
Pattern Color: 3
Pattern Coords (Abs): [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]
Source Center: (3.0, 3.0)
Target Center: (3.0, 10.0)
Delta: (0.0, 7.0)
Output Pattern Coords: [(0, 8), (1, 9), (2, 10), (3, 11), (4, 12)]
Simulated Output Coords (Center Align + Target BBox Clip): [(0, 8), (1, 9), (2, 10), (3, 11), (4, 12)]
Simulation Matches Output: True

--- Example 2 Analysis (BFS) ---
Input Shape: (10, 10)
Objects Found: 2
Source Object BBox: (1, 0, 6, 5), Primary Color: 4, Size: 25
Target Object BBox: (3, 7, 6, 10), Primary Color: 2, Size: 9
Pattern Color: 1
Pattern Coords (Abs): [(1, 4), (2, 3), (3, 2), (4, 1), (5, 0)]
Source Center: (3.5, 2.5)
Target Center: (4.5, 8.5)
Delta: (1.0, 6.0)
Output Pattern Coords: [(3, 9), (4, 8), (5, 7)]
Simulated Output Coords (Center Align + Target BBox Clip): [(3, 9), (4, 8), (5, 7)]
Simulation Matches Output: True

```
**YAML Facts**


```yaml
task_description: Identify two main objects, find an internal pattern in one (source), and transfer this pattern to the other (target) by aligning bounding box centers, applying the resulting translation to the pattern's absolute coordinates, and clipping the result to the target's bounding box.

definitions:
  - object: A connected component of non-white pixels. Identified using BFS or skimage.label.
  - bounding_box: The smallest rectangle enclosing all pixels of an object. Represented as (min_row, min_col, max_row, max_col), where max is exclusive.
  - primary_color: The most frequent non-white color within an object's pixels.
  - pattern_color: A single color found within the source object's bounding box that differs from its primary color and is not white.
  - pattern_pixels_absolute: A list of (row, col) tuples representing the absolute coordinates of all pixels with the pattern_color within the source object's bounding box.
  - source_object: The object (usually one of the two largest) whose bounding box contains the pattern_pixels_absolute.
  - target_object: The other large object onto which the pattern is transferred.
  - bbox_center: The geometric center coordinates (potentially fractional) of a bounding box, calculated as (min_r + height/2, min_c + width/2).
  - translation_vector: The difference (delta_r, delta_c) between the target_object's bbox_center and the source_object's bbox_center.

actions:
  - identify_objects: Find all distinct non-white connected components and their properties (pixels, primary_color, bounding_box, size).
  - select_main_objects: Choose the two objects with the largest pixel counts. Handle cases with fewer than two objects.
  - identify_source_target_pattern:
      - For each of the two main objects:
        - Check if its bounding box contains pixels of a single color that is different from its primary_color and not white.
        - If yes, designate this object as 'source', the other main object as 'target', the differing color as 'pattern_color', and record the absolute coordinates of these pattern pixels ('pattern_pixels_absolute').
  - calculate_centers_and_delta: Compute the bbox_center for both source and target objects and find the translation_vector (target_center - source_center).
  - apply_pattern_to_target:
      - Initialize the output grid as a copy of the input.
      - For each coordinate (src_r, src_c) in 'pattern_pixels_absolute':
        - Calculate potential target coordinates: target_r = round(src_r + delta_r), target_c = round(src_c + delta_c).
        - Validate target coordinates: Check if (target_r, target_c) is within the grid dimensions AND within the target_object's bounding_box (min_rt <= target_r < max_rt and min_ct <= target_c < max_ct).
        - If validation passes, update the pixel at (target_r, target_c) in the output grid to the 'pattern_color'.
  - finalize_output: Return the modified output grid.

example_1_analysis:
  objects_found: 2
  source_object: {bbox: (0, 0, 6, 6), primary_color: 6, size: 23}
  target_object: {bbox: (0, 7, 6, 13), primary_color: 7, size: 20}
  pattern_color: 3
  pattern_pixels_absolute: [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]
  translation_delta: (0.0, 7.0) # Using integer centers gives (0,7) delta as well
  output_pattern_coords: [(0, 8), (1, 9), (2, 10), (3, 11), (4, 12)]
  simulation_matches_output: True # Center align + target bbox clip works

example_2_analysis:
  objects_found: 2
  source_object: {bbox: (1, 0, 6, 5), primary_color: 4, size: 25}
  target_object: {bbox: (3, 7, 6, 10), primary_color: 2, size: 9}
  pattern_color: 1
  pattern_pixels_absolute: [(1, 4), (2, 3), (3, 2), (4, 1), (5, 0)]
  translation_delta: (1.0, 6.0)
  output_pattern_coords: [(3, 9), (4, 8), (5, 7)]
  simulation_matches_output: True # Center align + target bbox clip works

```


**Natural Language Program**

1.  **Initialize:** Create a copy of the input grid to serve as the output grid.
2.  **Identify Objects:** Find all connected components of non-white pixels in the input grid. For each object, determine its pixel coordinates, primary color (most frequent non-white color), pixel count, and bounding box (min_row, min_col, max_row_exclusive, max_col_exclusive).
3.  **Select Main Objects:** Identify the two objects with the largest pixel counts. If fewer than two objects exist, stop and return the copied input grid. Label them Object A and Object B.
4.  **Find Source, Target, and Pattern:**
    a.  Check if Object A's bounding box contains pixels of a single color ('Pattern Color A') that is not white and not Object A's primary color. If yes, designate Object A as the `source_object`, Object B as the `target_object`, 'Pattern Color A' as the `pattern_color`, and record the absolute (row, column) coordinates of all pixels with 'Pattern Color A' within Object A's bounding box as `pattern_coords_absolute`. Proceed to step 5.
    b.  If no pattern was found in Object A, perform the same check for Object B: Check if Object B's bounding box contains pixels of a single color ('Pattern Color B') different from its primary color and white. If yes, designate Object B as `source_object`, Object A as `target_object`, 'Pattern Color B' as `pattern_color`, and record the absolute coordinates of these pattern pixels as `pattern_coords_absolute`. Proceed to step 5.
    c.  If neither object contains such a pattern, stop and return the copied input grid.
5.  **Calculate Bounding Box Centers:**
    a.  Determine the center coordinates (center_r, center_c) for the `source_object`'s bounding box.
    b.  Determine the center coordinates (center_r, center_c) for the `target_object`'s bounding box.
6.  **Calculate Translation:** Compute the difference vector (`delta_r`, `delta_c`) by subtracting the source center coordinates from the target center coordinates.
7.  **Apply Translated Pattern with Clipping:**
    a.  Get the bounding box coordinates (`min_rt`, `min_ct`, `max_rt`, `max_ct`) of the `target_object`.
    b.  For each absolute coordinate (`src_r`, `src_c`) in `pattern_coords_absolute`:
        i.  Calculate the potential target coordinates: `target_r = round(src_r + delta_r)`, `target_c = round(src_c + delta_c)`.
        ii. Check if the target coordinates are within the grid bounds (0 <= `target_r` < grid_rows, 0 <= `target_c` < grid_cols).
        iii.Check if the target coordinates are within the *target object's bounding box* (`min_rt` <= `target_r` < `max_rt`, `min_ct` <= `target_c` < `max_ct`).
        iv. If both checks (ii and iii) pass, update the pixel at (`target_r`, `target_c`) in the output grid to the `pattern_color`.
8.  **Finalize:** Return the modified output grid.