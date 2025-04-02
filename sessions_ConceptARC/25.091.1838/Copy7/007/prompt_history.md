
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

Okay, let's analyze the provided examples to understand the transformation logic.

**Perception of Elements:**

*   **Example 1:**
    *   Input: Contains two main visual elements separated by white pixels.
        *   Left element: A magenta (6) square frame containing a diagonal line of green (3) pixels.
        *   Right element: An orange (7) square frame containing only white (0) pixels internally.
    *   Output: The overall structure is preserved. The left element is unchanged. The right element now has a green (3) diagonal line inside it, mirroring the pattern from the left element. The green pixels replace the original white pixels at those locations.
*   **Example 2:**
    *   Input: Also contains two main visual elements separated by white pixels.
        *   Left element: A larger, irregular shape made of yellow (4) pixels, containing an anti-diagonal line of blue (1) pixels.
        *   Right element: A smaller solid rectangle made of red (2) pixels.
    *   Output: The overall structure is preserved. The left element is unchanged. The right element now has an anti-diagonal line of blue (1) pixels inside it, mirroring the pattern from the left element. The blue pixels replace the original red pixels at those locations.

**General Observations:**

1.  **Object Identification:** The grids contain distinct non-white objects, often separated by white space.
2.  **Pattern Source and Target:** There seem to be two primary objects involved. One acts as a 'source' containing an internal pattern (a different color), and the other acts as a 'target' where this pattern is copied or imprinted.
3.  **Pattern Extraction:** The pattern consists of pixels of a specific color located *within* the bounding box of the source object, but differing from the source object's main color.
4.  **Pattern Transfer:** The relative positions of the pattern pixels within the source object's bounding box are calculated. These relative positions are then applied to the target object's bounding box to determine where the pattern color should be placed in the output.
5.  **Imprinting:** The pattern color replaces the existing color at the target locations.
6.  **Preservation:** Pixels not part of the transferred pattern generally retain their original color from the input.

**YAML Facts:**


```yaml
task_description: Copy an internal color pattern from a source object to a target object based on relative positions within their bounding boxes.

definitions:
  - object: A connected component of non-white pixels.
  - bounding_box: The smallest rectangle enclosing all pixels of an object.
  - primary_color: The most frequent non-white color constituting an object's main structure (e.g., the frame color).
  - pattern_color: A color found within the bounding box of the source object that is different from its primary_color and also not white.
  - source_object: The object containing the pattern_color pixels within its bounding box.
  - target_object: The object onto which the pattern is copied.

actions:
  - identify_objects: Find all distinct non-white connected components.
  - determine_largest_objects: Select the two most prominent objects (e.g., by bounding box size or pixel count).
  - identify_source_target_pattern:
      - For each prominent object:
        - Check if its bounding box contains pixels of a color different from its primary color and white.
        - If yes, designate this object as 'source', the other prominent object as 'target', and the differing color as 'pattern_color'.
  - extract_pattern_relative_coords: Find all pixels of 'pattern_color' within the 'source_object's bounding box and calculate their coordinates relative to the top-left corner of this bounding box.
  - apply_pattern_to_target:
      - For each relative coordinate (dr, dc) from the source pattern:
        - Calculate the absolute coordinate (target_row, target_col) by adding (dr, dc) to the top-left coordinate of the 'target_object's bounding box.
        - If the calculated coordinate is within the grid bounds, update the pixel at (target_row, target_col) in the output grid to the 'pattern_color'.
  - copy_unchanged_pixels: Ensure all pixels not modified by the pattern transfer retain their original input color.

example_1:
  objects:
    - Magenta (6) frame object (source)
    - Orange (7) frame object (target)
  pattern_color: Green (3)
  source_pattern_relative_coords: [(0,1), (1,2), (2,3), (3,4), (4,5)] (relative to magenta box top-left)
  target_application: The green pattern is imprinted onto the orange object's area.

example_2:
  objects:
    - Yellow (4) shape object (source)
    - Red (2) rectangle object (target)
  pattern_color: Blue (1)
  source_pattern_relative_coords: [(0,4), (1,3), (2,2), (3,1), (4,0)] (relative to yellow box top-left)
  target_application: The blue anti-diagonal pattern is imprinted onto the red object's area.

```


**Natural Language Program:**

1.  **Initialize:** Create a copy of the input grid to serve as the output grid.
2.  **Identify Objects:** Find all connected components (objects) of non-white pixels in the input grid.
3.  **Select Main Objects:** Identify the two largest objects (e.g., by bounding box area). Label them Object A and Object B. If fewer than two objects exist, stop and return the copied input grid.
4.  **Find Source, Target, and Pattern:**
    a.  Determine the primary color and bounding box of Object A. Check if any pixels *within* Object A's bounding box have a color that is *not* white and *not* Object A's primary color. If such a pixel exists, designate Object A as the `source_object`, Object B as the `target_object`, and the color of this pixel as the `pattern_color`. Proceed to step 5.
    b.  If no pattern was found in Object A, perform the same check for Object B: Determine its primary color and bounding box. Check if any pixels *within* Object B's bounding box have a color that is *not* white and *not* Object B's primary color. If found, designate Object B as `source_object`, Object A as `target_object`, and this color as `pattern_color`. Proceed to step 5.
    c.  If neither object contains a pattern according to these rules, stop and return the copied input grid.
5.  **Extract Relative Pattern:**
    a.  Get the top-left coordinates (`source_r0`, `source_c0`) of the `source_object`'s bounding box.
    b.  Create a list of relative coordinates `pattern_coords`.
    c.  Iterate through all pixels (`r`, `c`) within the `source_object`'s bounding box.
    d.  If the pixel at (`r`, `c`) has the `pattern_color`, add its relative coordinates (`r - source_r0`, `c - source_c0`) to the `pattern_coords` list.
6.  **Apply Pattern to Target:**
    a.  Get the top-left coordinates (`target_r0`, `target_c0`) of the `target_object`'s bounding box.
    b.  For each relative coordinate (`dr`, `dc`) in `pattern_coords`:
        i.  Calculate the target absolute coordinates: `target_r = target_r0 + dr`, `target_c = target_c0 + dc`.
        ii. Check if `target_r` and `target_c` are valid coordinates within the dimensions of the output grid.
        iii. If the coordinates are valid, update the pixel at (`target_r`, `target_c`) in the output grid to the `pattern_color`.
7.  **Finalize:** Return the modified output grid.
```python
import numpy as np
from collections import Counter
from skimage.measure import label, regionprops

"""
Copies an internal color pattern from a source object to a target object based on relative positions within their bounding boxes.

1.  Identify all connected components (objects) of non-white pixels.
2.  Select the two largest objects based on pixel count.
3.  Determine which of these two is the 'source' (contains an internal pattern of a different color) and which is the 'target'. The pattern color is the color found inside the source's bounding box that differs from the source's primary color and isn't white.
4.  Calculate the relative coordinates of the pattern pixels within the source object's bounding box.
5.  Apply these relative coordinates to the target object's bounding box to determine the locations to imprint the pattern color onto the output grid.
6.  Pixels not part of the imprinted pattern retain their original colors.
"""

def find_objects(grid):
    """
    Finds connected components of non-white pixels using 8-way connectivity.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, each representing an object with keys:
              'pixels': list of (row, col) tuples.
              'bbox': (min_row, min_col, max_row, max_col).
              'primary_color': The most frequent non-white color in the object.
              'size': Number of pixels in the object.
    """
    labeled_grid = label(grid > 0, connectivity=2) # connectivity=2 means 8-way
    objects = []
    for region in regionprops(labeled_grid):
        pixels = tuple(map(tuple, region.coords.T)) # Convert coords to list of (r, c) tuples
        if not pixels:
            continue

        # Extract colors of the object pixels from the original grid
        obj_colors = [grid[r, c] for r, c in pixels]

        # Filter out potential background pixels if necessary (though label should handle this)
        non_white_colors = [c for c in obj_colors if c != 0]
        if not non_white_colors:
            continue # Skip if only white pixels somehow got included

        # Determine primary color (most frequent non-white)
        color_counts = Counter(non_white_colors)
        primary_color = color_counts.most_common(1)[0][0]

        objects.append({
            'pixels': list(pixels),
            'bbox': region.bbox, # (min_row, min_col, max_row, max_col)
            'primary_color': primary_color,
            'size': len(pixels)
        })
    # Sort objects by size (descending)
    objects.sort(key=lambda o: o['size'], reverse=True)
    return objects

def get_pixels_in_bbox(grid, bbox):
    """Gets all pixels within a bounding box."""
    min_r, min_c, max_r, max_c = bbox
    pixels = {}
    for r in range(min_r, max_r):
        for c in range(min_c, max_c):
            pixels[(r, c)] = grid[r, c]
    return pixels

def transform(input_grid):
    """
    Transforms the input grid by copying an internal pattern from a source
    object to a target object.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Objects
    objects = find_objects(input_grid)

    # 2. Select Main Objects (need at least two)
    if len(objects) < 2:
        return output_grid # Not enough objects to perform the transformation

    # For simplicity, assume the two largest objects are the source/target pair
    obj_a = objects[0]
    obj_b = objects[1]

    # 3. Find Source, Target, and Pattern
    source_object = None
    target_object = None
    pattern_color = None
    pattern_coords_relative = []

    # Check Object A as potential source
    bbox_a = obj_a['bbox']
    min_ra, min_ca, max_ra, max_ca = bbox_a
    primary_color_a = obj_a['primary_color']
    found_pattern_in_a = False
    temp_pattern_coords_a = []
    temp_pattern_color_a = -1 # Invalid color init

    for r in range(min_ra, max_ra):
        for c in range(min_ca, max_ca):
            color = input_grid[r, c]
            if color != 0 and color != primary_color_a:
                if not found_pattern_in_a: # First pattern pixel found
                    temp_pattern_color_a = color
                    found_pattern_in_a = True
                # Ensure all pattern pixels have the same color (assumption)
                if color == temp_pattern_color_a:
                    temp_pattern_coords_a.append((r - min_ra, c - min_ca))

    if found_pattern_in_a:
        source_object = obj_a
        target_object = obj_b
        pattern_color = temp_pattern_color_a
        pattern_coords_relative = temp_pattern_coords_a
    else:
        # Check Object B as potential source
        bbox_b = obj_b['bbox']
        min_rb, min_cb, max_rb, max_cb = bbox_b
        primary_color_b = obj_b['primary_color']
        found_pattern_in_b = False
        temp_pattern_coords_b = []
        temp_pattern_color_b = -1

        for r in range(min_rb, max_rb):
            for c in range(min_cb, max_cb):
                color = input_grid[r, c]
                if color != 0 and color != primary_color_b:
                    if not found_pattern_in_b:
                        temp_pattern_color_b = color
                        found_pattern_in_b = True
                    if color == temp_pattern_color_b:
                       temp_pattern_coords_b.append((r - min_rb, c - min_cb))

        if found_pattern_in_b:
            source_object = obj_b
            target_object = obj_a
            pattern_color = temp_pattern_color_b
            pattern_coords_relative = temp_pattern_coords_b

    # If no source/pattern found after checking both, return original
    if source_object is None or pattern_color is None:
        return output_grid

    # 4. Apply Pattern to Target
    target_bbox = target_object['bbox']
    min_rt, min_ct, _, _ = target_bbox # Only need top-left corner

    for dr, dc in pattern_coords_relative:
        target_r = min_rt + dr
        target_c = min_ct + dc

        # Check bounds before applying
        if 0 <= target_r < rows and 0 <= target_c < cols:
            output_grid[target_r, target_c] = pattern_color

    return output_grid
```
```python
import numpy as np
from collections import deque, Counter

"""
Identifies the two largest non-white objects in the input grid.
One object (source) contains an internal pattern composed of pixels of a single color different from the object's primary color and the background (white).
This pattern's relative position within the source object's bounding box is determined.
The pattern is then copied (imprinted) onto the second largest object (target) by applying the same relative coordinates to the target object's bounding box.
The pattern color replaces the existing color at the target locations. All other pixels remain unchanged.
"""

def _get_neighbors(r, c, rows, cols):
    """ Helper function to get valid 8-way neighbors within grid bounds. """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def _find_objects_bfs(grid):
    """ Finds connected components of non-white pixels using BFS. """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If it's a non-white pixel and not yet visited, start BFS
            if grid[r, c] != 0 and not visited[r, c]:
                obj_pixels = []
                obj_colors = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    curr_r, curr_c = q.popleft()
                    obj_pixels.append((curr_r, curr_c))
                    obj_colors.append(grid[curr_r, curr_c])

                    # Update bounding box coordinates
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)

                    # Explore neighbors
                    for nr, nc in _get_neighbors(curr_r, curr_c, rows, cols):
                        if grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if obj_pixels:
                    # Determine primary color (most frequent non-white)
                    color_counts = Counter(obj_colors)
                    primary_color = color_counts.most_common(1)[0][0]
                    
                    # Bounding box (inclusive max)
                    bbox = (min_r, min_c, max_r + 1, max_c + 1) # Use +1 for max to align with slicing/range

                    objects.append({
                        'pixels': obj_pixels,
                        'bbox': bbox,
                        'primary_color': primary_color,
                        'size': len(obj_pixels)
                    })

    # Sort objects by size (descending)
    objects.sort(key=lambda o: o['size'], reverse=True)
    return objects

def transform(input_grid):
    """
    Transforms the input grid by copying an internal pattern from a source
    object to a target object.
    """
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify all non-white objects
    objects = _find_objects_bfs(input_grid)

    # 2. Need at least two objects for the transformation
    if len(objects) < 2:
        return output_grid # No transformation possible

    # 3. Assume the two largest objects are the source/target pair
    obj_a = objects[0]
    obj_b = objects[1]

    # 4. Try to find the source, target, pattern color, and pattern relative coordinates
    source_object = None
    target_object = None
    pattern_color = None
    pattern_coords_relative = []

    # Function to check an object for a pattern
    def check_for_pattern(potential_source):
        bbox = potential_source['bbox']
        min_r, min_c, max_r, max_c = bbox
        primary_color = potential_source['primary_color']
        
        found_pattern = False
        potential_pattern_color = -1
        coords = []

        # Iterate through the bounding box of the potential source
        for r in range(min_r, max_r):
            for c in range(min_c, max_c):
                # Check bounds just in case bbox goes slightly out (shouldn't with BFS approach)
                if 0 <= r < rows and 0 <= c < cols:
                    color = input_grid[r, c]
                    # Look for a color that is not background (0) and not the object's primary color
                    if color != 0 and color != primary_color:
                        # If this is the first pattern pixel found, store its color
                        if not found_pattern:
                            potential_pattern_color = color
                            found_pattern = True
                        
                        # Ensure all pattern pixels have the same color (task assumption)
                        if color == potential_pattern_color:
                            # Store relative coordinates (relative to bbox top-left)
                            coords.append((r - min_r, c - min_c))
                        else:
                            # Found a different internal color - this object doesn't fit the simple pattern model
                            return False, -1, [] 
                            
        return found_pattern, potential_pattern_color, coords

    # Check Object A as potential source
    found_in_a, color_a, coords_a = check_for_pattern(obj_a)
    if found_in_a:
        source_object = obj_a
        target_object = obj_b
        pattern_color = color_a
        pattern_coords_relative = coords_a
    else:
        # Check Object B as potential source
        found_in_b, color_b, coords_b = check_for_pattern(obj_b)
        if found_in_b:
            source_object = obj_b
            target_object = obj_a
            pattern_color = color_b
            pattern_coords_relative = coords_b

    # 5. If no source/pattern was identified, return the original grid
    if source_object is None or pattern_color is None or not pattern_coords_relative:
        return output_grid

    # 6. Apply the pattern to the target object
    target_bbox = target_object['bbox']
    min_rt, min_ct, _, _ = target_bbox # Target top-left corner

    for dr, dc in pattern_coords_relative:
        # Calculate absolute coordinates in the target area
        target_r = min_rt + dr
        target_c = min_ct + dc

        # Check if the calculated coordinates are within the grid bounds
        if 0 <= target_r < rows and 0 <= target_c < cols:
            # Update the output grid with the pattern color at the target location
            output_grid[target_r, target_c] = pattern_color

    # 7. Return the modified grid
    return output_grid
```
```python
import numpy as np
from collections import deque, Counter
import math

"""
Identifies the two largest non-white objects in the input grid.
One object (source) contains an internal pattern composed of pixels of a single color different from the object's primary color and the background (white).
This pattern is then transferred to the second largest object (target).
The transfer is based on aligning the centers of the bounding boxes of the source and target objects.
The translation vector calculated from the center alignment is applied to the absolute coordinates of the source pattern pixels to determine their new locations in the output grid.
The pattern color replaces the existing color at these new target locations. All other pixels remain unchanged.
"""

def _get_neighbors(r, c, rows, cols):
    """ Helper function to get valid 8-way neighbors within grid bounds. """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def _find_objects_bfs(grid):
    """ Finds connected components of non-white pixels using BFS. """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If it's a non-white pixel and not yet visited, start BFS
            if grid[r, c] != 0 and not visited[r, c]:
                obj_pixels = []
                obj_colors = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c
                current_color = grid[r,c] # Color of the starting pixel of the component

                component_queue = deque([(r,c)]) # Use a separate queue for BFS within the same color component
                component_visited = set([(r,c)])

                while component_queue:
                    curr_r, curr_c = component_queue.popleft()

                    obj_pixels.append((curr_r, curr_c))
                    obj_colors.append(grid[curr_r, curr_c])

                    # Update bounding box coordinates
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)

                    # Explore neighbors
                    for nr, nc in _get_neighbors(curr_r, curr_c, rows, cols):
                        # Add to component queue only if it has the same color and not visited for this component
                        if grid[nr, nc] == current_color and (nr, nc) not in component_visited:
                            visited[nr, nc] = True # Mark globally visited
                            component_visited.add((nr, nc))
                            component_queue.append((nr, nc))
                        # Also mark neighbors of different non-zero colors as visited to prevent starting BFS from them later
                        elif grid[nr,nc] != 0 and not visited[nr,nc]:
                             visited[nr, nc] = True # Mark globally visited so we don't start BFS from here

                if obj_pixels:
                    # Determine primary color (most frequent non-white, should be the component color here)
                    color_counts = Counter(obj_colors)
                    primary_color = color_counts.most_common(1)[0][0]

                    # Bounding box (inclusive max for coords, +1 for range/slicing)
                    bbox = (min_r, min_c, max_r + 1, max_c + 1)

                    objects.append({
                        'pixels': obj_pixels,
                        'bbox': bbox,
                        'primary_color': primary_color,
                        'size': len(obj_pixels)
                    })

    # Sort objects by size (descending)
    objects.sort(key=lambda o: o['size'], reverse=True)
    return objects

def _calculate_bbox_center(bbox):
    """ Calculates the center of a bounding box. """
    min_r, min_c, max_r, max_c = bbox
    center_r = min_r + (max_r - min_r) / 2.0
    center_c = min_c + (max_c - min_c) / 2.0
    return center_r, center_c

def transform(input_grid):
    """
    Transforms the input grid by copying an internal pattern from a source
    object to a target object, aligning by bounding box centers.
    """
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify all non-white objects
    # Using skimage.measure.label for potentially better handling of complex shapes
    # Revert to BFS if skimage is not allowed or fails
    try:
        from skimage.measure import label, regionprops
        labeled_grid = label(input_grid > 0, connectivity=2) # 8-way connectivity
        regions = regionprops(labeled_grid, intensity_image=input_grid)
        objects = []
        for region in regions:
             pixels = tuple(map(tuple, region.coords.T))
             if not pixels: continue
             non_white_colors = [c for c in region.intensity_image[region.image].flatten() if c != 0]
             if not non_white_colors: continue
             primary_color = Counter(non_white_colors).most_common(1)[0][0]
             objects.append({
                 'pixels': list(pixels),
                 'bbox': region.bbox, # (min_r, min_c, max_r, max_c) - exclusive max
                 'primary_color': primary_color,
                 'size': region.area # region.area should be count of non-zero pixels
             })
        objects.sort(key=lambda o: o['size'], reverse=True)

    except ImportError:
        # Fallback to BFS if skimage is not available
        print("Warning: skimage not found, using BFS for object detection.")
        objects = _find_objects_bfs(input_grid)


    # 2. Need at least two objects for the transformation
    if len(objects) < 2:
        return output_grid # No transformation possible

    # 3. Assume the two largest objects are the source/target pair
    obj_a = objects[0]
    obj_b = objects[1]

    # 4. Try to find the source, target, pattern color, and pattern absolute coordinates
    source_object = None
    target_object = None
    pattern_color = None
    pattern_coords_absolute = [] # Store absolute coordinates

    # Function to check an object for a pattern and return absolute coords
    def check_for_pattern(potential_source):
        bbox = potential_source['bbox']
        min_r, min_c, max_r, max_c = bbox # Exclusive max convention from regionprops/BFS bbox format
        primary_color = potential_source['primary_color']

        found_pattern = False
        potential_pattern_color = -1
        abs_coords = []

        # Iterate through the bounding box of the potential source
        for r in range(min_r, max_r):
            for c in range(min_c, max_c):
                 # Check grid bounds rigorously
                if 0 <= r < rows and 0 <= c < cols:
                    color = input_grid[r, c]
                    # Look for a color that is not background (0) and not the object's primary color
                    if color != 0 and color != primary_color:
                        # If this is the first pattern pixel found, store its color
                        if not found_pattern:
                            potential_pattern_color = color
                            found_pattern = True

                        # Ensure all pattern pixels have the same color (task assumption)
                        if color == potential_pattern_color:
                            # Store absolute coordinates
                            abs_coords.append((r, c))
                        else:
                            # Found a different internal color - this object doesn't fit the simple pattern model
                            return False, -1, []

        return found_pattern, potential_pattern_color, abs_coords

    # Check Object A as potential source
    found_in_a, color_a, coords_a = check_for_pattern(obj_a)
    if found_in_a:
        source_object = obj_a
        target_object = obj_b
        pattern_color = color_a
        pattern_coords_absolute = coords_a
    else:
        # Check Object B as potential source
        found_in_b, color_b, coords_b = check_for_pattern(obj_b)
        if found_in_b:
            source_object = obj_b
            target_object = obj_a
            pattern_color = color_b
            pattern_coords_absolute = coords_b

    # 5. If no source/pattern was identified, return the original grid
    if source_object is None or pattern_color is None or not pattern_coords_absolute:
        return output_grid

    # 6. Calculate centers and translation vector
    source_bbox = source_object['bbox']
    target_bbox = target_object['bbox']

    source_center_r, source_center_c = _calculate_bbox_center(source_bbox)
    target_center_r, target_center_c = _calculate_bbox_center(target_bbox)

    delta_r = target_center_r - source_center_r
    delta_c = target_center_c - source_center_c

    # 7. Apply the translated pattern to the target object locations in the output grid
    for src_r, src_c in pattern_coords_absolute:
        # Calculate target coordinates by applying the translation vector
        # Round to nearest integer for pixel coordinates
        target_r = round(src_r + delta_r)
        target_c = round(src_c + delta_c)

        # Check if the calculated coordinates are within the grid bounds
        if 0 <= target_r < rows and 0 <= target_c < cols:
            # Update the output grid with the pattern color at the target location
            output_grid[target_r, target_c] = pattern_color

    # 8. Return the modified grid
    return output_grid
```

Previous Code:
```python
import numpy as np
from collections import deque, Counter
import math

"""
Identifies the two largest non-white objects in the input grid.
One object (source) contains an internal pattern composed of pixels of a single color different from the object's primary color and the background (white).
This pattern is then transferred to the second largest object (target).
The transfer is based on aligning the centers of the bounding boxes of the source and target objects.
The translation vector calculated from the center alignment is applied to the absolute coordinates of the source pattern pixels to determine their new locations in the output grid.
The pattern color replaces the existing color at these new target locations. All other pixels remain unchanged.
"""

def _get_neighbors(r, c, rows, cols):
    """ Helper function to get valid 8-way neighbors within grid bounds. """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def _find_objects_bfs(grid):
    """ Finds connected components of non-white pixels using BFS. """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If it's a non-white pixel and not yet visited, start BFS
            if grid[r, c] != 0 and not visited[r, c]:
                obj_pixels = []
                obj_colors = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c
                current_color = grid[r,c] # Color of the starting pixel of the component

                component_queue = deque([(r,c)]) # Use a separate queue for BFS within the same color component
                component_visited = set([(r,c)])

                while component_queue:
                    curr_r, curr_c = component_queue.popleft()

                    obj_pixels.append((curr_r, curr_c))
                    obj_colors.append(grid[curr_r, curr_c])

                    # Update bounding box coordinates
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)

                    # Explore neighbors
                    for nr, nc in _get_neighbors(curr_r, curr_c, rows, cols):
                        # Add to component queue only if it has the same color and not visited for this component
                        if grid[nr, nc] == current_color and (nr, nc) not in component_visited:
                            visited[nr, nc] = True # Mark globally visited
                            component_visited.add((nr, nc))
                            component_queue.append((nr, nc))
                        # Also mark neighbors of different non-zero colors as visited to prevent starting BFS from them later
                        elif grid[nr,nc] != 0 and not visited[nr,nc]:
                             visited[nr, nc] = True # Mark globally visited so we don't start BFS from here

                if obj_pixels:
                    # Determine primary color (most frequent non-white, should be the component color here)
                    color_counts = Counter(obj_colors)
                    primary_color = color_counts.most_common(1)[0][0]

                    # Bounding box (inclusive max for coords, +1 for range/slicing)
                    bbox = (min_r, min_c, max_r + 1, max_c + 1)

                    objects.append({
                        'pixels': obj_pixels,
                        'bbox': bbox,
                        'primary_color': primary_color,
                        'size': len(obj_pixels)
                    })

    # Sort objects by size (descending)
    objects.sort(key=lambda o: o['size'], reverse=True)
    return objects

def _calculate_bbox_center(bbox):
    """ Calculates the center of a bounding box. """
    min_r, min_c, max_r, max_c = bbox
    center_r = min_r + (max_r - min_r) / 2.0
    center_c = min_c + (max_c - min_c) / 2.0
    return center_r, center_c

def transform(input_grid):
    """
    Transforms the input grid by copying an internal pattern from a source
    object to a target object, aligning by bounding box centers.
    """
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify all non-white objects
    # Using skimage.measure.label for potentially better handling of complex shapes
    # Revert to BFS if skimage is not allowed or fails
    try:
        from skimage.measure import label, regionprops
        labeled_grid = label(input_grid > 0, connectivity=2) # 8-way connectivity
        regions = regionprops(labeled_grid, intensity_image=input_grid)
        objects = []
        for region in regions:
             pixels = tuple(map(tuple, region.coords.T))
             if not pixels: continue
             non_white_colors = [c for c in region.intensity_image[region.image].flatten() if c != 0]
             if not non_white_colors: continue
             primary_color = Counter(non_white_colors).most_common(1)[0][0]
             objects.append({
                 'pixels': list(pixels),
                 'bbox': region.bbox, # (min_r, min_c, max_r, max_c) - exclusive max
                 'primary_color': primary_color,
                 'size': region.area # region.area should be count of non-zero pixels
             })
        objects.sort(key=lambda o: o['size'], reverse=True)

    except ImportError:
        # Fallback to BFS if skimage is not available
        print("Warning: skimage not found, using BFS for object detection.")
        objects = _find_objects_bfs(input_grid)


    # 2. Need at least two objects for the transformation
    if len(objects) < 2:
        return output_grid # No transformation possible

    # 3. Assume the two largest objects are the source/target pair
    obj_a = objects[0]
    obj_b = objects[1]

    # 4. Try to find the source, target, pattern color, and pattern absolute coordinates
    source_object = None
    target_object = None
    pattern_color = None
    pattern_coords_absolute = [] # Store absolute coordinates

    # Function to check an object for a pattern and return absolute coords
    def check_for_pattern(potential_source):
        bbox = potential_source['bbox']
        min_r, min_c, max_r, max_c = bbox # Exclusive max convention from regionprops/BFS bbox format
        primary_color = potential_source['primary_color']

        found_pattern = False
        potential_pattern_color = -1
        abs_coords = []

        # Iterate through the bounding box of the potential source
        for r in range(min_r, max_r):
            for c in range(min_c, max_c):
                 # Check grid bounds rigorously
                if 0 <= r < rows and 0 <= c < cols:
                    color = input_grid[r, c]
                    # Look for a color that is not background (0) and not the object's primary color
                    if color != 0 and color != primary_color:
                        # If this is the first pattern pixel found, store its color
                        if not found_pattern:
                            potential_pattern_color = color
                            found_pattern = True

                        # Ensure all pattern pixels have the same color (task assumption)
                        if color == potential_pattern_color:
                            # Store absolute coordinates
                            abs_coords.append((r, c))
                        else:
                            # Found a different internal color - this object doesn't fit the simple pattern model
                            return False, -1, []

        return found_pattern, potential_pattern_color, abs_coords

    # Check Object A as potential source
    found_in_a, color_a, coords_a = check_for_pattern(obj_a)
    if found_in_a:
        source_object = obj_a
        target_object = obj_b
        pattern_color = color_a
        pattern_coords_absolute = coords_a
    else:
        # Check Object B as potential source
        found_in_b, color_b, coords_b = check_for_pattern(obj_b)
        if found_in_b:
            source_object = obj_b
            target_object = obj_a
            pattern_color = color_b
            pattern_coords_absolute = coords_b

    # 5. If no source/pattern was identified, return the original grid
    if source_object is None or pattern_color is None or not pattern_coords_absolute:
        return output_grid

    # 6. Calculate centers and translation vector
    source_bbox = source_object['bbox']
    target_bbox = target_object['bbox']

    source_center_r, source_center_c = _calculate_bbox_center(source_bbox)
    target_center_r, target_center_c = _calculate_bbox_center(target_bbox)

    delta_r = target_center_r - source_center_r
    delta_c = target_center_c - source_center_c

    # 7. Apply the translated pattern to the target object locations in the output grid
    for src_r, src_c in pattern_coords_absolute:
        # Calculate target coordinates by applying the translation vector
        # Round to nearest integer for pixel coordinates
        target_r = round(src_r + delta_r)
        target_c = round(src_c + delta_c)

        # Check if the calculated coordinates are within the grid bounds
        if 0 <= target_r < rows and 0 <= target_c < cols:
            # Update the output grid with the pattern color at the target location
            output_grid[target_r, target_c] = pattern_color

    # 8. Return the modified grid
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
6 3 6 6 6 6 0 7 7 7 7 7 7
6 0 3 0 0 6 0 7 0 0 0 0 7
6 0 0 3 0 6 0 7 0 0 0 0 7
6 0 0 0 3 6 0 7 0 0 0 0 7
6 0 0 0 0 3 0 7 0 0 0 0 7
6 6 6 6 6 6 0 7 7 7 7 7 7
```
Expected Output:
```
6 3 6 6 6 6 0 7 3 7 7 7 7
6 0 3 0 0 6 0 7 0 3 0 0 7
6 0 0 3 0 6 0 7 0 0 3 0 7
6 0 0 0 3 6 0 7 0 0 0 3 7
6 0 0 0 0 3 0 7 0 0 0 0 3
6 6 6 6 6 6 0 7 7 7 7 7 7
```
Transformed Output:
```
6 3 6 6 6 6 0 7 3 7 7 7 7
6 0 3 0 0 6 0 7 0 3 0 0 7
6 0 0 3 0 6 0 7 0 0 3 0 7
6 0 0 0 3 6 0 7 0 0 0 3 7
6 0 0 0 0 3 0 7 0 0 0 0 3
6 6 6 6 6 6 0 7 7 7 7 7 7
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 2:
Input:
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
Expected Output:
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
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
4 4 4 4 1 0 0 0 0 0
4 4 4 1 4 0 0 0 0 0
4 4 1 4 4 0 0 2 2 1
4 1 4 4 4 0 0 2 1 2
1 4 4 4 4 0 0 1 2 2
0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 1
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 2.0
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


*code_execution:*
```python
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

*code_execution_result:*
outcome: OUTCOME_FAILED
```
Traceback (most recent call last):
  File "<string>", line 3, in <module>
ModuleNotFoundError: No module named 'skimage'

```
**Revised Metrics Gathering (using fallback BFS)**
It seems `skimage` is unavailable. Rerunning analysis using the BFS object detection.


*code_execution:*
```python
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

*code_execution_result:*
outcome: OUTCOME_OK
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
