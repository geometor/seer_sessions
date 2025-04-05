
Previous Code:
```python
import numpy as np
from collections import deque

"""
Identifies connected components (objects) of non-zero pixels in a 2D grid.
Classifies objects as 'enclosed' (surrounded entirely by background '0') or 'static'.
Assumes exactly one 'enclosed' object (the 'mover').
Finds the 'static' object ('target') whose bounding box is closest to the 'mover's bounding box.
Calculates the movement vector (dx, dy) required to shift the 'mover' so that its bounding box touches the 'target's bounding box along the axis (horizontal or vertical) where they were initially closest (smallest non-negative gap).
Creates an output grid where the 'mover' object is shifted by the calculated vector, and all 'static' objects remain in their original positions.
"""

def get_neighbors(r, c, H, W, include_diagonal=False):
    """Gets valid neighbor coordinates."""
    neighbors = []
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue
            if not include_diagonal and abs(dr) + abs(dc) != 1:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W:
                neighbors.append((nr, nc))
    return neighbors

def get_bounding_box(pixels):
    """Calculates the bounding box of a set of pixels."""
    if not pixels:
        return None
    min_r = min(r for r, c in pixels)
    max_r = max(r for r, c in pixels)
    min_c = min(c for r, c in pixels)
    max_c = max(c for r, c in pixels)
    return (min_r, max_r, min_c, max_c)

def find_objects(grid):
    """Finds all connected components of non-zero pixels."""
    H, W = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(H):
        for c in range(W):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    curr_r, curr_c = q.popleft()
                    if grid[curr_r, curr_c] == color: # Check color match
                        obj_pixels.add((curr_r, curr_c))
                        # Check orthogonal neighbors for expansion
                        for nr, nc in get_neighbors(curr_r, curr_c, H, W, include_diagonal=False):
                            if not visited[nr, nc] and grid[nr, nc] == color:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                    # Mark visited even if color doesn't match to avoid reprocessing
                    # But only add to object if color matches
                    # This handles cases where BFS starts on a cell adjacent but not part of the object color
                    # Let's refine: only add matching color neighbors to queue
                    # The initial check `grid[r, c] != 0 and not visited[r, c]` ensures we start a new object search correctly.
                
                # BFS refinement to ensure correct object extraction
                obj_pixels = set()
                q = deque([(r, c)])
                visited_bfs = set([(r, c)]) # Visited for this specific BFS run

                while q:
                    curr_r, curr_c = q.popleft()
                    obj_pixels.add((curr_r, curr_c))
                    visited[curr_r, curr_c] = True # Mark globally visited

                    for nr, nc in get_neighbors(curr_r, curr_c, H, W, include_diagonal=False):
                        if grid[nr, nc] == color and (nr, nc) not in visited_bfs:
                            visited_bfs.add((nr, nc))
                            q.append((nr, nc))


                if obj_pixels:
                    bbox = get_bounding_box(obj_pixels)
                    objects.append({
                        'color': color,
                        'pixels': obj_pixels,
                        'bbox': bbox
                    })
    return objects

def is_enclosed(obj, grid):
    """Checks if an object is entirely surrounded by background (0)."""
    H, W = grid.shape
    obj_pixels = obj['pixels']
    for r, c in obj_pixels:
        # Check all 8 neighbors
        for nr, nc in get_neighbors(r, c, H, W, include_diagonal=True):
            if (nr, nc) not in obj_pixels and grid[nr, nc] != 0:
                return False  # Found a non-background neighbor outside the object
    return True

def calculate_bbox_gaps(bbox1, bbox2):
    """Calculates the horizontal and vertical gaps between two bounding boxes."""
    r_min1, r_max1, c_min1, c_max1 = bbox1
    r_min2, r_max2, c_min2, c_max2 = bbox2

    # Vertical Gap (gap_y)
    if r_max1 < r_min2:  # bbox1 is strictly above bbox2
        gap_y = r_min2 - r_max1 - 1
    elif r_max2 < r_min1:  # bbox2 is strictly above bbox1
        gap_y = r_min1 - r_max2 - 1
    else:  # Bounding boxes overlap vertically
        gap_y = -1

    # Horizontal Gap (gap_x)
    if c_max1 < c_min2:  # bbox1 is strictly left of bbox2
        gap_x = c_min2 - c_max1 - 1
    elif c_max2 < c_min1:  # bbox2 is strictly left of bbox1
        gap_x = c_min1 - c_max2 - 1
    else:  # Bounding boxes overlap horizontally
        gap_x = -1

    return gap_x, gap_y

def calculate_shift(mover_obj, target_obj):
    """Calculates the shift (dx, dy) to make mover bbox touch target bbox along the minimum gap axis."""
    mover_bbox = mover_obj['bbox']
    target_bbox = target_obj['bbox']
    gap_x, gap_y = calculate_bbox_gaps(mover_bbox, target_bbox)

    r_min_m, r_max_m, c_min_m, c_max_m = mover_bbox
    r_min_t, r_max_t, c_min_t, c_max_t = target_bbox

    dx, dy = 0, 0

    # Determine primary movement axis based on smallest non-negative gap
    move_horizontally = False
    move_vertically = False

    if gap_x >= 0 and (gap_y < 0 or gap_x <= gap_y):
        move_horizontally = True
    elif gap_y >= 0 and (gap_x < 0 or gap_y < gap_x):
        move_vertically = True
    # If both gaps are negative or zero, no movement needed based on this logic

    # Calculate shift based on axis and relative position
    if move_horizontally:
        if c_max_m < c_min_t:  # Mover is left of target
            dx = gap_x
        elif c_min_m > c_max_t:  # Mover is right of target
            dx = -gap_x
        dy = 0
    elif move_vertically:
        if r_max_m < r_min_t:  # Mover is above target
            dy = gap_y
        elif r_min_m > r_max_t:  # Mover is below target
            dy = -gap_y
        dx = 0

    return dx, dy


def transform(input_grid):
    """
    Applies the transformation rule: finds the enclosed object, finds the closest static object,
    and moves the enclosed object until its bounding box touches the static object's bounding box
    along the axis of the smallest initial gap.
    """
    input_grid_np = np.array(input_grid)
    H, W = input_grid_np.shape
    
    # 1. Find all objects
    objects = find_objects(input_grid_np)
    if not objects:
        return input_grid # Return original if no objects found

    # 2. Classify objects
    mover_obj = None
    static_objs = []
    for obj in objects:
        if is_enclosed(obj, input_grid_np):
            if mover_obj is not None:
                 # Assumption violated: more than one enclosed object
                 # Handle error or default behavior (e.g., use the first one)
                 print("Warning: Multiple enclosed objects found. Using the first one.")
            mover_obj = obj
        else:
            static_objs.append(obj)

    # Check assumptions
    if mover_obj is None:
        # print("Warning: No enclosed object found.")
        return input_grid # No object to move
    if not static_objs:
        # print("Warning: No static object found.")
        return input_grid # No target to move towards

    # 3. Find the target static object (closest to mover)
    target_obj = None
    min_dist_sq = float('inf') # Use squared distance to avoid sqrt

    for static_obj in static_objs:
        gap_x, gap_y = calculate_bbox_gaps(mover_obj['bbox'], static_obj['bbox'])
        
        dist_sq = 0
        if gap_x >= 0 and gap_y >= 0:
             # Treat gaps as distances along axes for comparison
             # We want the minimum *gap*, not Euclidean distance here.
             # Let's find the object with the minimum non-negative gap sum,
             # prioritizing the smallest single gap.
             # Simpler: choose the target based on smallest non-negative gap.
             current_min_gap = float('inf')
             if gap_x >=0: current_min_gap = min(current_min_gap, gap_x)
             if gap_y >=0: current_min_gap = min(current_min_gap, gap_y)
             
             if current_min_gap < min_dist_sq: # Using min_dist_sq to store min_gap now
                 min_dist_sq = current_min_gap
                 target_obj = static_obj
        elif gap_x >= 0: # Only horizontal gap is non-negative
             if gap_x < min_dist_sq:
                 min_dist_sq = gap_x
                 target_obj = static_obj
        elif gap_y >= 0: # Only vertical gap is non-negative
             if gap_y < min_dist_sq:
                 min_dist_sq = gap_y
                 target_obj = static_obj
        else: # Both gaps negative (overlap) - considered distance 0
             if 0 < min_dist_sq: # Prioritize overlapping? Or closest non-overlapping?
                 # Let's prioritize smallest positive gap first. Overlap means 0 gap.
                 # If no positive gaps found yet, an overlapping one becomes the target.
                 if min_dist_sq == float('inf'):
                     min_dist_sq = 0 
                     target_obj = static_obj


    # If target_obj is still None (e.g., only overlapping objects found, and initial min_dist_sq was inf)
    # Pick the first static object as default, though this case shouldn't happen based on examples.
    if target_obj is None and static_objs:
        target_obj = static_objs[0]
        print("Warning: Could not determine closest static object based on gaps, defaulting.")
        
    if target_obj is None: # Should not happen if static_objs is not empty
        return input_grid

    # 4. Calculate shift (dx, dy)
    dx, dy = calculate_shift(mover_obj, target_obj)

    # 5. Apply movement
    output_grid = np.copy(input_grid_np)

    # Erase mover from original position
    for r, c in mover_obj['pixels']:
        output_grid[r, c] = 0

    # Draw mover in new position
    mover_color = mover_obj['color']
    for r, c in mover_obj['pixels']:
        new_r, new_c = r + dy, c + dx
        # Check bounds before drawing
        if 0 <= new_r < H and 0 <= new_c < W:
            output_grid[new_r, new_c] = mover_color
        else:
            # Part of the object moved out of bounds - handle as needed
            # For this problem, seems unlikely based on examples, but good practice
            print(f"Warning: Pixel ({r},{c}) moved out of bounds to ({new_r},{new_c})")

    return output_grid.tolist() # Return as list of lists
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2
0 0 3 3 3 3 0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 3 0 0 3 0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 3 0 0 3 0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 3 3 3 3 0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 3 3 3 3 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 3 0 0 3 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 3 0 0 3 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 3 3 3 3 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2
0 0 3 3 3 3 0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 3 0 0 3 0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 3 0 0 3 0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 3 3 3 3 0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 24
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 12.63157894736841

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 4 4 4 4 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0
0 4 4 4 4 4 4 4 4 4 4 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 4 4 4 4 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 8
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 4.761904761904773

Test Set Results:

## Example 1:
Input:
```
0 0 8 8 8 0 0 0 0 7 7 7 7 7 7 7 0 0 0 0
0 0 8 0 8 0 0 0 0 7 0 0 0 0 0 7 0 0 0 0
0 0 8 8 8 0 0 0 0 7 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 8 8 8 7 7 7 7 7 7 7 0 0 0 0
0 0 0 0 0 0 8 0 8 7 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 8 8 8 7 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0 0 0 0
```
Transformed Output:
```
0 0 8 8 8 0 0 0 0 7 7 7 7 7 7 7 0 0 0 0
0 0 8 0 8 0 0 0 0 7 0 0 0 0 0 7 0 0 0 0
0 0 8 8 8 0 0 0 0 7 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0 0 0 0
```
Match: False
Pixels Off: 16
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 13.333333333333329

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 3 0 0 0 0 0 0
3 0 0 0 0 0 0 0 3 0 0 0 0 0 0
0 3 0 0 0 0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 3 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 3 0 0 0 0 0 0
3 0 0 0 0 0 0 0 3 0 0 0 0 0 0
0 3 0 0 0 0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 3 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 3 0 0 0 0 0 0
3 0 0 0 0 0 0 0 3 0 0 0 0 0 0
0 3 0 0 0 0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 3 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 32
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 14.222222222222229

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 6 0 0
0 0 0 1 1 1 0 0 0 0 0 6 0 0 0 0 6 0 0
0 0 0 1 0 1 0 0 0 0 0 6 0 0 0 0 6 0 0
0 0 0 1 1 1 0 0 0 0 0 6 0 0 0 0 6 6 6
0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 1 1 1 6 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 1 0 1 6 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 1 1 1 6 0 0 0 0 6 6 6
0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 6 0 0
0 0 0 1 1 1 0 0 0 0 0 6 0 0 0 0 6 0 0
0 0 0 1 0 1 0 0 0 0 0 6 0 0 0 0 6 0 0
0 0 0 1 1 1 0 0 0 0 0 6 0 0 0 0 6 6 6
0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 16
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 7.655502392344488
