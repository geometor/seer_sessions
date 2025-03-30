Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np
from collections import deque
import copy

"""
Transformation Rule Description:

1.  **Object Identification:**
    *   Identify all distinct connected objects in the input grid using 4-way adjacency. Ignore background colors White (0) and Azure (8). Each object has a color, a set of pixel coordinates, and a bounding box.

2.  **Object Categorization:** Classify each identified object:
    *   **Potential Targets:** Red (2) objects.
    *   **Potential Anomaly Frames:** Green (3) objects.
    *   **Potential Sources:** All other objects (initially includes solid Green, Blue, Yellow, etc., but excludes Red).

3.  **Interior Analysis (for Red and Green frames):**
    *   For each Red(2) and Green(3) object (potential frame), determine the pixels it encloses using a flood-fill algorithm starting from the grid borders.
    *   Mark the frame pixels themselves as 'visited'.
    *   Flood-fill (4-way adjacency) from all border pixels that are not part of the frame, marking reachable pixels as 'visited'.
    *   Any pixel *not* visited by the flood fill is considered enclosed by *some* frame.
    *   Filter these enclosed pixels to find those spatially inside the bounding box of the specific Red/Green frame being analyzed.
    *   Verify the contents of this enclosed area:
        *   If all non-background (non-0, non-8) pixels within this enclosed area are Blue (1), then the frame is valid for its type.
        *   Store the set of enclosed Blue (1) pixels as the 'interior'.

4.  **Target Finalization:**
    *   A Red (2) object is confirmed as a 'Target' if the interior analysis (Step 3) finds it encloses only Blue (1) pixels (besides background). Store the Target along with its frame pixels and interior blue pixels.

5.  **Anomaly Detection and Handling:**
    *   Identify if there is exactly one Green (3) object confirmed as an 'Anomaly Frame' (encloses only Blue(1) pixels, per Step 3).
    *   Identify if there are one or more 'Solid Green' objects (Green objects *not* identified as Anomaly Frames).
    *   If both an Anomaly Frame and at least one Solid Green object exist:
        *   Select the Solid Green object with the topmost, then leftmost bounding box coordinate.
        *   In the *output grid*, change the color of all pixels belonging to this selected Solid Green object to Blue (1).
        *   Mark this specific Solid Green object as 'anomaly-modified'.
        *   Mark the Anomaly Frame (Green frame) as 'consumed-by-anomaly'.
        *   Set an 'anomaly_handled' flag.

6.  **Source Finalization:**
    *   Start with the list of 'Potential Sources'.
    *   Filter out (remove) the following:
        *   Any Red (2) objects (cannot be sources).
        *   Any Blue (1) objects (cannot be sources).
        *   If `anomaly_handled` is true:
            *   Remove the Green frame object ('consumed-by-anomaly').
            *   Remove the Solid Green object ('anomaly-modified').

7.  **Sorting:**
    *   Sort the finalized 'Targets' based on their bounding box's top-left coordinate (row, then column).
    *   Sort the finalized 'Sources' based on their bounding box's top-left coordinate (row, then column).

8.  **Transformation (Filling):**
    *   Check if the number of Targets equals the number of Sources, and is greater than zero.
    *   If the counts match:
        *   Pair the i-th Target with the i-th Source from the sorted lists.
        *   For each pair, replace the color of the 'interior' Blue (1) pixels of the Target with the *original* color of the paired Source object. Perform this change in the *output grid*.

9.  **Output:**
    *   Return the modified output grid. If the anomaly occurred, it includes the Green-to-Blue change. If the target/source counts matched, it includes the interior filling. Otherwise, it might return the initial grid (if no targets/sources) or the anomaly-modified grid (if anomaly occurred but counts didn't match).
"""

import numpy as np
from collections import deque
import copy

def find_objects(grid, ignore_colors=None):
    """
    Finds all connected objects of non-ignored colors using BFS with 4-way adjacency.

    Args:
        grid (np.array): The input grid.
        ignore_colors (set): Set of colors to ignore (e.g., background).

    Returns:
        list: A list of dictionaries, each representing an object with
              'color', 'pixels' (set of (r, c) tuples), and 'bbox'.
    """
    if ignore_colors is None:
        ignore_colors = {0, 8} # Default background colors

    objects = []
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            # Check if the pixel is already visited or if it's an ignored color
            if visited[r, c] or color in ignore_colors:
                continue

            # Start BFS for a new object
            obj_pixels = set()
            q = deque([(r, c)])
            visited[r, c] = True
            min_r, min_c, max_r, max_c = r, c, r, c
            current_color = color # Color of the object being traced

            while q:
                row, col = q.popleft()
                obj_pixels.add((row, col))
                min_r = min(min_r, row)
                min_c = min(min_c, col)
                max_r = max(max_r, row)
                max_c = max(max_c, col)

                # Check 4 neighbors (orthogonal)
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = row + dr, col + dc
                    # Check bounds, color match, and not visited
                    if 0 <= nr < height and 0 <= nc < width and \
                       grid[nr, nc] == current_color and not visited[nr, nc]:
                        visited[nr, nc] = True
                        q.append((nr, nc))

            objects.append({
                'color': current_color,
                'pixels': obj_pixels,
                'bbox': (min_r, min_c, max_r, max_c)
            })
    return objects


def get_enclosed_pixels(grid, frame_pixels):
    """
    Identifies all pixels enclosed by a given set of frame pixels using flood fill from outside.
    Does NOT check the color of the enclosed pixels at this stage.

    Args:
        grid (np.array): The grid.
        frame_pixels (set): Set of (r, c) tuples for the potential frame.

    Returns:
        set: Set of (r,c) tuples for all pixels enclosed by the frame.
             Returns an empty set if the frame is incomplete or touches the border implicitly.
    """
    height, width = grid.shape
    visited_outside = np.zeros_like(grid, dtype=bool)
    q = deque()

    # Mark frame pixels as visited to act as barriers
    for r, c in frame_pixels:
        if 0 <= r < height and 0 <= c < width:
            visited_outside[r, c] = True
        else: # Should not happen if frame_pixels come from find_objects
             return set() # Invalid frame pixel

    # Start flood fill from all border cells that are not part of the frame
    for r in range(height):
        if not visited_outside[r, 0]:
            q.append((r, 0))
            visited_outside[r, 0] = True
        if not visited_outside[r, width - 1]:
            q.append((r, width - 1))
            visited_outside[r, width - 1] = True
    for c in range(1, width - 1): # Avoid double-adding corners
        if not visited_outside[0, c]:
            q.append((0, c))
            visited_outside[0, c] = True
        if not visited_outside[height - 1, c]:
            q.append((height - 1, c))
            visited_outside[height - 1, c] = True

    # Perform BFS (flood fill) from the outside/borders
    while q:
        r, c = q.popleft()
        # Use 4-way adjacency for flood fill
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width and not visited_outside[nr, nc]:
                visited_outside[nr, nc] = True
                q.append((nr, nc))

    # Identify interior pixels: any non-frame pixel that was NOT visited by the flood fill
    interior_pixels = set()
    for r in range(height):
        for c in range(width):
            # Not visited by outside flood AND not part of the original frame
            if not visited_outside[r, c] and (r, c) not in frame_pixels:
                 interior_pixels.add((r,c))

    return interior_pixels

def check_interior_and_get_blue(grid, enclosed_pixels):
    """
    Checks if all non-background pixels in a set are Blue (1).
    Returns the set of Blue pixels if condition met, otherwise None.
    """
    blue_interior_pixels = set()
    only_blue_or_background = True
    found_any_blue = False

    for r_int, c_int in enclosed_pixels:
        pixel_color = grid[r_int, c_int]
        if pixel_color == 1:
            blue_interior_pixels.add((r_int, c_int))
            found_any_blue = True
        elif pixel_color not in {0, 8}: # Background colors
            only_blue_or_background = False
            break # Found a non-blue, non-background color

    if found_any_blue and only_blue_or_background:
        return blue_interior_pixels
    else:
        return None


def transform(input_grid):
    """
    Transforms the input grid based on identifying framed targets (Red frame/Blue interior)
    and solid sources, handling a Green/Green anomaly. Replaces the interior
    color of targets with the color of paired sources.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 1. Find all potential objects using 4-way connectivity
    all_objects = find_objects(output_grid, ignore_colors={0, 8})

    targets = []
    potential_sources = []
    green_frame_objects = [] # Store green objects identified as frames
    solid_green_objects = [] # Store green objects NOT identified as frames
    
    # Keep track of original object references for filtering later
    anomaly_frame_ref = None
    anomaly_solid_green_ref = None

    # --- 2 & 3. Categorize objects and Analyze Interiors ---
    for obj in all_objects:
        color = obj['color']
        pixels = obj['pixels']
        bbox = obj['bbox']

        is_frame_candidate = (color == 2 or color == 3) # Red or Green
        is_confirmed_frame = False
        blue_interior = None

        if is_frame_candidate:
            # Find all pixels potentially enclosed by this frame
            enclosed_pixels = get_enclosed_pixels(input_grid, pixels)

            if enclosed_pixels:
                # Check if the enclosed area contains only Blue (1) or background (0, 8)
                blue_interior = check_interior_and_get_blue(input_grid, enclosed_pixels)

                if blue_interior:
                    is_confirmed_frame = True
                    # --- 4. Target Finalization ---
                    if color == 2: # Red Frame
                        targets.append({
                            'frame_pixels': pixels,
                            'interior_pixels': blue_interior,
                            'bbox': bbox,
                            'obj_ref': obj # Keep ref if needed later
                        })
                    # --- Green Anomaly Frame Identification ---
                    elif color == 3: # Green Frame
                         green_frame_objects.append({
                             'frame_pixels': pixels,
                             'interior_pixels': blue_interior,
                             'bbox': bbox,
                             'obj_ref': obj
                         })

        # --- Categorize non-frames or failed frames ---
        if not is_confirmed_frame:
            if color == 3: # Green object, but not a valid frame
                solid_green_objects.append(obj)
                potential_sources.append(obj) # Add solid green to potential sources initially
            elif color != 2: # Any other color except Red (which can only be frames)
                potential_sources.append(obj) # Add to potential sources

    # --- 5. Anomaly Detection and Handling ---
    anomaly_handled = False
    # Check conditions: exactly one green frame and at least one solid green
    if len(green_frame_objects) == 1 and len(solid_green_objects) > 0:
        anomaly_handled = True
        anomaly_frame_ref = green_frame_objects[0]['obj_ref'] # The green frame object

        # Select the solid green object with the topmost, then leftmost bbox
        solid_green_objects.sort(key=lambda o: (o['bbox'][0], o['bbox'][1]))
        anomaly_solid_green_ref = solid_green_objects[0] # The solid green object to change

        # Change its color to Blue (1) in the output grid
        for r, c in anomaly_solid_green_ref['pixels']:
            if 0
---
