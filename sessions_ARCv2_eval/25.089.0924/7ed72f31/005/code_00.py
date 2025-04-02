import numpy as np
from collections import Counter, deque

"""
Transformation Rule Description:

1.  Initialize the output grid as an identical copy of the input grid.
2.  Determine the background color: This is the most frequent color in the input grid, excluding red (color 2).
3.  Identify all distinct contiguous groups (objects) of pixels in the input grid using a method like Breadth-First Search (BFS). Store each object's color and the set of its pixel coordinates.
4.  Separate the identified objects into two categories: 'red_objects' (color 2) and 'reflectable_objects' (neither red nor background color).
5.  Classify each 'red_object' based on its shape:
    - 'H' (Horizontal Line): Height is 1, Width > 1.
    - 'V' (Vertical Line): Width is 1, Height > 1.
    - 'P' (Point): Height is 1, Width is 1.
    (Height/Width calculated from the min/max row/column of the object's pixels).
6.  Create a mapping from red pixel coordinates to the classified red object they belong to.
7.  Iterate through each 'reflectable_object'.
8.  For each reflectable object, check if any of its pixels are cardinally adjacent to any pixel belonging to a 'red_object'.
9.  If a reflectable object pixel `(r, c)` is adjacent to a red pixel `(nr, nc)`:
    a.  Identify the specific red object associated with `(nr, nc)` using the mapping created earlier. Get its classification ('H', 'V', or 'P').
    b.  Determine the reflection type based on the classification: Vertical for 'H', Horizontal for 'V' or 'P'.
    c.  Iterate through *all* pixels `(orig_r, orig_c)` of the current reflectable object.
    d.  Calculate the reflected coordinates `(rr, rc)` based on the reflection type and the coordinates of the *adjacent red pixel* `(nr, nc)` that triggered the reflection:
        *   Vertical Reflection (across row `nr`): `rr = nr + (nr - orig_r)`, `rc = orig_c`.
        *   Horizontal Reflection (across col `nc`): `rr = orig_r`, `rc = nc + (nc - orig_c)`.
    e.  Check if the calculated `(rr, rc)` is within the grid boundaries.
    f.  If `(rr, rc)` is within bounds AND the pixel at `output_grid[rr, rc]` currently holds the background color, update `output_grid[rr, rc]` with the color of the reflectable object.
    g. Once a reflection is triggered and processed for a reflectable object (due to adjacency with *one* red pixel), stop checking its other pixels for adjacency and move to the next reflectable object. (Assumption: An object is reflected only once based on its first detected adjacency).
10. Return the modified output grid as a list of lists.
"""

def find_background_color(grid):
    """Finds the most frequent color in the grid, excluding red (2)."""
    counts = Counter(grid.flatten())
    if 2 in counts:
        del counts[2] # Exclude red

    if not counts:
        all_counts = Counter(grid.flatten())
        if 0 in all_counts: return 0
        if grid.size > 0:
            # Find most frequent among all if no non-red exists or only red exists
            non_red_counts = Counter(c for c in grid.flatten() if c != 2)
            if non_red_counts:
                return non_red_counts.most_common(1)[0][0]
            # If truly only red, pick an arbitrary background like 0, though ARC tasks usually have backgrounds.
            return 0
        return 0 # Default fallback for empty grid

    return counts.most_common(1)[0][0]

def is_within_bounds(grid_shape, r, c):
    """Checks if coordinates (r, c) are within the grid boundaries."""
    height, width = grid_shape
    return 0 <= r < height and 0 <= c < width

def find_connected_components(grid):
    """Finds all contiguous objects (connected components) in the grid."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            if not visited[r, c]:
                color = grid[r, c]
                component_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                component_pixels.add((r, c))

                while q:
                    row, col = q.popleft()
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if is_within_bounds((height, width), nr, nc) and \
                           not visited[nr, nc] and \
                           grid[nr, nc] == color:
                            visited[nr, nc] = True
                            component_pixels.add((nr, nc))
                            q.append((nr, nc))

                if component_pixels:
                    objects.append({'color': color, 'pixels': component_pixels})
    return objects

def classify_red_object(pixels):
    """Classifies a red object based on its pixel coordinates."""
    if not pixels:
        return None # Should not happen for valid objects

    rows = [r for r, c in pixels]
    cols = [c for r, c in pixels]
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)

    height = max_r - min_r + 1
    width = max_c - min_c + 1

    if height == 1 and width > 1:
        return 'H' # Horizontal Line
    elif width == 1 and height > 1:
        return 'V' # Vertical Line
    elif height == 1 and width == 1:
        return 'P' # Point
    else:
        # Handle blocks or other shapes - Treat as 'P' for reflection?
        # Or base on adjacency? Examples only show lines/points as mirrors.
        # Let's default to 'P' (horizontal reflection) for blocks for now.
         return 'P'


def transform(input_grid):
    # Convert to numpy array
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    grid_shape = (height, width)

    # 1. Initialize output_grid as a copy
    output_grid = np.copy(input_grid_np)

    # 2. Determine background color
    background_color = find_background_color(input_grid_np)

    # 3. Find all connected components (objects)
    all_objects = find_connected_components(input_grid_np)

    # 4. Separate objects
    red_objects = []
    reflectable_objects = []
    red_pixel_map = {} # Map: red pixel coord -> its object info

    for obj in all_objects:
        if obj['color'] == 2:
            # 5. Classify Red Objects
            classification = classify_red_object(obj['pixels'])
            obj['classification'] = classification
            red_objects.append(obj)
            # 6. Create red pixel map
            for pixel in obj['pixels']:
                red_pixel_map[pixel] = obj
        elif obj['color'] != background_color:
            reflectable_objects.append(obj)

    # 7. Iterate through reflectable objects
    for r_obj in reflectable_objects:
        obj_color = r_obj['color']
        obj_pixels = r_obj['pixels']
        reflection_triggered = False
        
        # 8. Check for adjacency to any red pixel
        for r, c in obj_pixels:
            if reflection_triggered: # Only reflect once per object
                break
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc

                # 9. If adjacent to a red pixel
                if is_within_bounds(grid_shape, nr, nc) and input_grid_np[nr, nc] == 2:
                    # 9a. Identify the red object and its classification
                    if (nr, nc) in red_pixel_map:
                        adjacent_red_obj = red_pixel_map[(nr, nc)]
                        red_classification = adjacent_red_obj['classification']
                        reflection_triggered = True # Mark that reflection should happen

                        # 9b. Determine reflection type
                        reflect_vertically = (red_classification == 'H')

                        # 9c. Iterate through ALL pixels of the reflectable object
                        for orig_r, orig_c in obj_pixels:
                            # 9d. Calculate reflected coordinates based on adjacent red pixel (nr, nc)
                            rr, rc = -1, -1
                            if reflect_vertically:
                                rr = nr + (nr - orig_r)
                                rc = orig_c
                            else: # Reflect horizontally
                                rr = orig_r
                                rc = nc + (nc - orig_c)

                            # 9e. Check bounds
                            if is_within_bounds(grid_shape, rr, rc):
                                # 9f. Update output grid if background
                                if output_grid[rr, rc] == background_color:
                                    output_grid[rr, rc] = obj_color
                        
                        # 9g. Break neighbor check once reflection is done for this object
                        break 
            # Break pixel loop once reflection is triggered
            if reflection_triggered:
                break

    # 11. Return the modified grid as list of lists
    return output_grid.tolist()