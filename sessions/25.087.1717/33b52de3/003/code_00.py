import numpy as np
from collections import deque

"""
Transformation Rule:

1.  **Identify Template Patterns:** Scan the input grid to find all occurrences of the specific template pattern: a 3x3 hollow square composed entirely of gray (5) pixels. Record the location (top-left corner) and pixels of each found template instance. If no templates are found, return the input grid unchanged.
2.  **Determine Template Grid Dimensions:** Analyze the top-left corner coordinates of the found template instances. Identify the unique row coordinates and unique column coordinates. The number of unique rows is the template grid height (`tr`), and the number of unique columns is the template grid width (`tc`). Create a mapping from template grid indices `(r_idx, c_idx)` (where `0 <= r_idx < tr`, `0 <= c_idx < tc`) to the corresponding template pattern instance based on its original top-left corner matching the sorted unique rows/cols.
3.  **Isolate Potential Key Pixels:** Create a temporary copy of the input grid. In this temporary grid, set the color of all pixels belonging to any identified template pattern instance to background (0).
4.  **Identify Key Pattern Object:** Find all distinct contiguous objects in the temporary grid consisting of any non-background color (i.e., colors 1-9). Gray pixels (5) should not form part of these objects as they were either part of templates (now 0) or potentially other gray structures which are ignored here.
5.  **Select the Key Pattern:** From the objects found in step 4, identify the *single* object whose bounding box height is exactly `tr` and whose bounding box width is exactly `tc`. If no such object or multiple such objects exist, return the input grid unchanged. Record the top-left corner `(key_r, key_c)` of this identified key pattern object's bounding box.
6.  **Prepare Output:** Create the output grid as a copy of the original input grid.
7.  **Apply Transformation:** Iterate through each template grid index `(r_idx, c_idx)` from `(0, 0)` up to `(tr-1, tc-1)`.
    a.  Retrieve the specific template pattern instance corresponding to `(r_idx, c_idx)` using the mapping created in step 2. If no template exists at this grid index, skip.
    b.  Get the replacement color from the *original input grid* at the location `(key_r + r_idx, key_c + c_idx)`.
    c.  For every pixel `(px_r, px_c)` that belongs to the current template pattern instance (which will have the color gray (5) in the output grid initially), update its color in the *output grid* to the replacement color obtained in step 7b.
8.  **Return Result:** Return the modified output grid.
"""

def find_contiguous_objects(grid, ignore_colors=None):
    """
    Finds all contiguous objects of non-ignored colors.

    Args:
        grid (np.ndarray): The input grid.
        ignore_colors (set): A set of colors to ignore (treat as background).
                             Defaults to {0} (background).

    Returns:
        list: A list of dictionaries, each representing an object with keys:
              'pixels' (set of (r, c) tuples),
              'bbox' (tuple: min_r, min_c, max_r, max_c),
              'height' (int),
              'width' (int),
              'colors' (set of colors in the object).
    """
    if ignore_colors is None:
        ignore_colors = {0} # Ignore background by default

    h, w = grid.shape
    visited = np.zeros((h, w), dtype=bool)
    objects = []

    for r in range(h):
        for c in range(w):
            color = grid[r, c]
            # Start BFS if pixel color is not ignored and not yet visited
            if color not in ignore_colors and not visited[r, c]:
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c
                colors_in_obj = {color}

                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < h and 0 <= nc < w and not visited[nr, nc]:
                             neighbor_color = grid[nr, nc]
                             # Add neighbor to queue if its color is not ignored
                             if neighbor_color not in ignore_colors:
                                visited[nr, nc] = True
                                colors_in_obj.add(neighbor_color)
                                q.append((nr, nc))

                # Completed finding an object, store its details
                bbox = (min_r, min_c, max_r, max_c)
                height = max_r - min_r + 1
                width = max_c - min_c + 1
                objects.append({
                    'pixels': obj_pixels,
                    'bbox': bbox,
                    'height': height,
                    'width': width,
                    'colors': colors_in_obj
                })
    return objects


def find_template_objects(grid):
    """
    Finds all 3x3 hollow gray square template objects in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, each representing a template object with keys:
              'pixels' (set of (r, c) tuples),
              'bbox' (tuple: min_r, min_c, max_r, max_c),
              'color' (int: always 5 for gray).
    """
    h, w = grid.shape
    visited = np.zeros((h, w), dtype=bool)
    template_objects = []
    gray = 5

    for r in range(h):
        for c in range(w):
            # Start BFS only if it's a gray pixel not yet assigned to an object
            if grid[r, c] == gray and not visited[r, c]:
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True # Mark start pixel as visited
                min_r, min_c = r, c
                max_r, max_c = r, c
                is_potential_template = True # Assume it might be a template initially

                component_q = deque([(r,c)]) # Queue for the current component's BFS

                while component_q:
                    row, col = component_q.popleft()

                    # If a non-gray pixel is connected, it's not a pure gray object
                    if grid[row,col] != gray:
                         is_potential_template = False
                         # We must continue BFS to mark all connected pixels as visited,
                         # even if it's not a template, to avoid starting new searches
                         # within this already explored connected component.

                    obj_pixels.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if neighbor is gray and not visited
                        if 0 <= nr < h and 0 <= nc < w and \
                           grid[nr, nc] == gray and not visited[nr, nc]:
                            visited[nr, nc] = True # Mark neighbor as visited
                            component_q.append((nr, nc)) # Add to BFS queue
                        # If a non-gray neighbor is found but not visited,
                        # we still need to visit it if we were continuing BFS
                        # for non-template components, but for templates,
                        # we only care about connected gray pixels. The is_potential_template
                        # flag handles cases where non-gray pixels were initially connected.

                # After BFS for the component is complete, check if it's a valid template
                if is_potential_template:
                    bbox_h = max_r - min_r + 1
                    bbox_w = max_c - min_c + 1

                    # Check if dimensions are 3x3
                    if bbox_h == 3 and bbox_w == 3:
                        # Check if it's exactly the hollow square pattern
                        expected_pixels = set()
                        for r_ in range(min_r, max_r + 1):
                            expected_pixels.add((r_, min_c))
                            expected_pixels.add((r_, max_c))
                        for c_ in range(min_c + 1, max_c):
                            expected_pixels.add((min_r, c_))
                            expected_pixels.add((max_r, c_))

                        # Compare the set of pixels found with the expected hollow square pixels
                        if obj_pixels == expected_pixels:
                            bbox = (min_r, min_c, max_r, max_c)
                            template_objects.append({'pixels': obj_pixels, 'bbox': bbox, 'color': gray})

    return template_objects


def transform(input_grid_list):
    """
    Applies the transformation rule: replaces pixels in template patterns
    using colors from a key pattern based on relative grid positions.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    output_grid = np.copy(input_grid)
    h, w = input_grid.shape

    # 1. Identify Template Patterns
    template_instances = find_template_objects(input_grid)

    if not template_instances:
        # No templates found, return original grid
        return output_grid.tolist()

    # 2. Determine Template Grid Dimensions
    # Get top-left corners and sort them to find unique rows/cols
    corners = sorted([(obj['bbox'][0], obj['bbox'][1], obj) for obj in template_instances])
    template_rows = sorted(list(set(c[0] for c in corners)))
    template_cols = sorted(list(set(c[1] for c in corners)))
    tr = len(template_rows) # template grid height
    tc = len(template_cols) # template grid width

    # Create a mapping from template grid index (r_idx, c_idx) to the actual object
    template_map = {}
    corner_to_obj = {(c[0], c[1]): c[2] for c in corners}
    row_map = {row_val: r_idx for r_idx, row_val in enumerate(template_rows)}
    col_map = {col_val: c_idx for c_idx, col_val in enumerate(template_cols)}

    for r_val, c_val, obj in corners:
        r_idx = row_map[r_val]
        c_idx = col_map[c_val]
        template_map[(r_idx, c_idx)] = obj


    # 3. Isolate Potential Key Pixels
    temp_grid = np.copy(input_grid)
    all_template_pixels = set().union(*(t['pixels'] for t in template_instances))
    for r_px, c_px in all_template_pixels:
        temp_grid[r_px, c_px] = 0 # Mark template pixels as background

    # 4. Identify Key Pattern Object
    # Find contiguous objects ignoring background (0) and original gray (5)
    # We ignore gray (5) here because any relevant gray pixels were part of templates and are now 0.
    # Other stray gray pixels should not be part of the key.
    potential_keys = find_contiguous_objects(temp_grid, ignore_colors={0, 5})

    # 5. Select the Key Pattern
    matched_key = None
    key_r, key_c = -1, -1
    found_match = False
    for key_candidate in potential_keys:
        # Check if the candidate's bounding box dimensions match the template grid dimensions
        if key_candidate['height'] == tr and key_candidate['width'] == tc:
            # Check if we already found a match (should only be one)
            if found_match:
                # Ambiguous: multiple potential keys match dimensions. Return original.
                # print("Warning: Multiple key patterns match template grid dimensions.")
                return input_grid_list # Return original grid on ambiguity/error

            matched_key = key_candidate
            key_r, key_c, _, _ = matched_key['bbox']
            found_match = True
            # Don't break yet, continue loop to check for ambiguity.

    if not found_match:
        # No key pattern found matching the template grid dimensions
        # print("Warning: No key pattern found matching template grid dimensions.")
        return input_grid_list # Return original grid if no key found

    # 6. Prepare Output (already done with output_grid = np.copy(input_grid))

    # 7. Apply Transformation
    for r_idx in range(tr):
        for c_idx in range(tc):
            # 7a. Retrieve the template instance for this grid position
            if (r_idx, c_idx) in template_map:
                template_obj = template_map[(r_idx, c_idx)]

                # 7b. Get replacement color from the *original* grid using key's top-left and relative index
                replacement_color = input_grid[key_r + r_idx, key_c + c_idx]

                # 7c. Replace pixels in the output grid
                for (px_r, px_c) in template_obj['pixels']:
                    # Ensure we only replace original gray pixels
                    if input_grid[px_r, px_c] == 5:
                        output_grid[px_r, px_c] = replacement_color
            # else: Handle case where template grid might be incomplete (optional, based on ARC task constraints)

    # 8. Return Result
    return output_grid.tolist()