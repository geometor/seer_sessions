```python
import numpy as np
from collections import deque

"""
Identifies zones separated by yellow lines in a grid. Finds 'source' objects (non-white/blue/yellow) and 'target' objects (blue) within these zones. Maps sources to targets based on proximity rules (within the same zone, or in vertically/horizontally adjacent zones). Transfers the source object's color to its mapped target objects. Finally, removes the original source object by changing its pixels to white (0).

1.  **Identify Grid Structure:**
    *   Locate all rows composed entirely of yellow (4) pixels (horizontal separators).
    *   Locate all columns composed entirely of yellow (4) pixels (vertical separators).
    *   Use grid boundaries and separators to define rectangular zones with coordinates (zone_row, zone_col).
2.  **Identify Objects:**
    *   Within each zone, find contiguous 'source' objects (color not 0, 1, or 4) and 'target' objects (color 1).
    *   Record each object's color, pixels, zone, and initialize a 'mapped' status to false.
3.  **Determine Mappings:** Create mappings from sources to targets based on rules, marking objects as 'mapped' once used.
    *   **Rule 1 (Intra-Zone):** Map a single source to all targets within the same zone.
    *   **Rule 2 (Inter-Zone Vertical):** Map a single unmapped source in one zone to all unmapped targets in a vertically adjacent zone. Check both directions (up/down).
    *   **Rule 3 (Inter-Zone Horizontal):** Map a single unmapped source in one zone to all unmapped targets in a horizontally adjacent zone. Check both directions (left/right).
4.  **Apply Transformation:**
    *   Create a copy of the input grid.
    *   For each mapping, color the target pixels with the source color in the copied grid.
    *   For every source object that was successfully mapped, change its original pixels to white (0) in the copied grid.
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

            if obj_pixels: # Only add if pixels were found
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'bbox': (min_r, min_c, max_r, max_c),
                    'mapped': False # Initialize mapped flag
                })

    return objects


def transform(input_grid):
    """
    Applies the transformation rule based on zone mapping.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    height, width = input_grid_np.shape

    source_colors = {2, 3, 5, 6, 7, 8, 9} # All colors except white(0), blue(1), yellow(4)
    target_color = {1} # Blue
    separator_color = 4 # Yellow
    background_color = 0 # White

    # --- 1. Identify Grid Structure (Separators and Zones) ---
    h_sep_rows = [-1] + [r for r in range(height) if np.all(input_grid_np[r, :] == separator_color)] + [height]
    v_sep_cols = [-1] + [c for c in range(width) if np.all(input_grid_np[:, c] == separator_color)] + [width]

    num_zone_rows = len(h_sep_rows) - 1
    num_zone_cols = len(v_sep_cols) - 1

    zones = {} # Store zone info: bounds, sources, targets

    # --- 2. Identify Objects per Zone ---
    # Populate zones dictionary with sources and targets found in each zone
    for zr in range(num_zone_rows):
        for zc in range(num_zone_cols):
            # Define zone boundaries
            r_start, r_end = h_sep_rows[zr] + 1, h_sep_rows[zr+1]
            c_start, c_end = v_sep_cols[zc] + 1, v_sep_cols[zc+1]

            # Skip if zone is effectively empty (e.g., adjacent separators)
            if r_start >= r_end or c_start >= c_end:
                 continue

            # Create a mask for the current zone
            zone_mask = np.zeros_like(input_grid_np, dtype=bool)
            zone_mask[r_start:r_end, c_start:c_end] = True

            # Find source and target objects within this zone
            zone_sources = find_objects(input_grid_np, source_colors, zone_mask)
            zone_targets = find_objects(input_grid_np, target_color, zone_mask)

            # Store zone information if it contains objects
            if zone_sources or zone_targets:
                for obj in zone_sources:
                    obj['zone_rc'] = (zr, zc)
                    obj['type'] = 'source'
                for obj in zone_targets:
                    obj['zone_rc'] = (zr, zc)
                    obj['type'] = 'target'

                zones[(zr, zc)] = {'sources': zone_sources, 'targets': zone_targets}

    # --- 3. Determine Mappings ---
    mappings = [] # List of tuples: (source_obj, list_of_target_objs)

    # Rule 1: Intra-Zone Mapping
    for zone_rc, zone_data in zones.items():
        sources = zone_data['sources']
        targets = zone_data['targets']

        # Condition: Exactly one source and one or more targets in the zone
        if len(sources) == 1 and len(targets) > 0:
            source_obj = sources[0]
            # Check if source and targets are not already mapped
            if not source_obj['mapped'] and all(not t['mapped'] for t in targets):
                 mappings.append((source_obj, targets))
                 source_obj['mapped'] = True
                 for t in targets:
                     t['mapped'] = True

    # Rule 2: Inter-Zone Vertical Mapping
    for zc in range(num_zone_cols): # Iterate through columns
        for zr in range(num_zone_rows - 1): # Iterate through adjacent row pairs
            zone_above_rc = (zr, zc)
            zone_below_rc = (zr + 1, zc)

            # Check if both adjacent zones exist in our zones dictionary
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
                # We need to re-evaluate unmapped counts as the previous check might have changed 'mapped' status
                unmapped_sources_below_now = [s for s in sources_below if not s['mapped']]
                unmapped_targets_above_now = [t for t in targets_above if not t['mapped']]
                if len(unmapped_sources_below_now) == 1 and len(unmapped_targets_above_now) > 0:
                    source_obj = unmapped_sources_below_now[0]
                    mappings.append((source_obj, unmapped_targets_above_now))
                    source_obj['mapped'] = True
                    for t in unmapped_targets_above_now:
                        t['mapped'] = True


    # Rule 3: Inter-Zone Horizontal Mapping
    for zr in range(num_zone_rows): # Iterate through rows
        for zc in range(num_zone_cols - 1): # Iterate through adjacent column pairs
            zone_left_rc = (zr, zc)
            zone_right_rc = (zr, zc + 1)

            # Check if both adjacent zones exist
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
                # Re-evaluate unmapped counts
                unmapped_sources_right_now = [s for s in sources_right if not s['mapped']]
                unmapped_targets_left_now = [t for t in targets_left if not t['mapped']]
                if len(unmapped_sources_right_now) == 1 and len(unmapped_targets_left_now) > 0:
                    source_obj = unmapped_sources_right_now[0]
                    mappings.append((source_obj, unmapped_targets_left_now))
                    source_obj['mapped'] = True
                    for t in unmapped_targets_left_now:
                        t['mapped'] = True


    # --- 4. Apply Transformation ---
    source_pixels_to_clear = set()

    # Apply color changes to targets first
    for source_obj, target_objs in mappings:
        source_color = source_obj['color']
        # Collect pixels of this mapped source to be cleared later
        source_pixels_to_clear.update(source_obj['pixels'])
        # Apply source color to all target objects in this mapping
        for target_obj in target_objs:
            for r, c in target_obj['pixels']:
                 # Basic bounds check (though pixels should be within grid)
                 if 0 <= r < height and 0 <= c < width:
                    output_grid[r, c] = source_color

    # Clear original source pixels AFTER coloring targets
    # Iterate through the collected set of all source pixels that were part of any mapping
    for r, c in source_pixels_to_clear:
         # Basic bounds check
         if 0 <= r < height and 0 <= c < width:
            output_grid[r, c] = background_color # Set to white

    # --- 5. Output ---
    return output_grid.tolist()
```