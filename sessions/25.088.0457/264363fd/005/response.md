```python
import numpy as np
from collections import Counter, deque

"""
Transformation Rule (Hypothesized - Requires Validation with Examples):

1.  **Identify Background:** Determine the background color, typically the most frequent color or color 0, possibly confirmed by checking grid borders.
2.  **Find Objects:** Locate all contiguous regions of non-background colors using orthogonal connectivity.
3.  **Categorize Objects (Tentative):** If multiple objects exist, heuristically separate them. Assume the largest object is the 'main canvas'. Assume smaller objects are potential 'key' or 'reference' patterns. This distinction needs validation.
4.  **Identify Key Pattern (Tentative):** Search within the 'key' objects for a simple, predefined pattern. A common pattern in ARC is adjacency. Look for two different non-background colors orthogonally adjacent to each other within the same key object. Record these two colors (e.g., `color1`, `color2`) and the ID of the key object containing this pattern. Use the first valid pattern found. This pattern identification needs validation.
5.  **Identify Transformation Parameters (Tentative):**
    *   Assume the `main canvas` object has a dominant color (`main_color`).
    *   Based on the key pattern (`color1`, `color2`), assume one color acts as a 'marker' (`marker_color = color1`) and the other as the 'target' (`target_color = color2`). This assignment might need swapping or refinement based on examples.
    *   Check if the `marker_color` exists anywhere within the `main canvas` object.
6.  **Apply Transformation - Paint Rows/Columns (Tentative):**
    *   If the `marker_color` is found within the `main canvas`:
        *   Find all locations (r, c) of the `marker_color` within the `main canvas` object.
        *   Collect the set of unique row indices (`marker_rows`) and column indices (`marker_cols`) from these locations.
        *   Iterate through the output grid. For any pixel (r, c) whose original color was the `main_color`, if its row `r` is in `marker_rows` OR its column `c` is in `marker_cols`, change its color to the `target_color`. This painting logic needs validation.
7.  **Clean Up (Tentative):** Remove the 'key' object that contained the identified pattern by replacing its pixels in the output grid with the background color. This cleanup step needs validation.
8.  **Return:** Return the modified grid. If no key pattern or main object is found matching the criteria, return a copy of the input grid.

**Note:** This program is based on hypotheses derived from previous attempts and common ARC patterns. The categorization of objects, the specific key pattern, the roles of colors from the key, the painting logic, and the cleanup step are all tentative and require validation against the specific task examples. The previous version timed out, suggesting the logic (especially around detailed marker finding and object interactions) might be overly complex or incorrect. This version simplifies some steps but retains the overall structure.
"""

# Imports
import numpy as np
from collections import Counter, deque

# Helper Functions
def get_background_color(grid):
    """Determines the background color (most frequent, often 0)."""
    if grid.size == 0:
        return 0
    counts = Counter(grid.flatten())
    # Check border pixels as a heuristic reinforcement
    rows, cols = grid.shape
    border_pixels = []
    if rows > 0:
        border_pixels.extend(grid[0, :])  # Top row
        border_pixels.extend(grid[-1, :]) # Bottom row
    if cols > 0:
        border_pixels.extend(grid[:, 0])  # Left col
        border_pixels.extend(grid[:, -1]) # Right col

    if not counts:
        return 0

    most_common = counts.most_common()
    candidate = most_common[0][0]

    # If border pixels are mostly one color, prefer that as background
    if border_pixels:
        border_counts = Counter(border_pixels)
        border_candidate, border_count = border_counts.most_common(1)[0]
        # Check if this border candidate is significantly present
        if border_count > len(border_pixels) / 2:
             # Check if it's also the overall most common or close to it
             if border_candidate == candidate or border_counts[border_candidate] >= counts[candidate] * 0.8:
                  return border_candidate

    # Default to most frequent if border check isn't decisive
    # Tie-breaking: prefer lower color index if counts are equal
    if len(most_common) > 1 and most_common[0][1] == most_common[1][1]:
         if most_common[0][0] > most_common[1][0]:
             return most_common[1][0]
    return candidate

def find_objects_bfs(grid, ignore_color):
    """Finds connected components (objects) using BFS, ignoring a specified color."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    object_id_counter = 1
    labeled_grid = np.zeros_like(grid, dtype=int) # Grid showing which object ID each pixel belongs to

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != ignore_color:
                obj_coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                component_colors = Counter()
                current_object_id = object_id_counter

                while q:
                    row, col = q.popleft()
                    pixel_color = grid[row, col]

                    # Check if the pixel belongs to the object (not background)
                    # This check prevents adding background pixels inadvertently included during BFS expansion
                    # if a non-background pixel touches a background pixel.
                    if grid[row, col] != ignore_color:
                        obj_coords.append((row, col))
                        labeled_grid[row, col] = current_object_id
                        component_colors[pixel_color] += 1

                        # Explore neighbors (orthogonal)
                        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               not visited[nr, nc] and grid[nr, nc] != ignore_color:
                                # Only add valid neighbors to queue and mark visited
                                visited[nr, nc] = True
                                q.append((nr, nc))
                    # Mark visited even if it was ignored color, to prevent reprocessing
                    visited[r,c] = True # Mark visited after processing neighbors

                if obj_coords:
                    coords_array = np.array(obj_coords)
                    min_r, min_c = coords_array.min(axis=0)
                    max_r, max_c = coords_array.max(axis=0)
                    objects.append({
                        'id': current_object_id,
                        'coords': coords_array,
                        'colors': dict(component_colors),
                        'size': len(obj_coords),
                        'bounding_box': ((min_r, min_c), (max_r, max_c)),
                        'dominant_color': max(component_colors, key=component_colors.get) if component_colors else -1
                    })
                    object_id_counter += 1
            visited[r, c] = True # Ensure all pixels get visited

    return labeled_grid, objects

def get_neighbors(r, c, rows, cols):
    """Gets orthogonal neighbor coordinates."""
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def transform(input_grid_list):
    """
    Applies the hypothesized transformation based on finding a key pattern
    in a small object and using it to modify a larger object.
    """
    input_grid = np.array(input_grid_list)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Background
    background_color = get_background_color(input_grid)

    # 2. Find Objects
    labeled_grid, objects = find_objects_bfs(input_grid, ignore_color=background_color)

    if not objects:
        return output_grid.tolist() # No objects to process

    # 3. Categorize Objects (Tentative: Largest = Main, Others = Keys)
    main_canvas = None
    key_objects = []
    if len(objects) == 1:
        main_canvas = objects[0]
    elif len(objects) > 1:
        objects.sort(key=lambda x: x['size'], reverse=True)
        main_canvas = objects[0]
        key_objects = objects[1:]
    else: # No objects found (shouldn't happen if not objects is checked, but defensive)
         return output_grid.tolist()

    # If no main canvas identified (e.g., only small objects), return input
    if main_canvas is None:
         return output_grid.tolist()

    # 4. Identify Key Pattern (Tentative: Adjacency in a Key Object)
    found_key_pattern = False
    key_color1 = -1
    key_color2 = -1
    key_object_id_to_remove = -1
    key_object_coords_to_remove = []

    for key_obj in key_objects:
        key_id = key_obj['id']
        for r_coord, c_coord in key_obj['coords']:
            current_pixel_color = input_grid[r_coord, c_coord]
            # Check neighbors within the same key object
            for nr, nc in get_neighbors(r_coord, c_coord, rows, cols):
                if labeled_grid[nr, nc] == key_id: # Neighbor is part of the same key object
                    neighbor_color = input_grid[nr, nc]
                    # Found two different non-background colors adjacent
                    if neighbor_color != current_pixel_color and neighbor_color != background_color:
                        key_color1 = current_pixel_color
                        key_color2 = neighbor_color
                        key_object_id_to_remove = key_id
                        key_object_coords_to_remove = key_obj['coords']
                        found_key_pattern = True
                        break # Found adjacent pair in this key object
            if found_key_pattern: break
        if found_key_pattern: break # Found pattern in the list of keys

    # 5 & 6. Check for Marker in Main & Apply Transformation (Tentative)
    if found_key_pattern and main_canvas:
        marker_color = key_color1 # Hypothesis
        target_color = key_color2 # Hypothesis
        main_color = main_canvas['dominant_color']

        # Check if marker_color exists in the main canvas
        marker_locations_in_main = []
        marker_present_in_main = False
        for r_mc, c_mc in main_canvas['coords']:
            if input_grid[r_mc, c_mc] == marker_color:
                marker_locations_in_main.append((r_mc, c_mc))
                marker_present_in_main = True
                # Optimization: If we only need to know *if* it's present, can break here.
                # break
        
        # If marker color is present, apply row/col painting
        if marker_present_in_main:
            marker_rows = set(r for r, c in marker_locations_in_main)
            marker_cols = set(c for r, c in marker_locations_in_main)

            # Apply Painting
            for r in range(rows):
                for c in range(cols):
                    # Check if pixel belongs to the main canvas originally
                    # and has the main color AND is in a marker row or column.
                    # Using labeled_grid ensures we only paint within the main object's original area.
                    if labeled_grid[r, c] == main_canvas['id'] and \
                       input_grid[r, c] == main_color and \
                       (r in marker_rows or c in marker_cols):
                        # Ensure we don't overwrite the marker pixels themselves if marker == main
                        is_marker_loc = False
                        for mr, mc in marker_locations_in_main:
                            if r == mr and c == mc:
                                is_marker_loc = True
                                break
                        if not is_marker_loc:
                             output_grid[r, c] = target_color
                         # If marker pixels should *also* be painted, remove the 'if not is_marker_loc:' check

            # 7. Clean Up (Tentative: Remove Key Object)
            if key_object_id_to_remove != -1:
                for r_k, c_k in key_object_coords_to_remove:
                     if 0 <= r_k < rows and 0 <= c_k < cols: # Bounds check
                          output_grid[r_k, c_k] = background_color

    # Return the potentially modified grid
    return output_grid.tolist()
```