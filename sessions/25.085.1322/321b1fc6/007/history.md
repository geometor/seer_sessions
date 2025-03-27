
Previous Code:
```python
"""
1. Initialize an output grid of the same dimensions as the input grid, filled entirely with the background color (white, 0).
2. Identify all distinct connected groups of azure (8) pixels in the input grid. These are the 'markers'. If no markers are found, return the initial white output grid.
3. Identify all distinct connected groups of pixels whose color is *not* white (0) and *not* azure (8). These are the 'source components'.
4. If no source components are found, return the initial white output grid.
5. Determine the single 'template pattern':
    a. Find the source component whose top-left corner coordinate has the minimum row index.
    b. If multiple source components share the minimum row index, select the one among them with the minimum column index. This is the 'primary source component'.
    c. Extract the shape of this primary source component within its own bounding box (treating pixels outside the component but within the box as background/white 0). This extracted shape is the 'template pattern'.
6. For each identified marker:
    a. Determine the coordinate (row, column) of its top-leftmost pixel.
    b. Copy ('stamp') the determined 'template pattern' onto the output grid, aligning the template's top-left corner with the marker's top-left coordinate.
    c. Ensure the template pattern is clipped if it extends beyond the output grid's boundaries during stamping. Pixels from the template overwrite the corresponding pixels in the output grid.
7. Return the final modified output grid.
"""

import numpy as np
from collections import deque

# Helper function to find connected components without scipy
def find_connected_components_no_scipy(grid, target_colors=None):
    """
    Finds all connected components for specified colors or all non-background colors
    using BFS, without relying on scipy.

    Args:
        grid (np.array): The input grid.
        target_colors (list or set, optional): A collection of integer colors
            to find objects for. If None, finds objects for all colors except 0.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color', 'pixels' (list of (r, c) tuples),
              'bbox' (tuple: (min_r, min_c, max_r, max_c)), 'top_left' (r, c).
              Returns empty list if no objects found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    if target_colors is None:
        colors_present = np.unique(grid)
        target_colors = [c for c in colors_present if c != 0]
    if not target_colors:
        return objects

    target_colors_set = set(target_colors) # Faster lookup

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color in target_colors_set and not visited[r, c]:
                # Start BFS for a new component
                component_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    component_pixels.append((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            # Check bounds, color match, and visited status
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))

                if component_pixels:
                    objects.append({
                        'color': color,
                        'pixels': component_pixels,
                        'bbox': (min_r, min_c, max_r, max_c),
                        'top_left': (min_r, min_c)
                    })

    # Sort objects primarily by top-left row, then column for consistent ordering
    objects.sort(key=lambda o: (o['top_left'][0], o['top_left'][1]))
    return objects

# Helper function to get the relative pattern of a component
def get_relative_pattern(component):
    """
    Extracts the relative pattern of a component within its bounding box.
    """
    color = component['color']
    pixels = component['pixels']
    min_r, min_c, max_r, max_c = component['bbox']
    
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    relative_pattern = np.zeros((height, width), dtype=int) # Use int type

    for r, c in pixels:
        relative_pattern[r - min_r, c - min_c] = color

    return relative_pattern

# Helper function to stamp a pattern onto the grid
def stamp_pattern(output_grid, pattern, top_left_coord):
    """
    Overlays the pattern onto the output grid at the specified coordinate,
    handling clipping.
    """
    r_start, c_start = top_left_coord
    p_h, p_w = pattern.shape
    g_h, g_w = output_grid.shape

    # Calculate the intersection bounds for stamping
    r_end = min(r_start + p_h, g_h)
    c_end = min(c_start + p_w, g_w)

    # Adjust start coordinates if they are negative (shouldn't happen with valid markers, but defensive)
    p_r_offset = 0
    p_c_offset = 0
    if r_start < 0:
        p_r_offset = -r_start
        r_start = 0
    if c_start < 0:
        p_c_offset = -c_start
        c_start = 0
        
    # Calculate slices for pattern and grid based on intersection and potential negative offset
    p_r_slice = slice(p_r_offset, p_r_offset + (r_end - r_start))
    p_c_slice = slice(p_c_offset, p_c_offset + (c_end - c_start))
    g_r_slice = slice(r_start, r_end)
    g_c_slice = slice(c_start, c_end)
    
    # Ensure slices are valid (have positive range) before attempting assignment
    # Also check if the calculated pattern slice dimensions match the grid slice dimensions
    if g_r_slice.start < g_r_slice.stop and g_c_slice.start < g_c_slice.stop and \
       (p_r_slice.stop - p_r_slice.start) == (g_r_slice.stop - g_r_slice.start) and \
       (p_c_slice.stop - p_c_slice.start) == (g_c_slice.stop - g_c_slice.start):
       
        # Create a mask for non-zero pixels in the pattern slice
        pattern_slice = pattern[p_r_slice, p_c_slice]
        mask = pattern_slice != 0 
        
        # Apply the pattern slice to the output grid using the mask
        output_grid[g_r_slice, g_c_slice][mask] = pattern_slice[mask]


def transform(input_grid):
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape

    # 1. Initialize output_grid
    output_grid = np.zeros_like(input_grid_np) # Filled with white (0)

    # 2. Find marker objects (color 8)
    marker_color = 8
    marker_objects = find_connected_components_no_scipy(input_grid_np, target_colors=[marker_color])

    # If no markers, return the initial white grid
    if not marker_objects:
        return output_grid.tolist()

    # 3. Find source objects (all colors except 0 and 8)
    all_colors = np.unique(input_grid_np)
    source_colors = [c for c in all_colors if c != 0 and c != marker_color]
    source_objects = find_connected_components_no_scipy(input_grid_np, target_colors=source_colors)

    # 4. If no source objects, return the initial white grid
    if not source_objects:
        return output_grid.tolist()

    # 5. Determine the template pattern
    # Objects are already sorted by top-left row, then column by find_connected_components
    primary_source_component = source_objects[0]
    template = get_relative_pattern(primary_source_component)

    # 6. Stamp the template for each marker
    for marker in marker_objects:
        marker_tl = marker['top_left']
        stamp_pattern(output_grid, template, marker_tl)

    # 7. Return the final grid as a list of lists
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0
0 8 8 8 0 0 8 8 0 0
0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 6 6 6 0 0
0 0 0 8 8 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0
0 6 6 6 0 0 7 7 0 0
0 0 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 0 0 0 0 0
0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 9
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 18.0

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 7 6 0 0 0 0 0 0 0
0 9 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0
0 0 8 8 0 0 0 0 8 8
0 0 0 0 0 0 0 0 8 8
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 6 0 0 0
0 0 0 0 0 9 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 6 0 0 0 0 0 0
0 0 9 4 0 0 0 0 7 6
0 0 0 0 0 0 0 0 9 4
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 9
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 18.0
**General Assessment**

The provided code attempted to solve the task by identifying a single "template" pattern (the top-leftmost non-background, non-marker object) and "stamping" it onto the output grid at locations indicated by azure (8) markers.

The results show this approach failed on both examples. The actual transformed output only contained parts of the expected output. Comparing the input, expected output, and actual output reveals that the core issue lies in the definition of the "template". Instead of a single object, the template seems to be a composite pattern derived from *all* non-background, non-marker objects present in the input, maintaining their relative spatial arrangement.

The strategy needs to be revised to:
1.  Identify all source objects (colors other than white 0 and azure 8).
2.  Determine the bounding box that encompasses *all* these source objects.
3.  Create the template pattern by extracting all source pixels within this combined bounding box, preserving their colors and relative positions. Pixels within the box that are not part of any source object should be treated as background (white 0) in the template.
4.  Identify all azure (8) marker objects.
5.  For each marker object, use its top-left coordinate as the anchor point to stamp the composite template onto the output grid.

**Metrics and Analysis**


*code_execution:*
```python
import numpy as np
from collections import deque

# Reusing the helper function from the previous code
def find_connected_components_no_scipy(grid, target_colors=None):
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    if target_colors is None:
        colors_present = np.unique(grid)
        target_colors = [c for c in colors_present if c != 0]
    if not target_colors:
        return objects
    target_colors_set = set(target_colors)
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color in target_colors_set and not visited[r, c]:
                component_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c, max_r, max_c = r, c
                while q:
                    row, col = q.popleft()
                    component_pixels.append((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                if component_pixels:
                    objects.append({
                        'color': color, 'pixels': component_pixels,
                        'bbox': (min_r, min_c, max_r, max_c),
                        'top_left': (min_r, min_c)
                    })
    # Sort objects primarily by top-left row, then column
    objects.sort(key=lambda o: (o['top_left'][0], o['top_left'][1]))
    return objects

# Define the inputs
input1 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 8, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 8, 8, 0, 0, 8, 8, 0, 0],
    [0, 0, 0, 0, 0, 0, 8, 8, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 7, 7, 0, 0, 0],
    [0, 0, 0, 0, 0, 6, 6, 6, 0, 0],
    [0, 0, 0, 8, 8, 0, 0, 0, 0, 0],
    [0, 0, 0, 8, 8, 8, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

input2 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 7, 6, 0, 0, 0, 0, 0, 0, 0],
    [0, 9, 4, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 8, 8, 0, 0, 0],
    [0, 0, 0, 0, 0, 8, 8, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 8, 8, 0, 0, 0, 0, 0, 0],
    [0, 0, 8, 8, 0, 0, 0, 0, 8, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 8, 8]
])

# --- Analysis Function ---
def analyze_example(input_grid, example_name):
    print(f"\n--- {example_name} Analysis ---")
    marker_color = 8
    all_colors = np.unique(input_grid)
    source_colors = [c for c in all_colors if c != 0 and c != marker_color]
    markers = find_connected_components_no_scipy(input_grid, target_colors=[marker_color])
    sources = find_connected_components_no_scipy(input_grid, target_colors=source_colors)

    print(f"Source Colors: {source_colors}")
    print(f"Number of Source Objects (by color block): {len(sources)}")
    if not sources:
        print("No source objects found.")
        return

    # Calculate combined bounding box for sources
    min_r = min(s['bbox'][0] for s in sources)
    min_c = min(s['bbox'][1] for s in sources)
    max_r = max(s['bbox'][2] for s in sources)
    max_c = max(s['bbox'][3] for s in sources)
    combined_bbox = (min_r, min_c, max_r, max_c)
    print(f"Combined Source BBox: {combined_bbox}")

    # Extract combined template
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    template = np.zeros((height, width), dtype=int)
    source_pixels_coords = set()
    for src in sources:
        for r, c in src['pixels']:
            source_pixels_coords.add((r, c))

    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if (r, c) in source_pixels_coords:
                template[r - min_r, c - min_c] = input_grid[r, c]
            # else: template remains 0 (background)

    print("Combined Template Pattern:")
    print(template)

    print(f"Number of Marker Objects: {len(markers)}")
    marker_tls = [mrk['top_left'] for mrk in markers]
    print(f"Marker Top-Left Coords: {marker_tls}")


# --- Run Analysis ---
analyze_example(input1, "Example 1")
analyze_example(input2, "Example 2")
```

*code_execution_result:*
outcome: OUTCOME_OK
```

--- Example 1 Analysis ---

```

*code_execution_result:*
outcome: OUTCOME_FAILED
```
Traceback (most recent call last):
  File "<string>", line 122, in <module>
  File "<string>", line 81, in analyze_example
  File "<string>", line 22, in find_connected_components_no_scipy
ValueError: not enough values to unpack (expected 4, got 2)

```
**Revised Metrics and Analysis**

It seems the `find_connected_components_no_scipy` function had an issue when called with `target_colors=[8]` if only one marker object existed (the sorting key was accessing multiple elements). Let's fix the tool code and rerun. The key issue was likely the sorting key `key=lambda o: (o['top_left'][0], o['top_left'][1])` applied to potentially empty or single-element lists if no objects of a certain type were found. A safer sort or conditional sorting is needed. Also, the template extraction logic needs adjustment. It should iterate through *all* source objects and place their pixels relative to the combined bounding box's top-left corner.

**Corrected Tool Code:**


*code_execution:*
```python
import numpy as np
from collections import deque

# Corrected helper function
def find_connected_components_no_scipy(grid, target_colors=None):
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    valid_target_colors = set()
    if target_colors is None:
        present_colors = np.unique(grid)
        valid_target_colors = {c for c in present_colors if c != 0}
    else:
        valid_target_colors = set(target_colors)

    if not valid_target_colors:
        return objects # Return empty list if no valid colors to search for

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color in valid_target_colors and not visited[r, c]:
                component_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    component_pixels.append((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check 8 neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))

                if component_pixels:
                    objects.append({
                        'color': color,
                        'pixels': component_pixels,
                        'bbox': (min_r, min_c, max_r, max_c),
                        'top_left': (min_r, min_c)
                    })

    # Sort objects only if there are objects to sort
    if objects:
        objects.sort(key=lambda o: (o['top_left'][0], o['top_left'][1]))
    return objects


# Define the inputs
input1 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 8, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 8, 8, 0, 0, 8, 8, 0, 0],
    [0, 0, 0, 0, 0, 0, 8, 8, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 7, 7, 0, 0, 0],
    [0, 0, 0, 0, 0, 6, 6, 6, 0, 0],
    [0, 0, 0, 8, 8, 0, 0, 0, 0, 0],
    [0, 0, 0, 8, 8, 8, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

input2 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 7, 6, 0, 0, 0, 0, 0, 0, 0],
    [0, 9, 4, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 8, 8, 0, 0, 0],
    [0, 0, 0, 0, 0, 8, 8, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 8, 8, 0, 0, 0, 0, 0, 0],
    [0, 0, 8, 8, 0, 0, 0, 0, 8, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 8, 8]
])

# --- Corrected Analysis Function ---
def analyze_example(input_grid, example_name):
    print(f"\n--- {example_name} Analysis ---")
    marker_color = 8
    all_colors = np.unique(input_grid)
    # Ensure 0 and marker_color are filtered out properly
    source_colors = [c for c in all_colors if c != 0 and c != marker_color]
    print(f"Identified Source Colors: {source_colors}")
    
    markers = find_connected_components_no_scipy(input_grid, target_colors=[marker_color])
    sources = find_connected_components_no_scipy(input_grid, target_colors=source_colors) # Pass list here

    print(f"Number of Source Objects (by contiguous color block): {len(sources)}")
    if not sources:
        print("No source objects found.")
        template = np.array([[]]) # Handle case with no sources
        combined_bbox = None
    else:
        for i, src in enumerate(sources):
             print(f"  Source {i+1}: Color={src['color']}, TopLeft={src['top_left']}, BBox={src['bbox']}")
        # Calculate combined bounding box for sources
        min_r = min(s['bbox'][0] for s in sources)
        min_c = min(s['bbox'][1] for s in sources)
        max_r = max(s['bbox'][2] for s in sources)
        max_c = max(s['bbox'][3] for s in sources)
        combined_bbox = (min_r, min_c, max_r, max_c)
        print(f"Combined Source BBox: {combined_bbox}")

        # Extract combined template
        height = max_r - min_r + 1
        width = max_c - min_c + 1
        template = np.zeros((height, width), dtype=int)
        # Iterate through *all* source objects found
        for src in sources:
            color = src['color']
            # Iterate through pixels of *this* source object
            for r, c in src['pixels']:
                 # Check if pixel is within combined bbox (should always be true by definition)
                 if min_r <= r <= max_r and min_c <= c <= max_c:
                     # Place pixel in template relative to combined bbox top-left
                     template[r - min_r, c - min_c] = color
        print("Combined Template Pattern:")
        print(template)

    print(f"Number of Marker Objects: {len(markers)}")
    if not markers:
        print("No marker objects found.")
        marker_tls = []
    else:
        marker_tls = [mrk['top_left'] for mrk in markers]
        print(f"Marker Top-Left Coords: {marker_tls}")
        for i, mrk in enumerate(markers):
             print(f"  Marker {i+1}: TopLeft={mrk['top_left']}")


# --- Run Analysis ---
analyze_example(input1, "Example 1")
analyze_example(input2, "Example 2")
```

*code_execution_result:*
outcome: OUTCOME_OK
```

--- Example 1 Analysis ---
Identified Source Colors: [np.int64(6), np.int64(7)]
Number of Source Objects (by contiguous color block): 2
  Source 1: Color=7, TopLeft=(5, 5), BBox=(5, 5, 5, 6)
  Source 2: Color=6, TopLeft=(6, 5), BBox=(6, 5, 6, 7)
Combined Source BBox: (5, 5, 6, 7)
Combined Template Pattern:
[[7 7 0]
 [6 6 6]]
Number of Marker Objects: 3
Marker Top-Left Coords: [(1, 1), (2, 6), (7, 3)]
  Marker 1: TopLeft=(1, 1)
  Marker 2: TopLeft=(2, 6)
  Marker 3: TopLeft=(7, 3)

--- Example 2 Analysis ---
Identified Source Colors: [np.int64(4), np.int64(6), np.int64(7), np.int64(9)]
Number of Source Objects (by contiguous color block): 4
  Source 1: Color=7, TopLeft=(1, 1), BBox=(1, 1, 1, 1)
  Source 2: Color=6, TopLeft=(1, 2), BBox=(1, 2, 1, 2)
  Source 3: Color=9, TopLeft=(2, 1), BBox=(2, 1, 2, 1)
  Source 4: Color=4, TopLeft=(2, 2), BBox=(2, 2, 2, 2)
Combined Source BBox: (1, 1, 2, 2)
Combined Template Pattern:
[[7 6]
 [9 4]]
Number of Marker Objects: 3
Marker Top-Left Coords: [(4, 5), (7, 2), (8, 8)]
  Marker 1: TopLeft=(4, 5)
  Marker 2: TopLeft=(7, 2)
  Marker 3: TopLeft=(8, 8)

```
**Facts (YAML)**


```yaml
task_description: Stamp a composite pattern derived from source objects onto locations marked by azure pixels.

definitions:
  - background_color: white (0)
  - marker_color: azure (8)
  - source_colors: Any color that is not white (0) and not azure (8).
  - source_object: A contiguous group of pixels of the same source_color. Note that adjacent pixels of different source colors form separate source objects initially.
  - marker_object: A contiguous group of pixels of the marker_color (azure, 8).
  - composite_template: A rectangular pattern derived from all source_objects.
  - stamp_location: The top-left coordinate of a marker_object.

rules:
  - rule: Identify all source_objects in the input grid.
  - rule: Identify all marker_objects in the input grid.
  - rule: If no source_objects exist OR no marker_objects exist, the output grid is entirely background_color.
  - rule: Determine the combined bounding box enclosing all pixels belonging to any source_object.
  - rule: Create the composite_template by taking the grid slice defined by the combined bounding box and replacing any pixel that is not part of a source_object with the background_color (white 0). Retain the original colors and relative positions of all source_object pixels within the template.
  - rule: Initialize an output grid of the same dimensions as the input grid, filled with the background_color.
  - rule: For each marker_object, determine its top-left coordinate (stamp_location).
  - rule: Copy ('stamp') the composite_template onto the output grid, aligning the template's top-left corner with the stamp_location. Pixels from the template overwrite the background in the output grid. Ensure clipping if the template extends beyond the output grid boundaries.

example_1_analysis:
  - source_objects:
      - color: orange (7), top_left: (5, 5)
      - color: magenta (6), top_left: (6, 5)
  - combined_source_bbox: (5, 5, 6, 7) # min_r, min_c, max_r, max_c
  - composite_template:
      - [7, 7, 0]
      - [6, 6, 6]
  - marker_objects:
      - top_left: (1, 1)
      - top_left: (2, 6)
      - top_left: (7, 3)
  - action: Stamp the 2x3 composite_template at each marker's top_left coordinate.

example_2_analysis:
  - source_objects: # Note: find_components treats these as 4 separate objects
      - color: orange (7), top_left: (1, 1)
      - color: magenta (6), top_left: (1, 2)
      - color: maroon (9), top_left: (2, 1)
      - color: yellow (4), top_left: (2, 2)
  - combined_source_bbox: (1, 1, 2, 2) # min_r, min_c, max_r, max_c
  - composite_template:
      - [7, 6]
      - [9, 4]
  - marker_objects:
      - top_left: (4, 5)
      - top_left: (7, 2)
      - top_left: (8, 8)
  - action: Stamp the 2x2 composite_template at each marker's top_left coordinate.

```


**Natural Language Program**

1.  Initialize an empty output grid with the same dimensions as the input grid, filled with the background color (white, 0).
2.  Identify all pixels in the input grid whose color is *not* white (0) and *not* azure (8). These are the 'source pixels'.
3.  If no source pixels are found, return the initial empty output grid.
4.  Determine the minimum bounding box that encloses *all* identified source pixels. Find the minimum row (`min_r`), minimum column (`min_c`), maximum row (`max_r`), and maximum column (`max_c`) among all source pixels.
5.  Create the 'composite template' pattern:
    a.  Create a new grid (the template) with height `max_r - min_r + 1` and width `max_c - min_c + 1`, initially filled with the background color (white, 0).
    b.  Iterate through all the original source pixels identified in step 2. For each source pixel at coordinate (`r`, `c`) with color `col`, set the pixel at `(r - min_r, c - min_c)` in the template grid to `col`.
6.  Identify all distinct connected groups of azure (8) pixels in the input grid. These are the 'markers'.
7.  If no markers are found, return the initial empty output grid.
8.  For each identified marker:
    a.  Determine the coordinate (row, column) of its top-leftmost pixel. This is the 'stamp location'.
    b.  Copy ('stamp') the 'composite template' onto the output grid, aligning the template's top-left corner with the 'stamp location'.
    c.  Pixels from the template (other than the background color 0) overwrite the corresponding pixels in the output grid. Ensure the template is clipped if it extends beyond the output grid's boundaries.
9.  Return the final modified output grid.
