import numpy as np
from collections import deque

"""
1.  **Identify Grid Structure:**
    *   Find all rows consisting entirely of yellow (4) pixels. These are horizontal separators.
    *   Find all columns consisting entirely of yellow (4) pixels. These are vertical separators.
    *   Use the grid boundaries and these separators to partition the grid into rectangular zones. Assign each zone coordinates (zone_row, zone_col).
2.  **Identify Objects:**
    *   Within each zone, identify all distinct contiguous objects.
    *   Classify objects as 'source' if their color is not white (0), blue (1), or yellow (4).
    *   Classify objects as 'target' if their color is blue (1).
    *   Store each object's color, pixels, and the zone it belongs to.
3.  **Determine Mappings:** Create a list of mappings, where each mapping connects one source object to one or more target objects. Apply the following rules in order, ensuring a source object is used only once:
    *   **Rule 1 (Intra-Zone):** For each zone, if it contains exactly one source object and one or more target objects, map that source object to all target objects within that same zone. Mark the source and targets as 'mapped'.
    *   **Rule 2 (Inter-Zone Vertical):** Check pairs of zones (Z_above, Z_below) that are in the same zone column and are directly separated by a single horizontal separator. If Z_above contains exactly one 'unmapped' source object, and Z_below contains one or more 'unmapped' target objects, map the source to all those targets. Mark the source and targets as 'mapped'. (Apply similarly if source is below and targets are above).
    *   **Rule 3 (Inter-Zone Horizontal):** Check pairs of zones (Z_left, Z_right) that are in the same zone row and are directly separated by a single vertical separator. If Z_left contains exactly one 'unmapped' source object, and Z_right contains one or more 'unmapped' target objects, map the source to all those targets. Mark the source and targets as 'mapped'. (Apply similarly if source is right and targets are left).
4.  **Apply Transformation:**
    *   Create a copy of the input grid.
    *   For every determined mapping (source S -> targets T_list): Change the color of all pixels belonging to each target T in T_list to the color of source S in the copied grid.
    *   For every source object S that was marked as 'mapped': Change the color of all pixels belonging to S to white (0) in the copied grid.
5.  **Output:** Return the modified grid.
"""

def find_objects(grid, colors_to_find, zone_mask):
    """
    Finds contiguous objects of specified colors within a masked zone of the grid.

    Args:
        grid (np.array): The input grid.
        colors_to_find (set): A set of color values to search for.
        zone_mask (np.array): A boolean mask of the same shape as grid,
                               True for pixels within the current zone.

    Returns:
        list: A list of dictionaries, each representing an object found.
              Each dictionary contains 'color', 'pixels', 'bbox', and 'mapped'.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # Skip if outside the specified zone or already visited
            if not zone_mask[r, c] or visited[r, c]:
                continue

            # Skip if not a target color for this search
            if grid[r, c] not in colors_to_find:
                continue

            color = grid[r, c]
            obj_pixels = set()
            q = deque([(r, c)])
            visited[r, c] = True
            min_r, min_c = r, c
            max_r, max_c = r, c

            while q:
                row, col = q.popleft()
                obj_pixels.add((row, col))
                min_r = min(min_r, row)
                min_c = min(min_c, col)
                max_r = max(max_r, row)
                max_c = max(max_c, col)

                # Check neighbors (4-connectivity)
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < height and 0 <= nc < width and \
                       zone_mask[nr, nc] and \
                       not visited[nr, nc] and grid[nr, nc] == color:
                        visited[nr, nc] = True
                        q.append((nr, nc))

            objects.append({
                'color': color,
                'pixels': obj_pixels,
                'bbox': (min_r, min_c, max_r, max_c),
                'mapped': False # Initialize mapped flag
            })

    return objects


def transform(input_grid):
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    source_colors = {2, 3, 5, 6, 7, 8, 9} # All colors except white, blue, yellow
    target_color = {1} # Blue

    # --- 1. Identify Grid Structure (Separators and Zones) ---
    h_sep_rows = [-1] + [r for r in range(height) if np.all(input_grid[r, :] == 4)] + [height]
    v_sep_cols = [-1] + [c for c in range(width) if np.all(input_grid[:, c] == 4)] + [width]

    num_zone_rows = len(h_sep_rows) - 1
    num_zone_cols = len(v_sep_cols) - 1

    zones = {} # Store zone info: bounds and objects

    # --- 2. Identify Objects per Zone ---
    all_objects = [] # Keep a flat list for easy access later
    for zr in range(num_zone_rows):
        for zc in range(num_zone_cols):
            r_start, r_end = h_sep_rows[zr] + 1, h_sep_rows[zr+1]
            c_start, c_end = v_sep_cols[zc] + 1, v_sep_cols[zc+1]

            if r_start >= r_end or c_start >= c_end: # Skip empty zones
                 continue

            zone_mask = np.zeros_like(input_grid, dtype=bool)
            zone_mask[r_start:r_end, c_start:c_end] = True

            zone_sources = find_objects(input_grid, source_colors, zone_mask)
            zone_targets = find_objects(input_grid, target_color, zone_mask)

            for obj in zone_sources:
                obj['zone_rc'] = (zr, zc)
                obj['type'] = 'source'
            for obj in zone_targets:
                obj['zone_rc'] = (zr, zc)
                obj['type'] = 'target'

            zones[(zr, zc)] = {'sources': zone_sources, 'targets': zone_targets}
            all_objects.extend(zone_sources)
            all_objects.extend(zone_targets)


    # --- 3. Determine Mappings ---
    mappings = [] # List of tuples: (source_obj, list_of_target_objs)
    
    # Rule 1: Intra-Zone Mapping
    for zr in range(num_zone_rows):
        for zc in range(num_zone_cols):
            zone_rc = (zr, zc)
            if zone_rc in zones:
                zone_data = zones[zone_rc]
                sources = zone_data['sources']
                targets = zone_data['targets']

                # Check for exactly one source and one or more targets
                if len(sources) == 1 and len(targets) > 0:
                    source_obj = sources[0]
                    # Ensure source and targets haven't been mapped yet
                    if not source_obj['mapped'] and all(not t['mapped'] for t in targets):
                         mappings.append((source_obj, targets))
                         source_obj['mapped'] = True
                         for t in targets:
                             t['mapped'] = True

    # Rule 2: Inter-Zone Vertical Mapping
    for zc in range(num_zone_cols): # Iterate through zone columns
        for zr in range(num_zone_rows - 1): # Iterate through adjacent zone rows
            zone_above_rc = (zr, zc)
            zone_below_rc = (zr + 1, zc)

            if zone_above_rc in zones and zone_below_rc in zones:
                sources_above = zones[zone_above_rc]['sources']
                targets_above = zones[zone_above_rc]['targets']
                sources_below = zones[zone_below_rc]['sources']
                targets_below = zones[zone_below_rc]['targets']

                # Check: 1 unmapped source above, >=1 unmapped target below
                unmapped_sources_above = [s for s in sources_above if not s['mapped']]
                unmapped_targets_below = [t for t in targets_below if not t['mapped']]
                if len(unmapped_sources_above) == 1 and len(unmapped_targets_below) > 0:
                    source_obj = unmapped_sources_above[0]
                    mappings.append((source_obj, unmapped_targets_below))
                    source_obj['mapped'] = True
                    for t in unmapped_targets_below:
                        t['mapped'] = True

                # Check: 1 unmapped source below, >=1 unmapped target above
                unmapped_sources_below = [s for s in sources_below if not s['mapped']]
                unmapped_targets_above = [t for t in targets_above if not t['mapped']]
                # Need fresh check as objects might have been mapped in previous check
                if len(unmapped_sources_below) == 1 and len(unmapped_targets_above) > 0:
                    # Re-fetch unmapped targets above, in case they were just mapped
                    unmapped_targets_above_fresh = [t for t in targets_above if not t['mapped']]
                    if len(unmapped_targets_above_fresh) > 0:
                        source_obj = unmapped_sources_below[0]
                        mappings.append((source_obj, unmapped_targets_above_fresh))
                        source_obj['mapped'] = True
                        for t in unmapped_targets_above_fresh:
                            t['mapped'] = True


    # Rule 3: Inter-Zone Horizontal Mapping
    for zr in range(num_zone_rows): # Iterate through zone rows
        for zc in range(num_zone_cols - 1): # Iterate through adjacent zone columns
            zone_left_rc = (zr, zc)
            zone_right_rc = (zr, zc + 1)

            if zone_left_rc in zones and zone_right_rc in zones:
                sources_left = zones[zone_left_rc]['sources']
                targets_left = zones[zone_left_rc]['targets']
                sources_right = zones[zone_right_rc]['sources']
                targets_right = zones[zone_right_rc]['targets']

                # Check: 1 unmapped source left, >=1 unmapped target right
                unmapped_sources_left = [s for s in sources_left if not s['mapped']]
                unmapped_targets_right = [t for t in targets_right if not t['mapped']]
                if len(unmapped_sources_left) == 1 and len(unmapped_targets_right) > 0:
                    source_obj = unmapped_sources_left[0]
                    mappings.append((source_obj, unmapped_targets_right))
                    source_obj['mapped'] = True
                    for t in unmapped_targets_right:
                        t['mapped'] = True

                # Check: 1 unmapped source right, >=1 unmapped target left
                unmapped_sources_right = [s for s in sources_right if not s['mapped']]
                unmapped_targets_left = [t for t in targets_left if not t['mapped']]
                 # Need fresh check as objects might have been mapped
                if len(unmapped_sources_right) == 1 and len(unmapped_targets_left) > 0:
                    # Re-fetch unmapped targets left
                    unmapped_targets_left_fresh = [t for t in targets_left if not t['mapped']]
                    if len(unmapped_targets_left_fresh) > 0:
                        source_obj = unmapped_sources_right[0]
                        mappings.append((source_obj, unmapped_targets_left_fresh))
                        source_obj['mapped'] = True
                        for t in unmapped_targets_left_fresh:
                            t['mapped'] = True


    # --- 4. Apply Transformation ---
    source_pixels_to_clear = set()

    # Apply color changes to targets first
    for source_obj, target_objs in mappings:
        source_color = source_obj['color']
        source_pixels_to_clear.update(source_obj['pixels']) # Collect pixels of mapped sources
        for target_obj in target_objs:
            for r, c in target_obj['pixels']:
                 if 0 <= r < height and 0 <= c < width: # Bounds check
                    output_grid[r, c] = source_color

    # Clear original source pixels AFTER coloring targets
    for r, c in source_pixels_to_clear:
         if 0 <= r < height and 0 <= c < width: # Bounds check
            output_grid[r, c] = 0 # Set to white

    # --- 5. Output ---
    return output_grid.tolist()