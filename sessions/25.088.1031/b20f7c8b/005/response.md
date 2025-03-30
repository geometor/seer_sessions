```python
import numpy as np
from collections import deque
import copy

"""
Identifies two types of primary objects:
1.  'Targets': Objects with a Red (2) frame perfectly enclosing a connected Blue (1) interior. Connectivity is based on 4-way adjacency (up, down, left, right). The enclosure check uses 8-way adjacency.
2.  'Sources': Solid, single-color objects (connected components based on 4-way adjacency), excluding Red objects and potentially excluding Green objects based on an anomaly condition. Background colors (White 0, Azure 8) are ignored.

Transformation Rules:
1.  Find all connected components (objects) in the grid using 4-way adjacency, ignoring background colors.
2.  Categorize objects:
    a.  Identify 'Targets' by checking Red (2) objects. For each Red object, verify if it perfectly encloses a single connected component of Blue (1) pixels using the `get_interior_pixels` helper function. Store valid targets.
    b.  Identify potential 'Sources'. Initially, consider all non-Red objects as potential sources. Keep track of any Green (3) object that frames a Blue (1) interior (`green_frame_blue_interior_obj`) and any solid Green (3) objects (`solid_green_objects`).
3.  Handle Anomaly Case (if present): If both `green_frame_blue_interior_obj` and at least one `solid_green_objects` exist:
    a.  Select the first found solid Green object (`anomaly_green_to_change`).
    b.  Change the pixels of this selected solid Green object to Blue (1) in the output grid.
    c.  Mark the anomaly as handled.
4.  Create the final list of Sources: Start with all potential sources found in step 2b. Then filter out:
    a.  Any Red (2) objects (these can only be frames, not sources).
    b.  If the anomaly was handled:
        i.  Exclude the Green object that acted as the frame (`green_frame_blue_interior_obj`).
        ii. Exclude the solid Green object that was modified (`anomaly_green_to_change`).
5.  Sort Targets by their top-left bounding box coordinate (row, then column).
6.  Sort the final Sources by their top-left bounding box coordinate (row, then column).
7.  Pair the sorted Targets and Sources index-wise. If the number of targets and sources does not match, no transformation is performed.
8.  For each matched pair, replace the Blue (1) interior pixels of the Target object with the color of its paired Source object in the output grid.
9.  All other pixels (background, frames, unused sources, etc.) remain unchanged from the (potentially anomaly-modified) grid.
"""

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
            if not visited[r, c] and color not in ignore_colors:
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

def get_interior_pixels(grid, frame_pixels, frame_color, interior_color):
    """
    Identifies the connected interior pixels of a potential frame.
    Uses 8-way adjacency for checking neighborhood relationships for enclosure.

    Args:
        grid (np.array): The grid.
        frame_pixels (set): Set of (r, c) tuples for the frame.
        frame_color (int): The color of the frame (unused in logic, but good for context).
        interior_color (int): The potential color of the interior.

    Returns:
        set: Set of (r,c) tuples for the interior pixels if it's a single,
             connected component fully enclosed by the frame, otherwise None.
    """
    height, width = grid.shape
    potential_interior_starts = set()

    # 1. Find potential starting points for the interior (adjacent to the frame, including diagonals)
    for r_frame, c_frame in frame_pixels:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r_frame + dr, c_frame + dc
                # Check bounds, is interior color, and not part of the frame itself
                if 0 <= nr < height and 0 <= nc < width and \
                   grid[nr, nc] == interior_color and \
                   (nr, nc) not in frame_pixels:
                    potential_interior_starts.add((nr, nc))

    if not potential_interior_starts:
        return None # No pixels of interior_color adjacent to the frame

    # 2. Perform BFS from one start point to find a single connected component (using 8-way for interior connectivity)
    start_node = next(iter(potential_interior_starts)) # Pick one starting point
    q = deque([start_node])
    visited_interior = {start_node}
    found_interior_pixels = {start_node}
    is_enclosed = True # Assume enclosed until proven otherwise

    while q:
        r, c = q.popleft()

        # Check 8 neighbors (including diagonals) for boundaries or more interior pixels
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                neighbor_pixel = (nr, nc)

                # Check if neighbor is outside the grid bounds
                if not (0 <= nr < height and 0 <= nc < width):
                    is_enclosed = False
                    # print(f"Interior pixel ({r},{c}) touches grid edge ({nr},{nc})")
                    break # Stop checking neighbors for this pixel

                neighbor_color = grid[nr, nc]

                # If it's an interior pixel and not visited, add it
                if neighbor_color == interior_color and neighbor_pixel not in visited_interior:
                    visited_interior.add(neighbor_pixel)
                    q.append(neighbor_pixel)
                    found_interior_pixels.add(neighbor_pixel)
                # If it's NOT interior and NOT part of the frame, then it's not enclosed
                elif neighbor_color != interior_color and neighbor_pixel not in frame_pixels:
                    is_enclosed = False
                    # print(f"Interior pixel ({r},{c}) touches non-frame/non-interior ({nr},{nc}) color {neighbor_color}")
                    break # Stop checking neighbors for this pixel
            if not is_enclosed:
                break # Stop BFS if enclosure broken

    if not is_enclosed:
        return None

    # 3. Verify that *all* potential starting points were part of this single component
    #    This ensures there isn't a separate blob of interior_color also adjacent to the frame.
    if not potential_interior_starts.issubset(found_interior_pixels):
         # This means the BFS didn't reach all pixels adjacent to the frame,
         # implying either multiple disjoint interiors or an incomplete enclosure.
         # print(f"Not all potential starts {potential_interior_starts} were in found interior {found_interior_pixels}")
         return None

    # 4. (Implicitly covered by BFS checks) Ensure all found interior pixels only touch frame or other interior pixels

    return found_interior_pixels


def transform(input_grid):
    """
    Transforms the input grid based on identifying framed objects (targets)
    and solid objects (sources), handling a green/green anomaly.
    Replaces the interior color of targets with the color of paired sources.
    """
    # Make a copy to modify
    output_grid = np.copy(input_grid)
    
    # Find all potential objects using 4-way connectivity
    all_objects = find_objects(output_grid, ignore_colors={0, 8})

    targets = []
    potential_sources = []
    green_frame_blue_interior_obj = None
    solid_green_objects = []
    anomaly_green_to_change = None # Store the specific solid green object if anomaly occurs

    # --- Categorize all found objects ---
    for obj in all_objects:
        color = obj['color']
        pixels = obj['pixels']
        bbox = obj['bbox']

        is_target = False
        is_green_frame_anomaly_candidate = False
        is_solid_green = False

        # Check if it's a Red frame around Blue (potential target)
        if color == 2: # Red
            # Use the original grid for checking interior properties
            interior = get_interior_pixels(input_grid, pixels, frame_color=2, interior_color=1)
            if interior:
                targets.append({'frame_pixels': pixels, 'interior_pixels': interior, 'bbox': bbox})
                is_target = True
        
        # Check Green objects for anomaly condition or being a potential source
        elif color == 3: # Green
            # Check if it frames a Blue interior
            # Use the original grid for checking interior properties
            interior = get_interior_pixels(input_grid, pixels, frame_color=3, interior_color=1)
            if interior:
                # Found the Green frame potentially involved in the anomaly
                green_frame_blue_interior_obj = {'frame_pixels': pixels, 'interior_pixels': interior, 'bbox': bbox, 'obj_ref': obj}
                is_green_frame_anomaly_candidate = True
                # Green frames are never sources, regardless of anomaly
            else:
                # It's a solid Green object (or other complex shape)
                solid_green_objects.append(obj)
                is_solid_green = True
                # Add solid green to potential sources for now, might be removed by anomaly
                potential_sources.append(obj)

        # Add other non-Red, non-Green-frame objects to potential sources
        # Blue objects *are* potential sources if they are solid
        if not is_target and color != 2 and not is_green_frame_anomaly_candidate and not is_solid_green:
             potential_sources.append(obj)

    # --- Handle Anomaly (Green frame + Solid Green) ---
    anomaly_handled = False
    if green_frame_blue_interior_obj and solid_green_objects:
        # Anomaly condition met. Choose the first solid green object found.
        anomaly_green_to_change = solid_green_objects[0]

        # Change its color in the output grid
        for r, c in anomaly_green_to_change['pixels']:
            output_grid[r, c] = 1 # Change to Blue

        # Mark anomaly as handled
        anomaly_handled = True
        # print(f"Anomaly handled: Changed solid green object {anomaly_green_to_change['bbox']} to blue.")


    # --- Filter Sources ---
    final_sources = []
    # Iterate through the initially collected potential sources
    for src in potential_sources:
        # Exclude the solid green object that was changed in the anomaly
        # Need to compare by pixels as the object reference might be stale if list was copied
        if anomaly_handled and src['pixels'] == anomaly_green_to_change['pixels']:
            # print(f"Excluding anomaly-changed green object {src['bbox']} from sources.")
            continue
        # Exclude any remaining Red objects (shouldn't be in potential_sources anyway, but double check)
        if src['color'] == 2:
             # print(f"Excluding red object {src['bbox']} from sources.")
             continue
        # Note: The green frame object was never added to potential_sources if identified correctly

        final_sources.append(src)


    # --- Pair Targets and Final Sources ---
    # Sort targets by top-left corner (row, then column)
    targets.sort(key=lambda o: (o['bbox'][0], o['bbox'][1]))
    # Sort sources by top-left corner (row, then column)
    final_sources.sort(key=lambda o: (o['bbox'][0], o['bbox'][1]))

    # --- Perform Transformation ---
    num_targets = len(targets)
    num_sources = len(final_sources)

    # Only proceed if the counts match
    if num_targets > 0 and num_targets == num_sources:
        # print(f"Matching {num_targets} targets to {num_sources} sources.")
        # Pair them index-wise based on the sorted lists
        for i in range(num_targets):
            target = targets[i]
            source = final_sources[i]
            new_color = source['color'] # Get the color of the matched source
            
            # Ensure the source color isn't the anomaly-changed one (it should be the original color)
            # If the source IS the object that got changed by anomaly, its color is now BLUE (1)
            # The description isn't 100% clear if the *original* green color or the *new* blue color should be used IF it were a source.
            # However, the description says "Exclude [...] the original solid Green object from the list of Sources."
            # The filtering logic above *should* prevent the anomaly-changed object from being in final_sources.

            # print(f"  Target {i} (bbox {target['bbox']}) <- Source {i} (color {new_color}, bbox {source['bbox']})")

            # Fill the interior of the target with the source color
            for r, c in target['interior_pixels']:
                # Double check bounds and that it's still blue (might be redundant)
                if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]: # and output_grid[r,c] == 1: (Removed check in case interior overlaps somehow)
                     output_grid[r, c] = new_color
    # else:
        # Optional: Add debugging print for mismatch cases
        # if num_targets != num_sources:
        #      print(f"Warning: Mismatch between number of targets ({num_targets}) and final sources ({num_sources}). No transformation applied.")
        #      print("Targets:", [t['bbox'] for t in targets])
        #      print("Sources:", [(s['color'], s['bbox']) for s in final_sources])
        # elif num_targets == 0:
        #      print("No targets found.")


    return output_grid
```