
Previous Code:
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
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 4 0 0 0 4 0 0 0
0 3 0 4 0 2 0 4 0 6 0
0 0 0 4 0 0 0 4 0 0 0
4 4 4 4 4 4 4 4 4 4 4
1 0 0 4 0 1 0 4 1 0 1
0 1 0 4 1 1 1 4 1 0 1
1 1 1 4 1 0 1 4 0 1 0
```
Expected Output:
```
0 0 0 4 0 0 0 4 0 0 0
0 3 0 4 0 2 0 4 0 6 0
0 0 0 4 0 0 0 4 0 0 0
4 4 4 4 4 4 4 4 4 4 4
3 0 0 4 0 2 0 4 6 0 6
0 3 0 4 2 2 2 4 6 0 6
3 3 3 4 2 0 2 4 0 6 0
```
Transformed Output:
```
0 0 0 4 0 0 0 4 0 0 0
0 0 0 4 0 0 0 4 0 0 0
0 0 0 4 0 0 0 4 0 0 0
4 4 4 4 4 4 4 4 4 4 4
3 0 0 4 0 2 0 4 6 0 6
0 3 0 4 2 2 2 4 6 0 6
3 3 3 4 2 0 2 4 0 6 0
```
Match: False
Pixels Off: 3
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 7.79220779220779

## Example 2:
Input:
```
0 0 0 4 1 0 0
0 7 0 4 0 1 1
0 0 0 4 0 1 0
4 4 4 4 4 4 4
0 0 0 4 1 1 0
0 3 0 4 0 1 0
0 0 0 4 1 1 1
4 4 4 4 4 4 4
0 0 0 4 1 1 0
0 8 0 4 0 1 1
0 0 0 4 1 0 1
```
Expected Output:
```
0 0 0 4 7 0 0
0 7 0 4 0 7 7
0 0 0 4 0 7 0
4 4 4 4 4 4 4
0 0 0 4 3 3 0
0 3 0 4 0 3 0
0 0 0 4 3 3 3
4 4 4 4 4 4 4
0 0 0 4 8 8 0
0 8 0 4 0 8 8
0 0 0 4 8 0 8
```
Transformed Output:
```
0 0 0 4 7 0 0
0 0 0 4 0 7 7
0 0 0 4 0 7 0
4 4 4 4 4 4 4
0 0 0 4 3 3 0
0 0 0 4 0 3 0
0 0 0 4 3 3 3
4 4 4 4 4 4 4
0 0 0 4 8 8 0
0 0 0 4 0 8 8
0 0 0 4 8 0 8
```
Match: False
Pixels Off: 3
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 7.79220779220779
## General Assessment

The provided code successfully identifies the grid structure (zones separated by yellow lines), locates source objects (non-white/blue/yellow) and target objects (blue), and applies the correct color transformation from sources to targets based on the zone mapping rules (intra-zone and adjacent inter-zone). However, it incorrectly removes the original source objects by changing their pixels to white (0) after the mapping. The expected outputs clearly show that the source objects should remain unchanged in their original positions and colors.

The strategy for resolving the errors is straightforward: modify the code to prevent the removal of source objects. This involves removing the step where source pixels are identified and subsequently changed to the background color (white). The rest of the logic concerning zone identification, object finding, and target coloring appears correct based on the provided examples.

## Metrics



*code_execution:*
```python
import numpy as np

# Example 1 Data
input_grid_1 = np.array([
    [0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0],
    [0, 3, 0, 4, 0, 2, 0, 4, 0, 6, 0],
    [0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [1, 0, 0, 4, 0, 1, 0, 4, 1, 0, 1],
    [0, 1, 0, 4, 1, 1, 1, 4, 1, 0, 1],
    [1, 1, 1, 4, 1, 0, 1, 4, 0, 1, 0]
])
expected_output_1 = np.array([
    [0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0],
    [0, 3, 0, 4, 0, 2, 0, 4, 0, 6, 0],
    [0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [3, 0, 0, 4, 0, 2, 0, 4, 6, 0, 6],
    [0, 3, 0, 4, 2, 2, 2, 4, 6, 0, 6],
    [3, 3, 3, 4, 2, 0, 2, 4, 0, 6, 0]
])
transformed_output_1 = np.array([
    [0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0], # Differs here
    [0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [3, 0, 0, 4, 0, 2, 0, 4, 6, 0, 6],
    [0, 3, 0, 4, 2, 2, 2, 4, 6, 0, 6],
    [3, 3, 3, 4, 2, 0, 2, 4, 0, 6, 0]
])

diff_1 = expected_output_1 != transformed_output_1
diff_indices_1 = np.where(diff_1)
mismatched_pixels_info_1 = []
for r, c in zip(*diff_indices_1):
    mismatched_pixels_info_1.append({
        'coord': (r, c),
        'expected': expected_output_1[r, c],
        'actual': transformed_output_1[r, c],
        'input': input_grid_1[r,c]
    })

# Example 2 Data
input_grid_2 = np.array([
    [0, 0, 0, 4, 1, 0, 0],
    [0, 7, 0, 4, 0, 1, 1],
    [0, 0, 0, 4, 0, 1, 0],
    [4, 4, 4, 4, 4, 4, 4],
    [0, 0, 0, 4, 1, 1, 0],
    [0, 3, 0, 4, 0, 1, 0],
    [0, 0, 0, 4, 1, 1, 1],
    [4, 4, 4, 4, 4, 4, 4],
    [0, 0, 0, 4, 1, 1, 0],
    [0, 8, 0, 4, 0, 1, 1],
    [0, 0, 0, 4, 1, 0, 1]
])
expected_output_2 = np.array([
    [0, 0, 0, 4, 7, 0, 0],
    [0, 7, 0, 4, 0, 7, 7],
    [0, 0, 0, 4, 0, 7, 0],
    [4, 4, 4, 4, 4, 4, 4],
    [0, 0, 0, 4, 3, 3, 0],
    [0, 3, 0, 4, 0, 3, 0],
    [0, 0, 0, 4, 3, 3, 3],
    [4, 4, 4, 4, 4, 4, 4],
    [0, 0, 0, 4, 8, 8, 0],
    [0, 8, 0, 4, 0, 8, 8],
    [0, 0, 0, 4, 8, 0, 8]
])
transformed_output_2 = np.array([
    [0, 0, 0, 4, 7, 0, 0],
    [0, 0, 0, 4, 0, 7, 7], # Source 7 changed to 0
    [0, 0, 0, 4, 0, 7, 0],
    [4, 4, 4, 4, 4, 4, 4],
    [0, 0, 0, 4, 3, 3, 0],
    [0, 0, 0, 4, 0, 3, 0], # Source 3 changed to 0
    [0, 0, 0, 4, 3, 3, 3],
    [4, 4, 4, 4, 4, 4, 4],
    [0, 0, 0, 4, 8, 8, 0],
    [0, 0, 0, 4, 0, 8, 8], # Source 8 changed to 0
    [0, 0, 0, 4, 8, 0, 8]
])

diff_2 = expected_output_2 != transformed_output_2
diff_indices_2 = np.where(diff_2)
mismatched_pixels_info_2 = []
for r, c in zip(*diff_indices_2):
    mismatched_pixels_info_2.append({
        'coord': (r, c),
        'expected': expected_output_2[r, c],
        'actual': transformed_output_2[r, c],
        'input': input_grid_2[r,c]
    })

print("--- Example 1 Metrics ---")
print(f"Input Shape: {input_grid_1.shape}")
print(f"Expected Output Shape: {expected_output_1.shape}")
print(f"Transformed Output Shape: {transformed_output_1.shape}")
print(f"Match: {np.array_equal(expected_output_1, transformed_output_1)}")
print(f"Number of Mismatched Pixels: {len(mismatched_pixels_info_1)}")
print("Mismatched Pixel Details:")
for info in mismatched_pixels_info_1:
    print(f"  Coord: {info['coord']}, Expected: {info['expected']}, Actual: {info['actual']}, Input: {info['input']}")

print("\n--- Example 2 Metrics ---")
print(f"Input Shape: {input_grid_2.shape}")
print(f"Expected Output Shape: {expected_output_2.shape}")
print(f"Transformed Output Shape: {transformed_output_2.shape}")
print(f"Match: {np.array_equal(expected_output_2, transformed_output_2)}")
print(f"Number of Mismatched Pixels: {len(mismatched_pixels_info_2)}")
print("Mismatched Pixel Details:")
for info in mismatched_pixels_info_2:
    print(f"  Coord: {info['coord']}, Expected: {info['expected']}, Actual: {info['actual']}, Input: {info['input']}")
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Example 1 Metrics ---
Input Shape: (7, 11)
Expected Output Shape: (7, 11)
Transformed Output Shape: (7, 11)
Match: False
Number of Mismatched Pixels: 3
Mismatched Pixel Details:
  Coord: (np.int64(1), np.int64(1)), Expected: 3, Actual: 0, Input: 3
  Coord: (np.int64(1), np.int64(5)), Expected: 2, Actual: 0, Input: 2
  Coord: (np.int64(1), np.int64(9)), Expected: 6, Actual: 0, Input: 6

--- Example 2 Metrics ---
Input Shape: (11, 7)
Expected Output Shape: (11, 7)
Transformed Output Shape: (11, 7)
Match: False
Number of Mismatched Pixels: 3
Mismatched Pixel Details:
  Coord: (np.int64(1), np.int64(1)), Expected: 7, Actual: 0, Input: 7
  Coord: (np.int64(5), np.int64(1)), Expected: 3, Actual: 0, Input: 3
  Coord: (np.int64(9), np.int64(1)), Expected: 8, Actual: 0, Input: 8

```
## Facts


```yaml
grid_properties:
  - structure: Divided into rectangular zones by solid yellow horizontal and vertical lines.
  - background_color: white (0)
  - separator_color: yellow (4)

objects:
  - type: source
    color: Any color except white (0), blue (1), or yellow (4).
    description: Represents the origin of a color transformation.
    persistence: Remains unchanged in the output grid.
  - type: target
    color: blue (1)
    description: Represents the destination of a color transformation. Receives color from a mapped source.
  - type: separator
    color: yellow (4)
    description: Forms the boundaries of zones. Can be full rows or columns.
    persistence: Remains unchanged in the output grid.
  - type: background
    color: white (0)
    description: The default empty space within zones.
    persistence: Remains unchanged unless it's part of a target object that gets colored.

zones:
  - definition: Rectangular areas defined by grid boundaries and yellow separator lines.
  - identification: Determined by finding rows and columns composed entirely of yellow pixels.
  - properties: Each zone has coordinates (zone_row, zone_col). Contains zero or more source objects and zero or more target objects.

actions:
  - name: identify_zones
    description: Locate all horizontal and vertical yellow separators to define zone boundaries.
  - name: identify_objects
    description: Within each zone, find all contiguous source objects and target objects. Record their color, pixels, and zone location.
  - name: determine_mappings
    description: Map source objects to target objects based on specific rules, prioritizing mappings that satisfy the conditions first. Mark objects as mapped once used in a rule.
    rules:
      - rule_1_intra_zone: If a zone contains exactly one unmapped source object and one or more unmapped target objects, map that source to all those targets.
      - rule_2_inter_zone_vertical: If a zone contains exactly one unmapped source object and a vertically adjacent zone (sharing a horizontal border segment, not just a corner) contains one or more unmapped target objects, map that source to all those targets in the adjacent zone. Check both directions (source above targets, source below targets).
      - rule_3_inter_zone_horizontal: If a zone contains exactly one unmapped source object and a horizontally adjacent zone (sharing a vertical border segment, not just a corner) contains one or more unmapped target objects, map that source to all those targets in the adjacent zone. Check both directions (source left of targets, source right of targets).
  - name: apply_transformation
    description: Create a copy of the input grid. For each mapping found, change the color of all pixels belonging to the target object(s) to the color of the mapped source object. Source objects remain unchanged.

output:
  - description: The modified grid after applying the color transformations to target objects. Separators and original source objects persist.
```


## Natural Language Program

1.  **Analyze Grid Structure**: Identify all complete horizontal and vertical lines composed solely of yellow (4) pixels. These lines, along with the grid borders, define distinct rectangular zones.
2.  **Identify Objects within Zones**:
    *   For each zone:
        *   Find all contiguous groups of pixels that are not white (0), blue (1), or yellow (4). These are 'source' objects. Record their color, constituent pixel coordinates, and the zone they belong to.
        *   Find all contiguous groups of pixels that are blue (1). These are 'target' objects. Record their color (blue), constituent pixel coordinates, and the zone they belong to.
3.  **Establish Mappings**: Determine which source objects provide color for which target objects according to the following prioritized rules. Once a source or target object is used in a mapping, it cannot be used again.
    *   **Rule 1 (Intra-Zone)**: For each zone, if it contains exactly one *unmapped* source object and one or more *unmapped* target objects, map this source object to *all* those target objects within the same zone. Mark the source and target objects as mapped.
    *   **Rule 2 (Inter-Zone Vertical)**: Check pairs of vertically adjacent zones. If one zone contains exactly one *unmapped* source object and the adjacent zone contains one or more *unmapped* target objects, map the source object to *all* those target objects in the adjacent zone. Perform this check for both directions (source above targets, source below targets). Mark the involved source and target objects as mapped.
    *   **Rule 3 (Inter-Zone Horizontal)**: Check pairs of horizontally adjacent zones. If one zone contains exactly one *unmapped* source object and the adjacent zone contains one or more *unmapped* target objects, map the source object to *all* those target objects in the adjacent zone. Perform this check for both directions (source left of targets, source right of targets). Mark the involved source and target objects as mapped.
4.  **Apply Transformations**: Create a copy of the input grid. For every mapping created in step 3:
    *   Iterate through all the pixel coordinates associated with the target object(s) in the mapping.
    *   Change the color of these pixels in the copied grid to the color of the corresponding source object.
5.  **Output**: Return the modified grid. The original source objects and yellow separator lines remain unchanged from the input grid.
