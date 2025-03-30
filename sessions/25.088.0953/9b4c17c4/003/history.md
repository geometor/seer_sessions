
Previous Code:
```python
import numpy as np
from collections import deque

"""
Identifies contiguous objects of color 2 (red) within distinct background regions 
(color 1 - blue or 8 - azure). For each red object, determines the horizontal 
boundaries of its containing background region. Calculates the horizontal distance 
from the object's edges to the region's left and right boundaries. Moves the 
object horizontally towards the *closer* boundary until it touches that boundary. 
The object's vertical position remains unchanged. The background regions themselves 
are static.
"""

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specified color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of sets, where each set contains the (row, col) coordinates
              of the pixels belonging to a single object.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def get_background_region_boundaries(grid, obj_coords):
    """
    Determines the background color and horizontal boundaries of the region
    containing the object.

    Args:
        grid (np.array): The input grid.
        obj_coords (set): Set of (row, col) coordinates for the object.

    Returns:
        tuple: (background_color, region_min_col, region_max_col) or
               (None, -1, -1) if background cannot be determined.
    """
    height, width = grid.shape
    
    # Find a representative point and try to find an adjacent background pixel
    start_r, start_c = next(iter(obj_coords)) # Get one coordinate from the object
    background_color = -1
    q_start_points = deque()

    # Check neighbors of all object pixels to find background color and starting points for BFS
    visited_bg_check = set() # Track pixels checked for background identification
    
    for r_obj, c_obj in obj_coords:
         for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r_obj + dr, c_obj + dc
            if 0 <= nr < height and 0 <= nc < width and (nr, nc) not in obj_coords:
                potential_bg_color = grid[nr, nc]
                if potential_bg_color != 2: # Must not be red (the object color)
                    background_color = potential_bg_color
                    # Add this neighbor as a potential starting point for region BFS
                    if (nr, nc) not in visited_bg_check:
                        q_start_points.append((nr, nc))
                        visited_bg_check.add((nr, nc))

    if background_color == -1:
        # Should not happen based on examples, but handle case where object has no non-red neighbors
        # Or object fills the entire grid? Highly unlikely. Could also happen if object touches grid edge only.
        # Let's assume background is the most common color *not* red if this fails. This is a heuristic.
         colors, counts = np.unique(grid[grid != 2], return_counts=True)
         if len(colors)>0:
              background_color = colors[np.argmax(counts)]
              # Need a starting point for BFS still if q_start_points is empty
              # This part is tricky, relies on object not touching *all* boundaries
              if not q_start_points:
                   # Find any pixel with background_color, preferably close to the object
                   # For simplicity, just find the first instance
                   bg_indices = np.argwhere(grid == background_color)
                   if len(bg_indices) > 0:
                       q_start_points.append(tuple(bg_indices[0]))
                       visited_bg_check.add(tuple(bg_indices[0]))
                   else: # No background pixels found? Error state.
                       return None, -1, -1 # Indicate error
         else: # Only red pixels in grid? Error state.
             return None, -1, -1

    if not q_start_points:
        # If we identified a background color but couldn't find a starting pixel adjacent
        # to the object (e.g., single pixel object in a corner), find any pixel of that color.
         bg_indices = np.argwhere(grid == background_color)
         if len(bg_indices) > 0:
             start_bg_pixel = tuple(bg_indices[0])
             if start_bg_pixel not in visited_bg_check:
                  q_start_points.append(start_bg_pixel)
                  visited_bg_check.add(start_bg_pixel)
         else:
              return None, -1, -1 # No pixels of this background color exist

    # BFS to find all connected background pixels
    region_coords = set()
    q = q_start_points # Use the starting points found earlier
    visited_bfs = visited_bg_check.copy() # Keep track of visited during this BFS

    while q:
        row, col = q.popleft()
        region_coords.add((row, col))

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] == background_color and (nr, nc) not in visited_bfs:
                visited_bfs.add((nr, nc))
                q.append((nr, nc))

    if not region_coords:
         # Fallback if BFS from neighbours failed to find a region.
         # This might happen if the determined background color isn't connected
         # to the object neighbours found earlier. Search entire grid for the color.
         bg_indices = np.argwhere(grid == background_color)
         if len(bg_indices) > 0:
             start_bg_pixel = tuple(bg_indices[0])
             q = deque([start_bg_pixel])
             visited_bfs = {start_bg_pixel}
             while q:
                 row, col = q.popleft()
                 region_coords.add((row, col))
                 for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                     nr, nc = row + dr, col + dc
                     if 0 <= nr < height and 0 <= nc < width and \
                        grid[nr, nc] == background_color and (nr, nc) not in visited_bfs:
                         visited_bfs.add((nr, nc))
                         q.append((nr, nc))
         else: # Really cannot find the background region
              return background_color, -1, -1 # Return color, but invalid bounds

    # Determine min/max col of the background region
    region_min_col = width
    region_max_col = -1
    for r_reg, c_reg in region_coords:
        region_min_col = min(region_min_col, c_reg)
        region_max_col = max(region_max_col, c_reg)

    if region_min_col == width: # Handle case where region was empty
        return background_color, -1, -1

    return background_color, region_min_col, region_max_col


def get_object_boundaries(obj_coords):
    """
    Finds the minimum and maximum column index occupied by the object.

    Args:
        obj_coords (set): Set of (row, col) coordinates for the object.

    Returns:
        tuple: (object_min_col, object_max_col)
    """
    if not obj_coords:
        return -1, -1
    min_col = float('inf')
    max_col = float('-inf')
    for _, c in obj_coords:
        min_col = min(min_col, c)
        max_col = max(max_col, c)
    return min_col, max_col


def transform(input_grid):
    """
    Moves red objects horizontally to the nearest vertical boundary of their
    background region.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    object_color = 2

    # Find all red objects
    red_objects = find_objects(input_np, object_color)

    for obj_coords in red_objects:
        if not obj_coords:
            continue

        # Determine the background region and its boundaries
        background_color, region_min_col, region_max_col = get_background_region_boundaries(input_np, obj_coords)

        # If region boundaries are invalid, skip this object
        if region_min_col == -1 or region_max_col == -1 or background_color is None:
            print(f"Warning: Could not determine valid region for object at {next(iter(obj_coords))}. Skipping.")
            continue

        # Determine the object's horizontal boundaries
        object_min_col, object_max_col = get_object_boundaries(obj_coords)

        # Calculate distances to boundaries
        dist_left = object_min_col - region_min_col
        dist_right = region_max_col - object_max_col

        # Determine shift amount
        shift_amount = 0
        if dist_left <= dist_right:
            # Move left
            shift_amount = -dist_left
        else:
            # Move right
            shift_amount = dist_right
            
        # Don't move if already touching the target boundary
        if shift_amount == 0:
             continue

        # Erase the object from its original position in the output grid
        for r, c in obj_coords:
            # Check bounds just in case, though should be within grid
            if 0 <= r < output_np.shape[0] and 0 <= c < output_np.shape[1]:
                 output_np[r, c] = background_color # Set to background color

        # Draw the object in its new position
        for r, c in obj_coords:
            new_c = c + shift_amount
            # Check bounds for the new position
            if 0 <= r < output_np.shape[0] and 0 <= new_c < output_np.shape[1]:
                 output_np[r, new_c] = object_color
            else:
                 # This case implies an error in boundary calculation or logic,
                 # as the object should stay within its region boundaries.
                 print(f"Warning: Object pixel ({r},{c}) moved out of bounds to ({r},{new_c}). Original boundaries: {region_min_col}-{region_max_col}. Shift: {shift_amount}")
                 # As a fallback, draw it back at original position? Or leave it erased?
                 # Leaving it erased might be safer than drawing potentially wrong pixel.
                 # Let's try drawing back at original pos, hoping background erase happened.
                 if 0 <= r < output_np.shape[0] and 0 <= c < output_np.shape[1]:
                    output_np[r, c] = object_color # Revert this pixel


    return output_np.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 2 2 1 1 1 1 1 1 1 1 1 1
1 1 1 2 2 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 2 2 2 1 1 1 1 1
1 1 1 1 1 1 1 2 2 2 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 2 2 2 8 8 8 8 8
8 8 8 8 8 8 8 2 2 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 2 2
1 1 1 1 1 1 1 1 1 1 1 1 1 2 2
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 2 2 2
1 1 1 1 1 1 1 1 1 1 1 1 2 2 2
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
2 2 2 8 8 8 8 8 8 8 8 8 8 8 8
2 2 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
2 2 1 1 1 1 1 1 1 1 1 1 1 1 1
2 2 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 2 2 2
1 1 1 1 1 1 1 1 1 1 1 1 2 2 2
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 2 2 2
8 8 8 8 8 8 8 8 8 8 8 8 2 2 2
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 20
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 8.888888888888886

## Example 2:
Input:
```
1 1 1 1 1 1 1 8 8 8 8 8 8
1 1 1 1 1 1 1 8 8 2 2 8 8
1 1 1 1 1 1 1 8 8 2 2 8 8
1 1 2 2 1 1 1 8 8 2 2 8 8
1 1 2 2 1 1 1 8 8 8 8 8 8
1 1 1 1 1 1 1 8 8 8 8 8 8
1 1 2 2 2 1 1 8 8 8 8 8 8
1 1 2 2 2 1 1 8 8 8 8 8 8
1 1 1 1 1 1 1 8 2 2 8 8 8
1 1 1 1 1 1 1 8 2 2 8 8 8
1 1 1 1 1 1 1 8 8 8 8 8 8
```
Expected Output:
```
1 1 1 1 1 1 1 8 8 8 8 8 8
1 1 1 1 1 1 1 2 2 8 8 8 8
1 1 1 1 1 1 1 2 2 8 8 8 8
1 1 1 1 1 2 2 2 2 8 8 8 8
1 1 1 1 1 2 2 8 8 8 8 8 8
1 1 1 1 1 1 1 8 8 8 8 8 8
1 1 1 1 2 2 2 8 8 8 8 8 8
1 1 1 1 2 2 2 8 8 8 8 8 8
1 1 1 1 1 1 1 2 2 8 8 8 8
1 1 1 1 1 1 1 2 2 8 8 8 8
1 1 1 1 1 1 1 8 8 8 8 8 8
```
Transformed Output:
```
1 1 1 1 1 1 1 8 8 8 8 8 8
1 1 1 1 1 1 1 2 2 8 8 8 8
1 1 1 1 1 1 1 2 2 8 8 8 8
2 2 1 1 1 1 1 2 2 8 8 8 8
2 2 1 1 1 1 1 8 8 8 8 8 8
1 1 1 1 1 1 1 8 8 8 8 8 8
2 2 2 1 1 1 1 8 8 8 8 8 8
2 2 2 1 1 1 1 8 8 8 8 8 8
1 1 1 1 1 1 1 2 2 8 8 8 8
1 1 1 1 1 1 1 2 2 8 8 8 8
1 1 1 1 1 1 1 8 8 8 8 8 8
```
Match: False
Pixels Off: 20
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 13.986013986013987

## Example 3:
Input:
```
8 8 8 8 8 8 1 1 1 1 1 1 1 1
8 8 8 8 8 8 1 1 1 1 1 1 1 1
8 8 2 2 8 8 1 1 1 1 2 2 1 1
8 8 2 2 8 8 1 1 1 1 2 2 1 1
8 8 2 2 8 8 1 1 1 1 1 1 1 1
8 8 2 2 8 8 1 1 1 1 1 1 1 1
8 8 8 8 8 8 1 1 2 2 2 1 1 1
8 2 2 8 8 8 1 1 2 2 2 1 1 1
8 2 2 8 8 8 1 1 1 1 1 1 1 1
8 8 8 8 8 8 1 1 1 1 1 2 2 1
8 8 8 8 8 8 1 1 1 1 1 1 1 1
8 8 8 8 8 8 1 1 1 1 1 1 1 1
```
Expected Output:
```
8 8 8 8 8 8 1 1 1 1 1 1 1 1
8 8 8 8 8 8 1 1 1 1 1 1 1 1
2 2 8 8 8 8 1 1 1 1 1 1 2 2
2 2 8 8 8 8 1 1 1 1 1 1 2 2
2 2 8 8 8 8 1 1 1 1 1 1 1 1
2 2 8 8 8 8 1 1 1 1 1 1 1 1
8 8 8 8 8 8 1 1 1 1 1 2 2 2
2 2 8 8 8 8 1 1 1 1 1 2 2 2
2 2 8 8 8 8 1 1 1 1 1 1 1 1
8 8 8 8 8 8 1 1 1 1 1 1 2 2
8 8 8 8 8 8 1 1 1 1 1 1 1 1
8 8 8 8 8 8 1 1 1 1 1 1 1 1
```
Transformed Output:
```
8 8 8 8 8 8 1 1 1 1 1 1 1 1
8 8 8 8 8 8 1 1 1 1 1 1 1 1
2 2 8 8 8 8 1 1 1 1 1 1 2 2
2 2 8 8 8 8 1 1 1 1 1 1 2 2
2 2 8 8 8 8 1 1 1 1 1 1 1 1
2 2 8 8 8 8 1 1 1 1 1 1 1 1
8 8 8 8 8 8 2 2 2 1 1 1 1 1
2 2 8 8 8 8 2 2 2 1 1 1 1 1
2 2 8 8 8 8 1 1 1 1 1 1 1 1
8 8 8 8 8 8 1 1 1 1 1 1 2 2
8 8 8 8 8 8 1 1 1 1 1 1 1 1
8 8 8 8 8 8 1 1 1 1 1 1 1 1
```
Match: False
Pixels Off: 12
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 7.142857142857139

## Example 4:
Input:
```
8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 8 8 8 8 8 8 8
8 8 2 2 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 2 2 8 8 8
8 8 8 8 8 2 2 2 8 8 8
8 8 8 8 8 8 8 8 8 8 8
1 1 1 1 1 1 1 1 1 1 1
1 1 1 2 2 1 1 1 1 1 1
1 1 1 2 2 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8
2 2 8 8 8 8 8 8 8 8 8
2 2 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8
2 2 2 8 8 8 8 8 8 8 8
2 2 2 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8
1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 2 2
1 1 1 1 1 1 1 1 1 2 2
1 1 1 1 1 1 1 1 1 1 2
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8
2 2 8 8 8 8 8 8 8 8 8
2 2 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 2 2
8 8 8 8 8 8 8 8 2 2 2
8 8 8 8 8 8 8 8 8 8 8
1 1 1 1 1 1 1 1 1 1 1
2 2 1 1 1 1 1 1 1 1 1
2 2 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 2
```
Match: False
Pixels Off: 20
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 15.151515151515156
**General Assessment**

The provided code correctly identifies the red objects (color 2) and can determine the background color (blue=1 or azure=8) and the horizontal extent of the contiguous background region containing each object. However, the core logic for determining the direction of movement was flawed. The previous code assumed objects move towards the *closest* horizontal boundary of their background region. The analysis of the failed examples reveals this is incorrect. The direction of movement appears to be fixed for each background color: objects in blue regions move right, and objects in azure regions move left, irrespective of their position within the region or proximity to boundaries. The task requires recalculating the movement based on this new rule.

**Metrics and Analysis**

The previous code failed on all examples because its core movement logic was incorrect.

*   **Example 1:**
    *   Blue Region (Top, Cols 0-14): Contains Obj1 (C:3-4) and Obj2 (C:7-9).
        *   Expected: Both move Right (towards Col 14). Obj1 -> C:13-14, Obj2 -> C:12-14.
        *   Code: Obj1 moved Left (closer boundary), Obj2 moved Right (closer boundary). **Obj1 incorrect.**
    *   Azure Region (Bottom, Cols 0-14): Contains Obj3 (C:2) and Obj4 (C:7-9).
        *   Expected: Both move Left (towards Col 0). Obj3 -> C:0, Obj4 -> C:0-2.
        *   Code: Obj3 moved Left (closer boundary), Obj4 moved Right (closer boundary). **Obj4 incorrect.**
*   **Example 2:**
    *   Blue Region (Left, Cols 0-6): Contains Obj1 (C:2-3) and Obj2 (C:2-4).
        *   Expected: Both move Right (towards Col 6). Obj1 -> C:5-6, Obj2 -> C:4-6.
        *   Code: Obj1 moved Left (closer boundary), Obj2 moved Left (tied, chose left). **Both incorrect.**
    *   Azure Region (Right, Cols 7-12): Contains Obj3 (C:9-10) and Obj4 (C:8-9).
        *   Expected: Both move Left (towards Col 7). Obj3 -> C:7-8, Obj4 -> C:7-8.
        *   Code: Obj3 moved Left (tied, chose left), Obj4 moved Left (closer boundary). **Both correct** (coincidentally, as 'closer' matched 'left').
*   **Example 3:**
    *   Azure Region (Left, Cols 0-5): Contains three objects.
        *   Expected: All move Left (towards Col 0).
        *   Code: Moved based on proximity, resulting in some objects moving left and potentially others right if they were closer to the right boundary (Col 5). Errors observed confirm this mismatch.
    *   Blue Region (Right, Cols 6-13): Contains three objects.
        *   Expected: All move Right (towards Col 13).
        *   Code: Moved based on proximity. Errors observed confirm this mismatch.
*   **Example 4:**
    *   Azure Region (Top, Cols 0-10): Contains two objects.
        *   Expected: Both move Left (towards Col 0).
        *   Code: Moved based on proximity. Errors observed confirm this mismatch.
    *   Blue Region (Bottom, Cols 0-10): Contains two objects.
        *   Expected: Both move Right (towards Col 10).
        *   Code: Moved based on proximity. Errors observed confirm this mismatch.

**Conclusion:** The direction of movement is determined by the background color, not proximity. Blue background implies moving right; Azure background implies moving left.

**YAML Facts**


```yaml
Context:
  - The grid is composed of distinct background regions and objects within them.
  - Background regions are contiguous areas of either Blue (1) or Azure (8).
  - Objects are contiguous areas of Red (2).
  - Each red object resides entirely within one background region.

Objects:
  - type: background_region
    color: Blue (1) or Azure (8)
    properties:
      - contiguous_area
      - horizontal_boundaries: [min_column, max_column]
      - color
  - type: object
    color: Red (2)
    properties:
      - contiguous_area
      - location: set of (row, col) coordinates
      - horizontal_boundaries: [min_column, max_column]
      - parent_region: the background_region containing the object

Actions:
  - Identify all distinct background_regions (Blue and Azure).
  - For each background_region:
    - Determine its color and horizontal_boundaries [region_min_col, region_max_col].
    - Find all red objects located within this region.
    - Determine the movement direction based *only* on the region's background color:
      - If color is Blue (1), direction is Right.
      - If color is Azure (8), direction is Left.
    - For each red object within this region:
      - Get the object's horizontal_boundaries [object_min_col, object_max_col].
      - If direction is Right:
        - Calculate shift: region_max_col - object_max_col
      - If direction is Left:
        - Calculate shift: region_min_col - object_min_col (will be negative or zero)
      - Apply the calculated horizontal shift to all coordinates of the object.
  - Construct the output grid by placing the shifted objects onto the original background. Erase objects from their original positions.
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all distinct, contiguous background regions composed solely of Blue (1) pixels or Azure (8) pixels. Record the coordinates belonging to each region.
3.  Identify all distinct, contiguous objects composed of Red (2) pixels. Record the coordinates belonging to each object.
4.  For each identified red object:
    a.  Determine which background region it belongs to (e.g., by checking the color of a neighbor pixel or finding the region containing the object's coordinates).
    b.  Retrieve the color (Blue or Azure) and the minimum and maximum column indices (`region_min_col`, `region_max_col`) of that specific background region.
    c.  Find the minimum and maximum column indices occupied by the red object (`object_min_col`, `object_max_col`).
    d.  Determine the target horizontal shift based on the background color:
        i.  If the background region color is Blue (1), the object must move Right. Calculate the shift amount as `shift = region_max_col - object_max_col`.
        ii. If the background region color is Azure (8), the object must move Left. Calculate the shift amount as `shift = region_min_col - object_min_col`.
    e.  If the calculated `shift` is not zero:
        i.  First, erase the object from its original position in the output grid by setting the corresponding pixels to the background color determined in step 4b.
        ii. Then, draw the object in its new position in the output grid by adding the `shift` amount to the column coordinate of each pixel of the object and setting the color to Red (2).
5.  Return the modified output grid.
