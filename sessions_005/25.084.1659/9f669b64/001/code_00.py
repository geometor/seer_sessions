import numpy as np
from collections import Counter, defaultdict
import sys

# Set higher recursion depth for deep object searches if needed, though BFS is preferred.
# sys.setrecursionlimit(2000) 

"""
Identifies three non-background objects in the input grid: stable, moving, and split.
The moving object is typically positioned between the other two along one axis.
It moves towards the nearest grid edge along the axis perpendicular to the alignment with the other objects.
As it moves, it effectively splits the object it moves towards (the split object) into two halves.
The split occurs along an axis perpendicular to the moving object's direction of travel.
A gap is created in the split object, matching the dimension of the moving object along the split axis.
The two halves of the split object are shifted outwards from this gap, each by half the gap's dimension.
The moving object ends up positioned at the edge it moved towards, aligned with its original position along the axis parallel to its movement.
The stable object remains unchanged.
The output grid is composed of the stable object in its original place, the two pieces of the split object in their new shifted positions, and the moving object in its final position at the edge, all on the original background color.
"""

def find_objects(grid, background_color):
    """
    Finds contiguous objects of the same color in the grid.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color to ignore.

    Returns:
        dict: A dictionary where keys are colors (int) and values are lists of sets,
              each set containing (row, col) tuples for a distinct object of that color.
              Example: {1: [{(0,0), (0,1)}, {(2,2)}], 2: [{(1,1)}]}
    """
    objects = defaultdict(list)
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != background_color:
                color = grid[r, c]
                obj_pixels = set()
                q = [(r, c)]
                visited[r, c] = True
                
                while q:
                    row, col = q.pop(0)
                    obj_pixels.add((row, col))

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
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
    
    center_r = (min_r + max_r) / 2
    center_c = (min_c + max_c) / 2
    
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
    Applies the identified transformation rule to the input grid.
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

    if len(all_objects) != 3:
        # This specific task assumes exactly 3 objects besides background
        print(f"Warning: Expected 3 objects, found {len(all_objects)}. Returning input.")
        return input_grid 

    # 3. Identify roles: stable, moving, split
    # Hypothesis: Moving object's center is between the other two along one axis.
    moving_obj, stable_obj, split_obj = None, None, None
    identified_axis = None # 'row' or 'col' where the mover is between others

    for i in range(3):
        potential_mover = all_objects[i]
        others = [all_objects[j] for j in range(3) if i != j]
        obj_a, obj_b = others[0], others[1]

        # Check if mover is between a and b vertically
        mover_r, mover_c = potential_mover['center']
        a_r, a_c = obj_a['center']
        b_r, b_c = obj_b['center']

        is_between_rows = (a_r < mover_r < b_r) or (b_r < mover_r < a_r)
        # Check rough alignment horizontally (centers are relatively close, or bboxes overlap)
        cols_overlap = max(potential_mover['bbox'][1], obj_a['bbox'][1], obj_b['bbox'][1]) - \
                       min(potential_mover['bbox'][3], obj_a['bbox'][3], obj_b['bbox'][3]) <= (potential_mover['width'] + obj_a['width'] + obj_b['width']) # A loose check

        if is_between_rows and cols_overlap: # Found potential vertical alignment
            moving_obj = potential_mover
            # Determine which is split and stable based on which side the mover is likely to move (towards nearest edge HORIZONTALLY)
            dist_left = moving_obj['bbox'][1]
            dist_right = cols - 1 - moving_obj['bbox'][3]
            if dist_left < dist_right: # Moving left
                split_obj = obj_a if a_c < b_c else obj_b 
                stable_obj = obj_b if a_c < b_c else obj_a
            else: # Moving right
                split_obj = obj_a if a_c > b_c else obj_b
                stable_obj = obj_b if a_c > b_c else obj_a
            identified_axis = 'row' # Mover is between others along row axis
            break 

        # Check if mover is between a and b horizontally
        is_between_cols = (a_c < mover_c < b_c) or (b_c < mover_c < a_c)
        # Check rough alignment vertically
        rows_overlap = max(potential_mover['bbox'][0], obj_a['bbox'][0], obj_b['bbox'][0]) - \
                       min(potential_mover['bbox'][2], obj_a['bbox'][2], obj_b['bbox'][2]) <= (potential_mover['height'] + obj_a['height'] + obj_b['height'])

        if is_between_cols and rows_overlap: # Found potential horizontal alignment
            moving_obj = potential_mover
             # Determine which is split and stable based on which side the mover is likely to move (towards nearest edge VERTICALLY)
            dist_up = moving_obj['bbox'][0]
            dist_down = rows - 1 - moving_obj['bbox'][2]
            if dist_up < dist_down: # Moving up
                 split_obj = obj_a if a_r < b_r else obj_b
                 stable_obj = obj_b if a_r < b_r else obj_a
            else: # Moving down
                 split_obj = obj_a if a_r > b_r else obj_b
                 stable_obj = obj_b if a_r > b_r else obj_a
            identified_axis = 'col' # Mover is between others along col axis
            break

    if not moving_obj:
        # Fallback or error if roles couldn't be identified
        print("Warning: Could not identify object roles based on position. Returning input.")
        return input_grid
        
    # 4. Determine movement direction
    mover_min_r, mover_min_c, mover_max_r, mover_max_c = moving_obj['bbox']
    direction = None
    if identified_axis == 'row': # Mover between others vertically, so moves horizontally
        dist_left = mover_min_c
        dist_right = cols - 1 - mover_max_c
        direction = 'Left' if dist_left <= dist_right else 'Right'
    elif identified_axis == 'col': # Mover between others horizontally, so moves vertically
        dist_up = mover_min_r
        dist_down = rows - 1 - mover_max_r
        direction = 'Up' if dist_up <= dist_down else 'Down'
    else:
         # Should not happen if roles were identified correctly
         print("Error: Could not determine movement direction.")
         return input_grid


    # 5. Determine split axis (perpendicular to movement)
    split_axis = 'Vertical' if direction in ['Left', 'Right'] else 'Horizontal'

    # 6. Calculate gap size and location based on MOVER's original position
    gap_dim = 0
    gap_indices = set()
    if split_axis == 'Horizontal':
        gap_dim = moving_obj['width']
        gap_indices = set(range(mover_min_c, mover_max_c + 1)) # Columns defining the gap
    else: # Vertical split
        gap_dim = moving_obj['height']
        gap_indices = set(range(mover_min_r, mover_max_r + 1)) # Rows defining the gap
        
    if gap_dim == 0:
         print("Error: Calculated gap dimension is zero.")
         return input_grid

    # 7. Calculate shift distance (integer division)
    # Need careful handling if gap_dim is odd, but examples suggest even dimensions.
    # Let's assume integer division works as intended by the task design.
    shift = gap_dim // 2 
    if shift == 0 and gap_dim == 1: # Handle single-pixel dimension gap
        shift = 1 # Split by pushing one side by 1

    # 8. Initialize output grid
    output_grid = np.full_like(input_np, background_color)

    # 9. Draw stable object
    for r, c in stable_obj['pixels']:
        output_grid[r, c] = stable_obj['color']

    # 10. Draw split object pieces
    split_color = split_obj['color']
    for r, c in split_obj['pixels']:
        nr, nc = r, c
        if split_axis == 'Horizontal':
            min_gap_idx = min(gap_indices)
            max_gap_idx = max(gap_indices)
            if c < min_gap_idx: # Pixel is to the left of the gap
                nc = c - shift
            elif c > max_gap_idx: # Pixel is to the right of the gap
                nc = c + shift
            # Pixels originally *in* the gap area are removed (not drawn)
            else: 
                continue 
        else: # Vertical split
            min_gap_idx = min(gap_indices)
            max_gap_idx = max(gap_indices)
            if r < min_gap_idx: # Pixel is above the gap
                nr = r - shift
            elif r > max_gap_idx: # Pixel is below the gap
                nr = r + shift
            # Pixels originally *in* the gap area are removed
            else:
                continue
        
        # Draw pixel if within bounds
        if 0 <= nr < rows and 0 <= nc < cols:
            output_grid[nr, nc] = split_color

    # 11. Calculate final position of moving object at the edge
    final_r, final_c = -1, -1
    mover_h, mover_w = moving_obj['height'], moving_obj['width']
    mover_color = moving_obj['color']

    if direction == 'Up':
        final_r, final_c = 0, mover_min_c
    elif direction == 'Down':
        final_r, final_c = rows - mover_h, mover_min_c
    elif direction == 'Left':
        final_r, final_c = mover_min_r, 0
    elif direction == 'Right':
        final_r, final_c = mover_min_r, cols - mover_w
        
    # 12. Draw moving object at its final position
    for r_offset in range(mover_h):
        for c_offset in range(mover_w):
            # Check if the relative position corresponds to an original pixel of the mover
            original_pixel = (mover_min_r + r_offset, mover_min_c + c_offset)
            if original_pixel in moving_obj['pixels']:
                 target_r, target_c = final_r + r_offset, final_c + c_offset
                 if 0 <= target_r < rows and 0 <= target_c < cols:
                    output_grid[target_r, target_c] = mover_color


    # 13. Convert back to list of lists
    return output_grid.tolist()