```python
import numpy as np
from collections import Counter, defaultdict
import sys
import math

# Optional: Set higher recursion depth if deep object searches are needed,
# but BFS (implemented below) is generally preferred and avoids recursion limits.
# sys.setrecursionlimit(2000)

"""
Analyzes three non-background objects in a grid. One object (mover) is positioned between the other two along a primary axis (vertical or horizontal), and its span along the perpendicular axis overlaps with both other objects' spans along that perpendicular axis. The mover moves towards the closer of the other two objects (split_object) along the primary axis until it reaches the grid edge. The split_object is split perpendicular to the mover's path, creating a gap aligned with the mover's dimension along that perpendicular axis. The resulting pieces of the split_object are shifted away from the gap along the primary axis by ceil(mover's dimension perpendicular to path / 2). The third object (stable_object) remains unchanged. The output grid shows the stable_object, the shifted split_object pieces, and the mover at the grid edge.

Note: The rule for determining the 'split_object' (and thus direction) based on proximity might be incorrect, as suggested by Example 2. This implementation uses the proximity rule ('closer' object is the split_object). If results are inconsistent, this rule needs re-evaluation.
"""

def find_objects(grid, background_color):
    """
    Finds contiguous objects of the same color in the grid using BFS (4-way connectivity).

    Args:
        grid (np.array): The input grid.
        background_color (int): The color to ignore.

    Returns:
        dict: A dictionary where keys are colors (int) and values are lists of sets,
              each set containing (row, col) tuples for a distinct object of that color.
    """
    objects = defaultdict(list)
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != background_color:
                color = grid[r, c]
                obj_pixels = set()
                q = [(r, c)] # Use list as a queue for BFS
                visited[r, c] = True
                head = 0
                while head < len(q):
                    row, col = q[head]
                    head += 1
                    obj_pixels.add((row, col))

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if obj_pixels:
                    objects[color].append(obj_pixels)
    return objects

def get_object_properties(obj_pixels):
    """
    Calculates properties for a given set of object pixels.

    Args:
        obj_pixels (set): A set of (row, col) tuples.

    Returns:
        dict: A dictionary containing 'pixels', 'bbox' (min_r, min_c, max_r, max_c),
              'center' (center_r, center_c), 'height', 'width'. Returns None if obj_pixels is empty.
    """
    if not obj_pixels:
        return None

    rows = [r for r, c in obj_pixels]
    cols = [c for r, c in obj_pixels]

    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)

    # Use geometric center of the bounding box
    center_r = (min_r + max_r) / 2.0
    center_c = (min_c + max_c) / 2.0

    height = max_r - min_r + 1
    width = max_c - min_c + 1

    return {
        'pixels': obj_pixels,
        'bbox': (min_r, min_c, max_r, max_c),
        'center': (center_r, center_c),
        'height': height,
        'width': width
    }

def check_overlap(bbox1, bbox2, axis):
    """ Checks if two bounding boxes overlap along a specified axis ('vertical' for rows, 'horizontal' for columns). """
    if axis == 'horizontal': # Check column overlap
        min1, max1 = bbox1[1], bbox1[3]
        min2, max2 = bbox2[1], bbox2[3]
    elif axis == 'vertical': # Check row overlap
        min1, max1 = bbox1[0], bbox1[2]
        min2, max2 = bbox2[0], bbox2[2]
    else:
        return False
    # Overlap exists if the interval [max(min1, min2), min(max1, max2)] is valid
    return max(min1, min2) <= min(max1, max2)


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # 1. Identify the background color (most frequent color).
    counts = Counter(input_np.flatten())
    background_color = counts.most_common(1)[0][0] if counts else 0 # Default to 0 if grid is empty

    # 2. Find all distinct, contiguous non-background objects and calculate their properties.
    objects_by_color = find_objects(input_np, background_color)
    all_objects = []
    for color, obj_list in objects_by_color.items():
        for obj_pixels in obj_list:
            props = get_object_properties(obj_pixels)
            if props:
                all_objects.append({'color': color, **props})

    # Ensure exactly three such objects exist.
    if len(all_objects) != 3:
        # print(f"Warning: Expected 3 objects, found {len(all_objects)}. Returning input.")
        return input_grid # Return original grid if rule assumption fails

    # 3. Determine the roles of the three objects (mover, split_object, stable_object) and the axis/direction of movement.
    mover = None
    stable = None
    split_obj = None
    direction = None
    movement_axis = None # 'vertical' or 'horizontal'

    for i in range(3):
        potential_mover = all_objects[i]
        others = [all_objects[j] for j in range(3) if i != j]
        obj_a, obj_b = others[0], others[1]

        mover_r, mover_c = potential_mover['center']
        mover_bbox = potential_mover['bbox']
        a_r, a_c = obj_a['center']
        a_bbox = obj_a['bbox']
        b_r, b_c = obj_b['center']
        b_bbox = obj_b['bbox']

        # a. Check for vertical alignment and horizontal overlap
        is_between_rows = (a_r < mover_r < b_r) or (b_r < mover_r < a_r)
        mover_overlaps_a_cols = check_overlap(mover_bbox, a_bbox, 'horizontal')
        mover_overlaps_b_cols = check_overlap(mover_bbox, b_bbox, 'horizontal')

        if is_between_rows and mover_overlaps_a_cols and mover_overlaps_b_cols:
            mover = potential_mover
            movement_axis = 'vertical'
            # b. Determine Split (closer) and Stable (further) based on center distance along the alignment axis
            dist_a = abs(a_r - mover_r)
            dist_b = abs(b_r - mover_r)
            if dist_a <= dist_b: # Using <= to handle equidistant cases, arbitrarily choosing A
                split_obj = obj_a
                stable = obj_b
                direction = 'Up' if a_r < mover_r else 'Down'
            else:
                split_obj = obj_b
                stable = obj_a
                direction = 'Up' if b_r < mover_r else 'Down'
            break # Roles identified

        # c. If no vertical alignment, check for horizontal alignment and vertical overlap
        is_between_cols = (a_c < mover_c < b_c) or (b_c < mover_c < a_c)
        mover_overlaps_a_rows = check_overlap(mover_bbox, a_bbox, 'vertical')
        mover_overlaps_b_rows = check_overlap(mover_bbox, b_bbox, 'vertical')

        if is_between_cols and mover_overlaps_a_rows and mover_overlaps_b_rows:
            mover = potential_mover
            movement_axis = 'horizontal'
            # d. Determine Split (closer) and Stable (further) based on center distance along the alignment axis
            dist_a = abs(a_c - mover_c)
            dist_b = abs(b_c - mover_c)
            if dist_a <= dist_b: # Using <= to handle equidistant cases
                split_obj = obj_a
                stable = obj_b
                direction = 'Left' if a_c < mover_c else 'Right'
            else:
                split_obj = obj_b
                stable = obj_a
                direction = 'Left' if b_c < mover_c else 'Right'
            break # Roles identified

    # e. If neither alignment is found, the rule may not apply.
    if not mover or not stable or not split_obj:
        # print("Warning: Could not definitively identify object roles based on alignment and overlap. Returning input.")
        return input_grid

    # 4. Create a new grid filled with the background color, matching the input dimensions.
    output_grid = np.full_like(input_np, background_color)

    # 5. Place the `stable_object` onto the new grid at its original location.
    for r, c in stable['pixels']:
        if 0 <= r < rows and 0 <= c < cols:
             output_grid[r, c] = stable['color']

    # 6. Process the `split_object` using the corrected logic.
    split_color = split_obj['color']
    mover_min_r, mover_min_c, mover_max_r, mover_max_c = mover['bbox']

    if movement_axis == 'vertical':
        # Movement is Up/Down. Split is horizontal. Gap uses mover's width. Shift is vertical.
        gap_extent = mover['width'] # Dimension along perpendicular axis (horizontal)
        shift = math.ceil(gap_extent / 2)
        gap_range = (mover_min_c, mover_max_c) # Column range for the gap

        for r, c in split_obj['pixels']:
            nr, nc = r, c
            # Check if pixel is vertically aligned with the gap
            if gap_range[0] <= c <= gap_range[1]:
                 # Determine shift direction based on mover's movement direction
                if direction == 'Up': # Mover moves Up, split pieces shift Up/Down away from center
                    if r < mover['center'][0]: # Pixel is above mover's center (relative to split obj) - shift Up
                        nr = r - shift
                    else: # Pixel is below or at mover's center - shift Down
                         nr = r + shift
                else: # direction == 'Down'. Mover moves Down.
                    if r > mover['center'][0]: # Pixel is below mover's center - shift Down
                        nr = r + shift
                    else: # Pixel is above or at mover's center - shift Up
                        nr = r - shift
            # Pixels not aligned with gap horizontally are kept in place relative to shift axis
            # No, the specification implies *all* pixels shift if they aren't removed by the gap.
            # Let's re-read: "split perpendicular ... creating a gap ... resulting pieces ... shifted away"
            # This implies two pieces are formed and both shift.

            # Let's try the new interpretation: Split perpendicular to movement. Shift parallel to movement.
            # If movement is Vertical (Up/Down), split is Horizontal.
            # Split line is related to mover's vertical position relative to split object.
            # This seems overly complex. Let's use the interpretation from YAML analysis.

            # --- Start Revised Split Logic ---
            # Split Axis: Perpendicular to Movement Axis.
            # Gap Location: Corresponds to Mover's span along the Perpendicular Axis.
            # Shift Axis: Parallel to Movement Axis.
            # Shift Amount: ceil(Mover_Dimension_Along_Perpendicular_Axis / 2).

            # Movement = Vertical (Up/Down)
            # Perpendicular Axis = Horizontal
            # Split = Vertical cut
            # Gap Range = Columns covered by mover (mover_min_c to mover_max_c)
            # Shift = Horizontal shift
            # Shift Amount = ceil(mover_width / 2)

            if c < gap_range[0]:   # Pixel is left of the gap
                nc = c - shift
            elif c > gap_range[1]: # Pixel is right of the gap
                nc = c + shift
            else: # Pixel is within the horizontal range of the gap, discard it
                continue # Discard pixel within the gap columns

            # Draw shifted pixel if within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                output_grid[nr, nc] = split_color
            # --- End Revised Split Logic ---


    else: # movement_axis == 'horizontal'
        # Movement is Left/Right. Split is vertical. Gap uses mover's height. Shift is horizontal.
        gap_extent = mover['height'] # Dimension along perpendicular axis (vertical)
        shift = math.ceil(gap_extent / 2)
        gap_range = (mover_min_r, mover_max_r) # Row range for the gap

        for r, c in split_obj['pixels']:
            nr, nc = r, c

            # --- Start Revised Split Logic ---
            # Movement = Horizontal (Left/Right)
            # Perpendicular Axis = Vertical
            # Split = Horizontal cut
            # Gap Range = Rows covered by mover (mover_min_r to mover_max_r)
            # Shift = Vertical shift
            # Shift Amount = ceil(mover_height / 2)

            if r < gap_range[0]:   # Pixel is above the gap
                nr = r - shift
            elif r > gap_range[1]: # Pixel is below the gap
                nr = r + shift
            else: # Pixel is within the vertical range of the gap, discard it
                continue # Discard pixel within the gap rows

            # Draw shifted pixel if within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                output_grid[nr, nc] = split_color
            # --- End Revised Split Logic ---


    # 7. Determine the final position of the `mover` object at the grid edge.
    mover_color = mover['color']
    mover_h = mover['height']
    mover_w = mover['width']
    mover_orig_min_r, mover_orig_min_c = mover['bbox'][0], mover['bbox'][1]
    final_min_r, final_min_c = -1, -1 # Top-left corner of the mover's final bbox

    if direction == 'Up':
        final_min_r, final_min_c = 0, mover_orig_min_c # Top edge, same columns
    elif direction == 'Down':
        final_min_r, final_min_c = rows - mover_h, mover_orig_min_c # Bottom edge, same columns
    elif direction == 'Left':
        final_min_r, final_min_c = mover_orig_min_r, 0 # Left edge, same rows
    elif direction == 'Right':
        final_min_r, final_min_c = mover_orig_min_r, cols - mover_w # Right edge, same rows
    else:
         # Should not happen if roles/direction were identified
         # print("Error: Invalid movement direction determined.")
         return input_grid # Or raise error

    # 8. Draw the `mover` object onto the new grid at its calculated final position.
    # Iterate through the original relative coordinates within the mover's bbox
    for r_offset in range(mover_h):
        for c_offset in range(mover_w):
            # Check if this relative position corresponds to an actual pixel of the mover
            original_pixel = (mover_orig_min_r + r_offset, mover_orig_min_c + c_offset)
            if original_pixel in mover['pixels']:
                # Calculate target position in the output grid
                target_r = final_min_r + r_offset
                target_c = final_min_c + c_offset
                # Draw if within bounds
                if 0 <= target_r < rows and 0 <= target_c < cols:
                    output_grid[target_r, target_c] = mover_color

    # 9. Return the new grid.
    return output_grid.tolist()
```