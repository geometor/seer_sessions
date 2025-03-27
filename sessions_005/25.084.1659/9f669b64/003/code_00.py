import numpy as np
from collections import Counter, defaultdict
import sys
import math

# Optional: Set higher recursion depth if deep object searches are needed,
# but BFS (implemented below) is generally preferred and avoids recursion limits.
# sys.setrecursionlimit(2000)

"""
Identifies three non-background objects aligned along a primary axis (vertical or horizontal).
One object (mover) is positioned between the other two.
The mover moves towards the closer of the other two objects (the split object), continuing to the nearest grid edge along that path.
The split object is divided perpendicular to the mover's path.
A gap is created in the split object, matching the mover's dimension along the split axis.
The pieces of the split object shift away from this gap.
The third object (stable) remains unchanged.
The output grid contains the stable object, the shifted pieces of the split object, and the mover at its final position on the edge.
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

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # 1. Find background color (most frequent color)
    background_color = Counter(input_np.flatten()).most_common(1)[0][0]

    # 2. Find all distinct objects and their properties
    objects_by_color = find_objects(input_np, background_color)
    all_objects = []
    for color, obj_list in objects_by_color.items():
        for obj_pixels in obj_list:
            props = get_object_properties(obj_pixels)
            if props:
                all_objects.append({'color': color, **props})

    # 3. Validate: Ensure exactly 3 objects
    if len(all_objects) != 3:
        print(f"Warning: Expected 3 objects, found {len(all_objects)}. Returning input.")
        return input_grid

    # 4. Identify Roles (Mover, Stable, Split) and Movement Direction
    mover = None
    stable = None
    split_obj = None # Renamed from 'split' to avoid confusion with function name
    direction = None
    movement_axis = None # 'vertical' or 'horizontal'

    for i in range(3):
        potential_mover = all_objects[i]
        others = [all_objects[j] for j in range(3) if i != j]
        obj_a, obj_b = others[0], others[1]

        mover_r, mover_c = potential_mover['center']
        a_r, a_c = obj_a['center']
        b_r, b_c = obj_b['center']

        # Check for vertical alignment (mover between A and B vertically)
        # Use a small tolerance for center comparison? No, strict betweenness seems intended.
        is_between_rows = (a_r < mover_r < b_r) or (b_r < mover_r < a_r)
        # Check rough horizontal overlap (their column ranges overlap significantly)
        cols_overlap = max(potential_mover['bbox'][1], obj_a['bbox'][1], obj_b['bbox'][1]) < \
                       min(potential_mover['bbox'][3], obj_a['bbox'][3], obj_b['bbox'][3]) + 1

        if is_between_rows and cols_overlap:
            mover = potential_mover
            movement_axis = 'vertical'
            # Determine Split (closer) and Stable (further)
            dist_a = abs(a_r - mover_r)
            dist_b = abs(b_r - mover_r)
            if dist_a < dist_b:
                split_obj = obj_a
                stable = obj_b
            else:
                split_obj = obj_b
                stable = obj_a
            # Determine direction towards split object
            direction = 'Up' if split_obj['center'][0] < mover_r else 'Down'
            break # Roles identified

        # Check for horizontal alignment (mover between A and B horizontally)
        is_between_cols = (a_c < mover_c < b_c) or (b_c < mover_c < a_c)
        # Check rough vertical overlap
        rows_overlap = max(potential_mover['bbox'][0], obj_a['bbox'][0], obj_b['bbox'][0]) < \
                       min(potential_mover['bbox'][2], obj_a['bbox'][2], obj_b['bbox'][2]) + 1

        if is_between_cols and rows_overlap:
            mover = potential_mover
            movement_axis = 'horizontal'
            # Determine Split (closer) and Stable (further)
            dist_a = abs(a_c - mover_c)
            dist_b = abs(b_c - mover_c)
            if dist_a < dist_b:
                split_obj = obj_a
                stable = obj_b
            else:
                split_obj = obj_b
                stable = obj_a
             # Determine direction towards split object
            direction = 'Left' if split_obj['center'][1] < mover_c else 'Right'
            break # Roles identified

    if not mover or not stable or not split_obj:
        print("Warning: Could not definitively identify object roles based on alignment and proximity. Returning input.")
        return input_grid

    # 5. Create the Output Grid
    output_grid = np.full_like(input_np, background_color)

    # 6. Place the Stable Object
    for r, c in stable['pixels']:
        # Check bounds just in case, though should be original position
        if 0 <= r < rows and 0 <= c < cols:
             output_grid[r, c] = stable['color']

    # 7. Perform the Split and Shift on the Split Object
    split_color = split_obj['color']
    split_axis = 'Horizontal' if movement_axis == 'vertical' else 'Vertical'
    mover_min_r, mover_min_c, mover_max_r, mover_max_c = mover['bbox']

    if split_axis == 'Horizontal':
        gap_dim = mover['width']
        # Columns covered by the mover's bounding box define the gap
        gap_indices = range(mover_min_c, mover_max_c + 1)
        min_gap_idx = min(gap_indices)
        max_gap_idx = max(gap_indices)
        shift = (gap_dim + 1) // 2 # Integer division, handles odd gaps slightly better

        for r, c in split_obj['pixels']:
            nr, nc = r, c
            if c < min_gap_idx:   # Pixel is left of the gap
                nc = c - shift
            elif c > max_gap_idx: # Pixel is right of the gap
                nc = c + shift
            else: # Pixel is within the horizontal range of the gap, remove it
                continue

            # Draw shifted pixel if within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                output_grid[nr, nc] = split_color

    else: # Vertical split
        gap_dim = mover['height']
        # Rows covered by the mover's bounding box define the gap
        gap_indices = range(mover_min_r, mover_max_r + 1)
        min_gap_idx = min(gap_indices)
        max_gap_idx = max(gap_indices)
        shift = (gap_dim + 1) // 2

        for r, c in split_obj['pixels']:
            nr, nc = r, c
            if r < min_gap_idx:   # Pixel is above the gap
                nr = r - shift
            elif r > max_gap_idx: # Pixel is below the gap
                nr = r + shift
            else: # Pixel is within the vertical range of the gap, remove it
                continue

            # Draw shifted pixel if within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                output_grid[nr, nc] = split_color

    # 8. Place the Mover Object at the Target Edge
    mover_color = mover['color']
    mover_h = mover['height']
    mover_w = mover['width']
    final_min_r, final_min_c = -1, -1 # Top-left corner of the mover's final bbox

    if direction == 'Up':
        final_min_r, final_min_c = 0, mover_min_c
    elif direction == 'Down':
        final_min_r, final_min_c = rows - mover_h, mover_min_c
    elif direction == 'Left':
        final_min_r, final_min_c = mover_min_r, 0
    elif direction == 'Right':
        final_min_r, final_min_c = mover_min_r, cols - mover_w
    else:
         # Should not happen if roles/direction were identified
         print("Error: Invalid movement direction determined.")
         return input_grid # Or raise error

    # Copy mover pixels relative to its final position
    # Iterate through the original relative coordinates within the mover's bbox
    for r_offset in range(mover_h):
        for c_offset in range(mover_w):
            # Check if this relative position corresponds to an actual pixel of the mover
            original_pixel = (mover_min_r + r_offset, mover_min_c + c_offset)
            if original_pixel in mover['pixels']:
                # Calculate target position in the output grid
                target_r = final_min_r + r_offset
                target_c = final_min_c + c_offset
                # Draw if within bounds
                if 0 <= target_r < rows and 0 <= target_c < cols:
                    output_grid[target_r, target_c] = mover_color

    # 9. Convert back to list of lists and return
    return output_grid.tolist()