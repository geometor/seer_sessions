```python
import numpy as np
from collections import deque

"""
Identify objects in the input grid, specifically focusing on:
1. "Target" objects: Red (2) frames surrounding a Blue (1) interior.
2. "Source" objects: Solid, single-color shapes (not Red frames, often Green, Yellow, Gray, Magenta, etc.).
3. Anomaly case (seen in train_2): A solid Green (3) object and a Green (3) framed Blue (1) object.

Transformation rules:
1. General rule: For each Target object (Red frame, Blue interior), find a corresponding Source object. Replace the Blue (1) interior pixels of the Target with the color of the paired Source object. The pairing is done by sorting Targets and Sources by their top-left bounding box coordinates and matching them index-wise.
2. Anomaly rule: If both a solid Green (3) object and a Green (3) framed Blue (1) object exist, change the solid Green object's pixels to Blue (1) and leave the Green-framed object untouched. This Green object is then not considered a Source for the general rule.
3. All other pixels (background, frames, other shapes not involved in the above) remain unchanged.

Helper functions needed:
- find_objects: Locates connected components (objects) of non-background colors.
- get_bounding_box: Calculates the bounding box of an object.
- identify_framed_objects: Specifically finds objects with a frame of one color surrounding an interior of another color.
"""

def find_objects(grid):
    """
    Finds all connected objects of non-background colors (0 and 8).

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, each representing an object with
              'color', 'pixels' (set of (r, c) tuples), and 'bbox'.
    """
    objects = []
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    background_colors = {0, 8}

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if not visited[r, c] and color not in background_colors:
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c, max_r, max_c = r, c, r, c

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
                            if 0 <= nr < height and 0 <= nc < width and \
                               not visited[nr, nc] and grid[nr, nc] == color:
                                visited[nr, nc] = True
                                q.append((nr, nc))

                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
    return objects

def identify_framed_object(grid, frame_pixels, frame_color, interior_color):
    """
    Checks if a set of frame_pixels perfectly encloses a single connected
    component of interior_color.

    Args:
        grid (np.array): The input grid.
        frame_pixels (set): Set of (r, c) tuples for the potential frame.
        frame_color (int): The color of the frame.
        interior_color (int): The color of the potential interior.

    Returns:
        set: Set of (r,c) tuples for the interior pixels if it's a valid framed object,
             otherwise None.
    """
    if not frame_pixels:
        return None

    height, width = grid.shape
    q = deque()
    potential_interior = set()
    visited_interior = set()

    # Find starting points for interior search (neighbors of frame pixels)
    for r_frame, c_frame in frame_pixels:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if abs(dr) + abs(dc) != 1: # Only check cardinal neighbors initially
                    continue
                r_adj, c_adj = r_frame + dr, c_frame + dc
                # Check bounds, if it's the interior color, and not part of the frame
                if 0 <= r_adj < height and 0 <= c_adj < width and \
                   grid[r_adj, c_adj] == interior_color and \
                   (r_adj, c_adj) not in frame_pixels:
                    potential_interior.add((r_adj, c_adj))
                    if not q and (r_adj, c_adj) not in visited_interior:
                         q.append((r_adj, c_adj))
                         visited_interior.add((r_adj, c_adj))


    if not q: # No potential interior pixels found adjacent to frame
        return None

    # Perform BFS on potential interior pixels starting from one point
    actual_interior = set()
    start_r, start_c = q[0] # Use the first discovered potential interior pixel

    # Re-initialize queue and visited for clean BFS of the single component
    q = deque([(start_r, start_c)])
    visited_interior = {(start_r, start_c)}
    actual_interior.add((start_r, start_c))


    while q:
        r_int, c_int = q.popleft()

        # Check neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                 if dr == 0 and dc == 0:
                     continue
                 nr, nc = r_int + dr, c_int + dc

                 if 0 <= nr < height and 0 <= nc < width:
                     neighbor_pixel = (nr, nc)
                     neighbor_color = grid[nr, nc]

                     # If neighbor is interior color and not visited, add to queue
                     if neighbor_color == interior_color and neighbor_pixel not in visited_interior:
                         visited_interior.add(neighbor_pixel)
                         q.append(neighbor_pixel)
                         actual_interior.add(neighbor_pixel)
                     # If neighbor is NOT interior and NOT frame, then it's not fully enclosed
                     elif neighbor_color != interior_color and neighbor_pixel not in frame_pixels:
                          # Check if this non-interior, non-frame neighbor is outside the bounding box of the frame
                          min_r_frame = min(r for r, c in frame_pixels)
                          min_c_frame = min(c for r, c in frame_pixels)
                          max_r_frame = max(r for r, c in frame_pixels)
                          max_c_frame = max(c for r, c in frame_pixels)
                          if not (min_r_frame <= nr <= max_r_frame and min_c_frame <= nc <= max_c_frame):
                              # If it touches something other than the frame or itself, and that thing is outside the frame's bbox,
                              # it might still be enclosed if the frame is concave, but simple check fails.
                              # A more robust check would be needed, but let's assume frames are simple enough for now.
                              # For now, we assume if it touches non-frame/non-interior within bbox, it's okay, but outside it's leaking.
                              # Let's refine: if ANY interior pixel touches a non-frame color pixel, it's invalid.
                              return None # Touches something other than frame or self

    # Check if all potential interior pixels were covered by the single BFS
    # This check might be redundant if the frame integrity check is good
    # if potential_interior != actual_interior:
        # print(f"Potential interior {potential_interior} != Actual {actual_interior}")
        # return None # Interior is not a single connected component

    # Final check: ensure all interior pixels only touch frame or other interior pixels
    for r_int, c_int in actual_interior:
         for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                 if dr == 0 and dc == 0:
                     continue
                 nr, nc = r_int + dr, c_int + dc
                 if 0 <= nr < height and 0 <= nc < width:
                     neighbor_pixel = (nr, nc)
                     if neighbor_pixel not in frame_pixels and neighbor_pixel not in actual_interior:
                          # Touches something that is neither frame nor interior
                          # print(f"Interior pixel {(r_int, c_int)} touches non-frame/non-interior at {(nr, nc)}")
                          return None

    return actual_interior


def transform(input_grid):
    """
    Transforms the input grid based on identifying framed objects and source objects.
    Replaces the interior color of framed objects with the color of corresponding source objects.
    Handles a special case involving green-framed and solid green objects.
    """
    output_grid = np.copy(input_grid)
    all_objects = find_objects(output_grid)

    targets = []
    potential_sources = []
    green_frame_blue_interior_obj = None
    solid_green_objects = []

    # --- Categorize objects ---
    for obj in all_objects:
        color = obj['color']
        pixels = obj['pixels']

        if color == 2: # Red - potential target frame
            interior_pixels = identify_framed_object(output_grid, pixels, frame_color=2, interior_color=1)
            if interior_pixels:
                targets.append({'frame_pixels': pixels, 'interior_pixels': interior_pixels, 'bbox': obj['bbox']})
            else:
                potential_sources.append(obj) # Red object, but not a frame for blue
        elif color == 3: # Green - potential anomaly frame or solid object
             interior_pixels = identify_framed_object(output_grid, pixels, frame_color=3, interior_color=1)
             if interior_pixels:
                 green_frame_blue_interior_obj = {'frame_pixels': pixels, 'interior_pixels': interior_pixels, 'bbox': obj['bbox']}
                 # This green frame object is NOT a source
             else:
                 # It's a solid green object (or green but not framing blue)
                 solid_green_objects.append(obj)
                 potential_sources.append(obj) # Initially add solid green as potential source
        else:
            potential_sources.append(obj) # Other colors are potential sources


    # --- Handle Anomaly (train_2 case) ---
    anomaly_handled = False
    if green_frame_blue_interior_obj and solid_green_objects:
        # Find the specific solid green object to change (if multiple, take the first found)
        # We need to remove *this specific* green object from potential_sources
        obj_to_change = solid_green_objects[0]
        
        # Check if obj_to_change is actually in potential_sources before removing
        original_sources_count = len(potential_sources)
        potential_sources = [s for s in potential_sources if s['pixels'] != obj_to_change['pixels']]
        
        if len(potential_sources) < original_sources_count: # Check if removal happened
            # Change the color of the solid green object to blue in the output grid
            for r, c in obj_to_change['pixels']:
                output_grid[r, c] = 1 # Change to Blue
            anomaly_handled = True
            # print(f"Anomaly handled: Changed solid green object to blue. Removed from sources.")
        # else:
            # print(f"Anomaly condition met, but solid green object not found in potential sources? obj: {obj_to_change}")


    # --- Handle Standard Transformations ---
    # Sort targets and remaining sources by bounding box (top-row, then left-col)
    targets.sort(key=lambda o: (o['bbox'][0], o['bbox'][1]))
    potential_sources.sort(key=lambda o: (o['bbox'][0], o['bbox'][1]))

    # Filter out the green frame if it existed (it was never added or already removed if anomaly triggered)
    # This filtering step might be redundant given the logic above, but ensures correctness.
    final_sources = []
    for src in potential_sources:
        is_green_frame = green_frame_blue_interior_obj and src['pixels'] == green_frame_blue_interior_obj['frame_pixels']
        # Also ensure the anomaly-swapped green object isn't reconsidered as a source if logic failed above
        is_swapped_green = anomaly_handled and src['color'] == 3 and src['pixels'] == solid_green_objects[0]['pixels']

        if not is_green_frame and not is_swapped_green:
             final_sources.append(src)


    # Perform the color replacement based on sorted lists
    if len(targets) == len(final_sources):
        # print(f"Matching {len(targets)} targets to {len(final_sources)} sources.")
        for i in range(len(targets)):
            target = targets[i]
            source = final_sources[i]
            new_color = source['color']
            # print(f"Target {i} (bbox {target['bbox']}) paired with Source {i} (color {new_color}, bbox {source['bbox']})")

            for r, c in target['interior_pixels']:
                # Check if the pixel is still blue (relevant if multiple targets overlap?)
                if output_grid[r,c] == 1:
                    output_grid[r, c] = new_color
    # else:
        # print(f"Warning: Mismatch between number of targets ({len(targets)}) and final sources ({len(final_sources)}).")
        # print("Targets:", [t['bbox'] for t in targets])
        # print("Sources:", [(s['color'], s['bbox']) for s in final_sources])


    return output_grid
```