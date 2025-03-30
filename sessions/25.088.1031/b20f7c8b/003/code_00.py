import numpy as np
from collections import deque
import copy

"""
Identifies two types of primary objects:
1.  'Targets': Objects with a Red (2) frame perfectly enclosing a connected Blue (1) interior.
2.  'Sources': Solid, single-color objects (including potentially solid Blue objects), excluding Red frames that aren't targets, and excluding Green frames if an anomaly condition is met.

Transformation Rules:
1.  Find all Targets and potential Sources.
2.  Handle Anomaly Case (if present): If a Green (3) framed Blue (1) object exists *and* a solid Green (3) object exists:
    a.  Change the pixels of the solid Green object to Blue (1).
    b.  Exclude both the Green frame and the original solid Green object from the list of Sources.
3.  Create the final list of Sources by excluding non-source objects (Red frames that didn't qualify as Targets, the Green frame in the anomaly case).
4.  Sort Targets by their top-left bounding box coordinate (row, then column).
5.  Sort the final Sources by their top-left bounding box coordinate (row, then column).
6.  Pair the sorted Targets and Sources index-wise.
7.  For each matched pair, replace the Blue (1) interior pixels of the Target object with the color of its paired Source object.
8.  All other pixels (background, frames, unused sources, etc.) remain unchanged.
"""

def find_objects(grid, ignore_colors=None):
    """
    Finds all connected objects of non-ignored colors using BFS.

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

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
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

    Args:
        grid (np.array): The grid.
        frame_pixels (set): Set of (r, c) tuples for the frame.
        frame_color (int): The color of the frame.
        interior_color (int): The potential color of the interior.

    Returns:
        set: Set of (r,c) tuples for the interior pixels if it's a single,
             connected component fully enclosed by the frame, otherwise None.
    """
    height, width = grid.shape
    potential_interior_starts = set()

    # 1. Find potential starting points for the interior (adjacent to the frame)
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

    # 2. Perform BFS from one start point to find a single connected component
    start_node = next(iter(potential_interior_starts)) # Pick one starting point
    q = deque([start_node])
    visited_interior = {start_node}
    found_interior_pixels = {start_node}

    while q:
        r, c = q.popleft()

        # Check neighbors for more interior pixels or boundaries
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc

                # Check bounds
                if not (0 <= nr < height and 0 <= nc < width):
                    # Interior pixel touches the edge of the grid - not enclosed
                    return None

                neighbor_pixel = (nr, nc)
                neighbor_color = grid[nr, nc]

                # If it's an interior pixel and not visited, add it
                if neighbor_color == interior_color and neighbor_pixel not in visited_interior:
                    visited_interior.add(neighbor_pixel)
                    q.append(neighbor_pixel)
                    found_interior_pixels.add(neighbor_pixel)
                # If it's NOT interior and NOT frame, then it's not enclosed
                elif neighbor_color != interior_color and neighbor_pixel not in frame_pixels:
                    return None # Touches something other than frame or self

    # 3. Verify that *all* potential starting points were part of this single component
    #    This ensures there isn't a separate blob of interior_color also adjacent to the frame.
    if not potential_interior_starts.issubset(found_interior_pixels):
         # This can happen if the 'frame' doesn't fully enclose all adjacent interior pixels
         return None

    # 4. Final check: Ensure all found interior pixels only touch frame or other interior pixels
    #    (This is partially covered by check 2, but double-check boundaries)
    for r_int, c_int in found_interior_pixels:
         for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                 if dr == 0 and dc == 0:
                     continue
                 nr, nc = r_int + dr, c_int + dc
                 neighbor_pixel = (nr, nc)
                 # If a neighbor is outside the grid (should have been caught earlier)
                 if not (0 <= nr < height and 0 <= nc < width):
                      return None # Should not happen if check 2 worked
                 # If neighbor is not part of the frame and not part of the found interior
                 if neighbor_pixel not in frame_pixels and neighbor_pixel not in found_interior_pixels:
                      return None # Touches something unexpected

    return found_interior_pixels


def transform(input_grid):
    """
    Transforms the input grid based on identifying framed objects (targets)
    and solid objects (sources), handling a green/green anomaly.
    Replaces the interior color of targets with the color of paired sources.
    """
    output_grid = np.copy(input_grid)
    all_objects = find_objects(output_grid, ignore_colors={0, 8}) # Find non-background objects

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
        is_green_frame = False
        is_solid_green = False

        # Check if it's a Red frame around Blue
        if color == 2: # Red
            interior = get_interior_pixels(output_grid, pixels, frame_color=2, interior_color=1)
            if interior:
                targets.append({'frame_pixels': pixels, 'interior_pixels': interior, 'bbox': bbox})
                is_target = True
        # Check if it's a Green frame around Blue OR a solid Green object
        elif color == 3: # Green
            interior = get_interior_pixels(output_grid, pixels, frame_color=3, interior_color=1)
            if interior:
                # Found the Green frame potentially involved in the anomaly
                green_frame_blue_interior_obj = {'frame_pixels': pixels, 'interior_pixels': interior, 'bbox': bbox, 'obj_ref': obj}
                is_green_frame = True
            else:
                # It's a solid Green object
                solid_green_objects.append(obj)
                is_solid_green = True

        # Add to potential sources if it's not a target and not a green frame
        # Solid green objects are added here initially, but might be removed later if anomaly occurs
        if not is_target and not is_green_frame:
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
    for src in potential_sources:
        # Exclude the green frame object if it exists
        if green_frame_blue_interior_obj and src['pixels'] == green_frame_blue_interior_obj['obj_ref']['pixels']:
            # print(f"Excluding green frame {src['bbox']} from sources.")
            continue
        # Exclude the solid green object that was changed in the anomaly
        if anomaly_handled and src['pixels'] == anomaly_green_to_change['pixels']:
            # print(f"Excluding anomaly-changed green object {src['bbox']} from sources.")
            continue
        # Exclude Red objects that were not identified as Targets (i.e., solid Red or invalid frames)
        # Note: get_interior_pixels already determined valid targets, so any remaining Red object is not a target.
        # However, the prompt implies red objects are *only* frames, never sources. Let's exclude them.
        if src['color'] == 2:
             # print(f"Excluding non-target red object {src['bbox']} from sources.")
             continue

        final_sources.append(src)


    # --- Pair Targets and Final Sources ---
    targets.sort(key=lambda o: (o['bbox'][0], o['bbox'][1]))
    final_sources.sort(key=lambda o: (o['bbox'][0], o['bbox'][1]))

    # --- Perform Transformation ---
    num_targets = len(targets)
    num_sources = len(final_sources)

    if num_targets == num_sources:
        # print(f"Matching {num_targets} targets to {num_sources} sources.")
        for i in range(num_targets):
            target = targets[i]
            source = final_sources[i]
            new_color = source['color']
            # print(f"  Target {i} (bbox {target['bbox']}) <- Source {i} (color {new_color}, bbox {source['bbox']})")

            for r, c in target['interior_pixels']:
                # Check if pixel still exists and is blue (in case of overlaps?)
                if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1] and output_grid[r,c] == 1:
                     output_grid[r, c] = new_color
    # else:
        # print(f"Warning: Mismatch between number of targets ({num_targets}) and final sources ({num_sources}). No transformation applied.")
        # print("Targets:", [t['bbox'] for t in targets])
        # print("Sources:", [(s['color'], s['bbox']) for s in final_sources])


    return output_grid