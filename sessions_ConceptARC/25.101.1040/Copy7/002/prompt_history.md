
## train_1

**input:**
```
6 3 6 6 6 6 0 7 7 7 7 7 7
6 0 3 0 0 6 0 7 0 0 0 0 7
6 0 0 3 0 6 0 7 0 0 0 0 7
6 0 0 0 3 6 0 7 0 0 0 0 7
6 0 0 0 0 3 0 7 0 0 0 0 7
6 6 6 6 6 6 0 7 7 7 7 7 7
```


**output:**
```
6 3 6 6 6 6 0 7 3 7 7 7 7
6 0 3 0 0 6 0 7 0 3 0 0 7
6 0 0 3 0 6 0 7 0 0 3 0 7
6 0 0 0 3 6 0 7 0 0 0 3 7
6 0 0 0 0 3 0 7 0 0 0 0 3
6 6 6 6 6 6 0 7 7 7 7 7 7
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
4 4 4 4 1 0 0 0 0 0
4 4 4 1 4 0 0 0 0 0
4 4 1 4 4 0 0 2 2 2
4 1 4 4 4 0 0 2 2 2
1 4 4 4 4 0 0 2 2 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
4 4 4 4 1 0 0 0 0 0
4 4 4 1 4 0 0 0 0 0
4 4 1 4 4 0 0 2 2 1
4 1 4 4 4 0 0 2 1 2
1 4 4 4 4 0 0 1 2 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

*   **Perception:** The task involves identifying two primary non-background objects in the input grid. One object contains an internal pattern, specifically a diagonal line of a distinct color. The other object is typically a solid color block. The transformation consists of copying the internal diagonal pattern from the first object ("source") into the second object ("target"), preserving the pattern's color and its relative position within the bounds of the target object. The original objects and the background remain otherwise unchanged.

*   **Facts YAML:**
    
```yaml
    task_type: pattern_transfer
    components:
      - role: background
        properties:
          color: white (0)
      - role: source_object
        properties:
          shape: variable (rectangle, irregular)
          main_color: variable (magenta, yellow in examples)
          contains_pattern: true
          pattern:
            shape: diagonal_line
            color: variable (green, blue in examples)
            orientation: variable (top-left to bottom-right, top-right to bottom-left)
            position: relative to source_object boundaries
      - role: target_object
        properties:
          shape: variable (rectangle)
          main_color: variable (orange, red in examples)
          contains_pattern: false (initially)
      - role: separator (optional)
        properties:
          color: white (0)
          shape: vertical_line (example 1)
    actions:
      - type: identify
        target: source_object
        criteria: non-background object containing an internal pattern (pixels of a different color within its bounds)
      - type: extract
        source: source_object
        details: pattern color, relative coordinates of pattern pixels within source bounds
      - type: identify
        target: target_object
        criteria: non-background object without an internal pattern
      - type: apply_pattern
        target: target_object
        details:
          pattern_color: extracted from source_object
          pattern_coordinates: calculated by adding relative pattern coordinates (from source) to target_object's top-left corner coordinate
    relationships:
      - type: spatial
        between: source_object, target_object
        details: usually spatially separated, relative positions can vary
      - type: pattern_correspondence
        between: source_pattern, target_pattern (created)
        details: relative position and orientation within object bounds are identical
    ```


*   **Natural Language Program:**
    1.  Identify all distinct, contiguous non-background objects in the input grid.
    2.  For each object, determine its bounding box and primary color (most frequent color within the box).
    3.  Locate the "source object": the object containing pixels within its bounding box that are neither the background color nor its own primary color. These differing pixels constitute the "internal pattern".
    4.  Record the color of the internal pattern pixels and their coordinates relative to the top-left corner of the source object's bounding box.
    5.  Locate the "target object": a distinct non-background object that does not contain an internal pattern. Determine its bounding box.
    6.  Initialize the output grid as a copy of the input grid.
    7.  Iterate through the recorded relative coordinates of the source object's internal pattern. For each relative coordinate `(dr, dc)`:
        a.  Calculate the corresponding absolute coordinate `(r, c)` within the output grid by adding the relative coordinate `(dr, dc)` to the top-left coordinate of the target object's bounding box.
        b.  Change the color of the pixel at `(r, c)` in the output grid to the recorded pattern color.
    8.  Return the modified output grid.
```python
import numpy as np
from scipy.ndimage import label, find_objects, center_of_mass

"""
Identify two primary non-background objects. One object (source) contains an internal pattern, typically a diagonal line of a distinct color. The other object (target) is initially solid.
Copy the pattern's type (e.g., diagonal, anti-diagonal) and color from the source object's bounding box context to the target object's bounding box context.
The pattern's specific parameter (like the constant sum for an anti-diagonal) is determined relative to the target bounding box dimensions.
The pattern is applied by changing the color of the pixels within the target's bounding box that satisfy the derived pattern rule for the target context.
"""

def find_connected_components(grid, background_color=0):
    """Finds connected components of non-background colors."""
    objects = {}
    binary_grid = grid != background_color
    labeled_array, num_features = label(binary_grid)

    if num_features == 0:
        return objects

    slices = find_objects(labeled_array)
    for i, slc in enumerate(slices):
        obj_id = i + 1
        obj_mask = labeled_array[slc] == obj_id
        coords_raw = np.argwhere(labeled_array == obj_id)
        # Use the color of the first pixel found for this component
        # This assumes components are single-colored, which holds for ARC objects
        obj_color = grid[coords_raw[0, 0], coords_raw[0, 1]]

        # Ensure coords are relative to the full grid, not the slice
        coords = list(tuple(coord) for coord in coords_raw)

        min_r = np.min(coords_raw[:, 0])
        min_c = np.min(coords_raw[:, 1])
        max_r = np.max(coords_raw[:, 0])
        max_c = np.max(coords_raw[:, 1])
        bbox = (min_r, min_c, max_r, max_c)

        # Store object info: color, coordinates, bounding box
        if obj_color != background_color:
             # Use center of mass row as a unique-enough key for the object
             # center_r, center_c = center_of_mass(grid, labeled_array, obj_id)
             # obj_key = round(center_r * grid.shape[1] + center_c) # Simple hash
             obj_key = obj_id # Use label id as key
             objects[obj_key] = {
                 'color': obj_color,
                 'coords': coords,
                 'bbox': bbox
            }

    return objects

def get_pixels_in_bbox(grid, bbox):
    """Extracts all pixels (r, c, color) within a bounding box."""
    min_r, min_c, max_r, max_c = bbox
    pixels = []
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
             # Check bounds just in case bbox extends beyond grid (shouldn't happen with find_objects)
             if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
                pixels.append((r, c, grid[r, c]))
    return pixels

def identify_source_target(objects, grid, background_color=0):
    """Identifies source (has pattern) and target (no pattern) objects."""
    source_obj = None
    target_obj = None
    pattern_color = -1 # Invalid color initially

    obj_keys = list(objects.keys())
    if len(obj_keys) < 2:
        # Need at least two objects for source and target
        return None, None, -1

    potential_sources = []
    potential_targets = []

    for obj_key, obj_data in objects.items():
        obj_color = obj_data['color']
        bbox = obj_data['bbox']
        pixels_in_bbox = get_pixels_in_bbox(grid, bbox)
        has_pattern = False
        local_pattern_color = -1

        for r, c, color in pixels_in_bbox:
            if color != background_color and color != obj_color:
                # Found a pixel within the bbox that's not background and not the object's main color
                has_pattern = True
                local_pattern_color = color # Assume pattern is one color
                break # Only need one pattern pixel to classify

        if has_pattern:
            potential_sources.append((obj_key, local_pattern_color))
        else:
            potential_targets.append(obj_key)

    # Basic assumption: one source, one target
    if len(potential_sources) == 1 and len(potential_targets) >= 1:
        source_key, pattern_color = potential_sources[0]
        source_obj = objects[source_key]
        # Find the target object that is *different* from the source object
        # In simple cases, there might be only one potential target.
        # If multiple, this logic might need refinement (e.g., nearest, largest).
        # Let's pick the first one found that isn't the source.
        for target_key in potential_targets:
             if target_key != source_key:
                 target_obj = objects[target_key]
                 break # Found a distinct target

    return source_obj, target_obj, pattern_color


def get_pattern_relative_coords(grid, source_bbox, source_color, pattern_color, background_color=0):
    """Finds pattern pixels within source bbox and returns their relative coordinates."""
    min_r, min_c, max_r, max_c = source_bbox
    relative_coords = []
    pixels_in_bbox = get_pixels_in_bbox(grid, source_bbox)

    for r, c, color in pixels_in_bbox:
        if color == pattern_color:
            # Ensure this pixel is truly inside the bbox bounds defined
            if min_r <= r <= max_r and min_c <= c <= max_c:
                 dr = r - min_r
                 dc = c - min_c
                 relative_coords.append((dr, dc))

    return relative_coords

def determine_pattern_rule(relative_coords, H_s, W_s):
    """Determines pattern type and parameter k_s from relative coordinates."""
    if not relative_coords:
        return 'unknown', -1

    # Use the first point to guess the rule parameter k
    dr0, dc0 = relative_coords[0]

    # Check for anti-diagonal: dr + dc = k_s
    k_s_anti = dr0 + dc0
    is_anti_diag = all(dr + dc == k_s_anti for dr, dc in relative_coords)
    if is_anti_diag:
        return 'anti_diag', k_s_anti

    # Check for main diagonal offset: dr = dc + k_s => k_s = dr - dc
    k_s_main = dr0 - dc0
    is_main_diag = all(dr - dc == k_s_main for dr, dc in relative_coords)
    if is_main_diag:
        return 'main_diag_offset', k_s_main

    # Check for horizontal line: dr = k_s
    k_s_horiz = dr0
    is_horiz = all(dr == k_s_horiz for dr, dc in relative_coords)
    if is_horiz:
         return 'horiz', k_s_horiz

    # Check for vertical line: dc = k_s
    k_s_vert = dc0
    is_vert = all(dc == k_s_vert for dr, dc in relative_coords)
    if is_vert:
         return 'vert', k_s_vert

    return 'unknown', -1


def calculate_target_parameter(pattern_type, k_s, H_t, W_t):
    """Calculates the corresponding parameter k_t for the target bbox."""
    if pattern_type == 'main_diag_offset':
        # Offset relative to main diagonal seems constant
        return k_s
    elif pattern_type == 'anti_diag':
        # Anti-diagonal position depends on the target dimensions.
        # Based on train_2, where k_s=4 (for 5x5) became k_t=2 (for 3x3)
        # k_t = H_t - 1 seems to work. Let's use that.
        # Alternative: k_t = H_t - 1 + W_t - 1 - k_s might map opposite corners but failed test.
        return H_t - 1 # Tentative rule
    elif pattern_type == 'horiz':
        # Horizontal line at specific row index relative to bbox top
        return k_s
    elif pattern_type == 'vert':
         # Vertical line at specific col index relative to bbox left
         return k_s
    else:
        return -1 # Unknown or unsupported pattern

def apply_pattern_rule(output_grid, target_bbox, pattern_type, k_t, pattern_color):
    """Applies the pattern rule to modify the output grid within the target bbox."""
    if pattern_type == 'unknown' or k_t == -1:
        return # Cannot apply unknown pattern

    min_r, min_c, max_r, max_c = target_bbox
    H_t = max_r - min_r + 1
    W_t = max_c - min_c + 1

    for dr_t in range(H_t):
        for dc_t in range(W_t):
            apply = False
            if pattern_type == 'main_diag_offset' and dr_t - dc_t == k_t:
                apply = True
            elif pattern_type == 'anti_diag' and dr_t + dc_t == k_t:
                 apply = True
            elif pattern_type == 'horiz' and dr_t == k_t:
                 apply = True
            elif pattern_type == 'vert' and dc_t == k_t:
                 apply = True

            if apply:
                # Calculate absolute coordinates
                abs_r = min_r + dr_t
                abs_c = min_c + dc_t
                # Check if coordinates are within grid bounds before painting
                if 0 <= abs_r < output_grid.shape[0] and 0 <= abs_c < output_grid.shape[1]:
                    output_grid[abs_r, abs_c] = pattern_color

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by identifying a source object with a pattern
    and a target object, then copying the pattern type (e.g., diagonal)
    and color to the target object's bounding box, adjusting its parameters
    relative to the target dimensions.
    """
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    background_color = 0 # Assuming background is 0 (white)

    # 1. Find all distinct non-background objects
    objects = find_connected_components(input_array, background_color)
    if not objects or len(objects) < 2:
         # Need at least source and target
         return input_grid # Return original if cannot proceed

    # 2. Identify Source (with pattern) and Target (without)
    source_obj, target_obj, pattern_color = identify_source_target(objects, input_array, background_color)

    if source_obj is None or target_obj is None or pattern_color == -1:
        # Failed to identify required components
        return input_grid

    # 3. Get bounding boxes and source object details
    source_bbox = source_obj['bbox']
    target_bbox = target_obj['bbox']
    source_color = source_obj['color']
    H_s = source_bbox[2] - source_bbox[0] + 1
    W_s = source_bbox[3] - source_bbox[1] + 1
    H_t = target_bbox[2] - target_bbox[0] + 1
    W_t = target_bbox[3] - target_bbox[1] + 1

    # 4. Find pattern pixels relative to source bbox
    relative_coords = get_pattern_relative_coords(input_array, source_bbox, source_color, pattern_color, background_color)
    if not relative_coords:
         # No pattern pixels found where expected
         return input_grid

    # 5. Determine pattern rule (type and k_s) from source relative coordinates
    pattern_type, k_s = determine_pattern_rule(relative_coords, H_s, W_s)

    # 6. Calculate the corresponding parameter k_t for the target context
    k_t = calculate_target_parameter(pattern_type, k_s, H_t, W_t)

    # 7. Apply the pattern rule using k_t within the target bbox
    apply_pattern_rule(output_array, target_bbox, pattern_type, k_t, pattern_color)

    # Convert back to list of lists for the required output format
    return output_array.tolist()
```
