
Previous Code:
```python
import numpy as np
from collections import deque

"""
Identifies two distinct non-background objects in the input grid: a 'Pattern Object' and an 'Azure Frame Object'.
The Azure Frame Object (color 8) must contain a fully enclosed rectangular region of background pixels (color 0), referred to as the 'Hole'.
The Pattern Object is extracted, including its background pixels within its bounding box.
This extracted Pattern (subgrid) is then copied/pasted into the Hole within the Azure Frame in the output grid, aligning the top-left corner of the Pattern's bounding box with the top-left corner of the Hole's bounding box.
The original Pattern Object and the Azure Frame Object remain in their original positions in the output grid.
"""

def find_objects(grid, ignore_color=0):
    """
    Finds all connected components (objects) of non-ignored colors in the grid.

    Args:
        grid (np.ndarray): The input grid.
        ignore_color (int): The color to treat as background/ignore.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color' (int), 'pixels' (set of (r, c) tuples),
              and 'bbox' (dict with 'min_row', 'min_col', 'max_row', 'max_col').
              Returns an empty list if no objects are found.
    """
    objects = []
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)

    for r in range(height):
        for c in range(width):
            if grid[r, c] != ignore_color and not visited[r, c]:
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

                    # Check 8 neighbors (including diagonals) for same color
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < height and 0 <= nc < width and \
                               not visited[nr, nc] and grid[nr, nc] == color:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                # Store primary color (first one found, good enough if object is one color)
                # For multi-color objects, need refinement if needed, but task seems to have single-color or pattern/frame separation
                first_pixel_color = grid[r,c]

                objects.append({
                    'pixels': obj_pixels,
                    'color': first_pixel_color, # Store the specific color of this component
                    'bbox': {'min_row': min_r, 'min_col': min_c, 'max_row': max_r, 'max_col': max_c}
                })
                
    # Check if any object is multi-colored, adjust 'color' if needed (maybe set to -1 or specific logic)
    final_objects = []
    for obj in objects:
         colors_in_obj = set(grid[r,c] for r,c in obj['pixels'])
         if len(colors_in_obj) > 1:
              obj['color'] = -1 # Mark as multi-color pattern object
         else:
              obj['color'] = colors_in_obj.pop() # Should be single color
         final_objects.append(obj)
         
    return final_objects


def find_hole(grid, frame_bbox):
    """
    Finds the rectangular hole (area of background color 0) inside a frame's bounding box.

    Args:
        grid (np.ndarray): The input grid.
        frame_bbox (dict): Bounding box of the frame object.

    Returns:
        dict: Bounding box dictionary {'min_row', 'min_col', 'max_row', 'max_col'}
              of the hole, or None if no hole is found.
    """
    height, width = grid.shape
    min_r_frame, min_c_frame = frame_bbox['min_row'], frame_bbox['min_col']
    max_r_frame, max_c_frame = frame_bbox['max_row'], frame_bbox['max_col']

    hole_pixels = set()
    visited_hole = np.zeros((height, width), dtype=bool)
    start_pixel = None

    # Find a starting background pixel within the frame's bbox, skipping the border
    for r in range(min_r_frame + 1, max_r_frame):
        for c in range(min_c_frame + 1, max_c_frame):
            if grid[r, c] == 0:
                start_pixel = (r, c)
                break
        if start_pixel:
            break

    if start_pixel is None:
        return None # No background pixel found inside

    # BFS from the starting pixel to find all connected background pixels *within* the frame's bbox
    q = deque([start_pixel])
    visited_hole[start_pixel[0], start_pixel[1]] = True
    min_r_hole, min_c_hole = start_pixel[0], start_pixel[1]
    max_r_hole, max_c_hole = start_pixel[0], start_pixel[1]

    while q:
        r, c = q.popleft()
        
        # Check if pixel is truly inside (not touching outside boundary via background)
        # If any neighbor is outside frame bbox and is background, this isn't a contained hole start point.
        is_truly_inside = True
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                 nr, nc = r + dr, c + dc
                 if not (min_r_frame <= nr <= max_r_frame and min_c_frame <= nc <= max_c_frame):
                      if 0 <= nr < height and 0 <= nc < width and grid[nr, nc] == 0:
                           # This search started from a pixel connected to the outside background. Reset and find another start.
                           # This check should ideally be done before starting BFS, but is complex.
                           # A simpler approach relies on task structure: the hole is fully contained.
                           pass # Assuming valid task structure for now.

        hole_pixels.add((r, c))
        min_r_hole = min(min_r_hole, r)
        min_c_hole = min(min_c_hole, c)
        max_r_hole = max(max_r_hole, r)
        max_c_hole = max(max_c_hole, c)

        # Check 4 cardinal neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Stay within frame bbox, look for background color, and ensure not visited
            if min_r_frame < nr < max_r_frame and min_c_frame < nc < max_c_frame and \
               grid[nr, nc] == 0 and not visited_hole[nr, nc]:
                visited_hole[nr, nc] = True
                q.append((nr, nc))

    if not hole_pixels:
         return None

    # Verify it's rectangular - check if all pixels within the derived bbox are in hole_pixels
    # hole_height = max_r_hole - min_r_hole + 1
    # hole_width = max_c_hole - min_c_hole + 1
    # if len(hole_pixels) != hole_height * hole_width:
        # Could implement stricter check if needed, but task examples suggest rectangular holes.
        # pass

    return {'min_row': min_r_hole, 'min_col': min_c_hole, 'max_row': max_r_hole, 'max_col': max_c_hole}


def extract_subgrid(grid, bbox):
    """
    Extracts the subgrid defined by the bounding box.

    Args:
        grid (np.ndarray): The source grid.
        bbox (dict): Bounding box dictionary.

    Returns:
        np.ndarray: The extracted subgrid.
    """
    return grid[bbox['min_row']:bbox['max_row']+1, bbox['min_col']:bbox['max_col']+1]


def paste_subgrid(target_grid, subgrid, top_left_coord, ignore_color=None):
    """
    Pastes a subgrid onto a target grid at the specified top-left coordinate.
    Optionally ignores pasting pixels of a specific color from the subgrid.

    Args:
        target_grid (np.ndarray): The grid to paste onto (modified in place).
        subgrid (np.ndarray): The subgrid to paste.
        top_left_coord (tuple): (row, col) for the top-left corner of the paste location.
        ignore_color (int, optional): If specified, pixels of this color in the
                                       subgrid will not be pasted. Defaults to None.
    """
    start_row, start_col = top_left_coord
    sub_height, sub_width = subgrid.shape
    target_height, target_width = target_grid.shape

    for r in range(sub_height):
        for c in range(sub_width):
            target_r, target_c = start_row + r, start_col + c
            # Check bounds
            if 0 <= target_r < target_height and 0 <= target_c < target_width:
                pixel_to_paste = subgrid[r, c]
                if ignore_color is None or pixel_to_paste != ignore_color:
                    target_grid[target_r, target_c] = pixel_to_paste


def transform(input_grid):
    """
    Applies the transformation: finds a pattern and an azure frame with a hole,
    then copies the pattern into the hole.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # Find all distinct objects (connected components of non-zero colors)
    objects = find_objects(input_grid, ignore_color=0)

    frame_object = None
    pattern_object = None
    hole_bbox = None

    # Identify the frame (color 8) and the pattern (other non-zero object)
    for obj in objects:
        # Check if the object consists *only* of color 8
        is_azure_frame = all(input_grid[r, c] == 8 for r, c in obj['pixels'])
        
        if is_azure_frame:
             # Attempt to find a hole within this potential frame's bounding box
             potential_hole_bbox = find_hole(input_grid, obj['bbox'])
             if potential_hole_bbox:
                  # Found a valid azure frame with a hole
                  frame_object = obj
                  hole_bbox = potential_hole_bbox
        else:
             # Assume any other non-background object is the pattern
             pattern_object = obj

    # Check if we found both necessary components
    if frame_object is None or pattern_object is None or hole_bbox is None:
        # If components aren't found as expected, return the original grid
        # or handle error appropriately based on task requirements for missing elements.
        print("Warning: Could not find pattern, frame, or hole. Returning input.")
        return output_grid 

    # Extract the pattern subgrid based on its bounding box
    pattern_subgrid = extract_subgrid(input_grid, pattern_object['bbox'])

    # Determine the top-left coordinate where the pattern should be pasted (top-left of the hole)
    paste_coord = (hole_bbox['min_row'], hole_bbox['min_col'])

    # Paste the pattern subgrid into the output grid at the hole's location
    # We ignore pasting the background color (0) from the pattern subgrid,
    # effectively overlaying the non-background parts of the pattern onto the hole.
    paste_subgrid(output_grid, pattern_subgrid, paste_coord, ignore_color=0)

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 4 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 0 0
0 0 0 8 0 0 0 8 0 0
0 0 0 8 0 0 0 8 0 0
0 0 0 8 0 0 0 8 0 0
0 0 0 8 8 8 8 8 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 4 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 0 0
0 0 0 8 2 2 2 8 0 0
0 0 0 8 2 4 2 8 0 0
0 0 0 8 2 2 2 8 0 0
0 0 0 8 8 8 8 8 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 4 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 0 0
0 0 0 8 4 0 0 8 0 0
0 0 0 8 0 0 0 8 0 0
0 0 0 8 0 0 0 8 0 0
0 0 0 8 8 8 8 8 0 0
```
Match: False
Pixels Off: 9
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 18.0

## Example 2:
Input:
```
0 0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 6 1 6 0 0 0 0 0 0 0 0 0
0 6 1 1 1 6 0 0 0 0 0 0 0 0
0 0 6 1 6 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 6 1 6 0 0 0 0 0 0 0 0 0
0 6 1 1 1 6 0 0 0 0 0 0 0 0
0 0 6 1 6 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 8 0 0 6 0 0 8
0 0 0 0 0 0 0 8 0 6 1 6 0 8
0 0 0 0 0 0 0 8 6 1 1 1 6 8
0 0 0 0 0 0 0 8 0 6 1 6 0 8
0 0 0 0 0 0 0 8 0 0 6 0 0 8
0 0 0 0 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 6 1 6 0 0 0 0 0 0 0 0 0
0 6 1 1 1 6 0 0 0 0 0 0 0 0
0 0 6 1 6 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 8 6 1 6 0 0 8
0 0 0 0 0 0 0 8 1 1 1 0 0 8
0 0 0 0 0 0 0 8 6 1 6 0 0 8
0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 12
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 12.244897959183675
