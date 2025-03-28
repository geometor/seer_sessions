
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
Okay, let's analyze the provided information and refine our understanding of the transformation.

**General Assessment and Strategy**

The previous code attempted to solve the task by identifying two objects: a pattern object and an azure frame object containing a hole. It then extracted the pattern based on its bounding box and pasted it into the hole.

The results show this approach failed for both examples. The core issue seems to be the definition and extraction of the "pattern object". The code treated connected components of a single color as distinct objects. However, the patterns in the examples are multi-colored or consist of multiple disconnected components (if considering only single-color connectivity). The pasting logic also incorrectly ignored background pixels from the pattern area.

**Revised Strategy:**

1.  **Identify Frame and Hole:** Correctly identify the azure (color 8) frame and the rectangular background (color 0) hole it encloses. This part of the logic seems potentially reusable but needs verification.
2.  **Identify Pattern Area:** Define the "pattern" not as a single object, but as the collection of *all* pixels that are *neither* background (0) *nor* part of the azure frame (8).
3.  **Determine Pattern Bounding Box:** Find the minimal bounding box that encompasses all pixels identified in step 2.
4.  **Extract Pattern Subgrid:** Extract the rectangular region defined by the pattern bounding box from the input grid. This extraction *must include* any background pixels within that bounding box.
5.  **Paste Pattern:** Copy the input grid to the output grid. Then, paste the *entire* extracted pattern subgrid into the hole area of the output grid, aligning the top-left corner of the subgrid with the top-left corner of the hole. Do *not* ignore background pixels during pasting.

**Metrics and Evidence Gathering**

Let's verify the properties of the key components in each example using the revised strategy definition.



*code_execution:*
```python
import numpy as np

def analyze_example(grid):
    height, width = grid.shape
    azure_pixels = set((r, c) for r in range(height) for c in range(width) if grid[r, c] == 8)
    pattern_pixels = set((r, c) for r in range(height) for c in range(width) if grid[r, c] != 0 and grid[r, c] != 8)

    if not azure_pixels or not pattern_pixels:
        return {"error": "Missing azure frame or pattern pixels"}

    # Basic Frame BBox (assuming one connected frame object)
    min_r_frame = min(r for r, c in azure_pixels)
    max_r_frame = max(r for r, c in azure_pixels)
    min_c_frame = min(c for r, c in azure_pixels)
    max_c_frame = max(c for r, c in azure_pixels)
    frame_bbox = {'min_row': min_r_frame, 'min_col': min_c_frame, 'max_row': max_r_frame, 'max_col': max_c_frame}

    # Find Hole (simple version assuming rectangular hole inside frame bbox)
    hole_bbox = None
    for r in range(min_r_frame + 1, max_r_frame):
        for c in range(min_c_frame + 1, max_c_frame):
            if grid[r, c] == 0:
                # Potential start, now find extents
                min_r_hole, max_r_hole = r, r
                min_c_hole, max_c_hole = c, c
                q = [(r, c)]
                visited = set([(r,c)])
                while q:
                    row, col = q.pop(0)
                    min_r_hole = min(min_r_hole, row)
                    max_r_hole = max(max_r_hole, row)
                    min_c_hole = min(min_c_hole, col)
                    max_c_hole = max(max_c_hole, col)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if min_r_frame < nr < max_r_frame and min_c_frame < nc < max_c_frame and \
                           grid[nr, nc] == 0 and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                # Assuming the first connected component of 0s found is the hole
                hole_bbox = {'min_row': min_r_hole, 'min_col': min_c_hole, 'max_row': max_r_hole, 'max_col': max_c_hole}
                break
        if hole_bbox:
            break

    if not hole_bbox:
        return {"error": "Could not find hole"}

    # Pattern BBox
    min_r_pattern = min(r for r, c in pattern_pixels)
    max_r_pattern = max(r for r, c in pattern_pixels)
    min_c_pattern = min(c for r, c in pattern_pixels)
    max_c_pattern = max(c for r, c in pattern_pixels)
    pattern_bbox = {'min_row': min_r_pattern, 'min_col': min_c_pattern, 'max_row': max_r_pattern, 'max_col': max_c_pattern}

    pattern_subgrid = grid[pattern_bbox['min_row']:pattern_bbox['max_row']+1, pattern_bbox['min_col']:pattern_bbox['max_col']+1]
    hole_height = hole_bbox['max_row'] - hole_bbox['min_row'] + 1
    hole_width = hole_bbox['max_col'] - hole_bbox['min_col'] + 1
    pattern_height, pattern_width = pattern_subgrid.shape


    return {
        "grid_shape": grid.shape,
        "frame_bbox": frame_bbox,
        "hole_bbox": hole_bbox,
        "hole_shape": (hole_height, hole_width),
        "pattern_bbox": pattern_bbox,
        "pattern_shape": (pattern_height, pattern_width),
        "pattern_subgrid": pattern_subgrid.tolist() # for printing
    }

# Example 1 Input
grid1_in = np.array([
    [0,0,0,0,0,0,0,0,0,0],
    [0,2,2,2,0,0,0,0,0,0],
    [0,2,4,2,0,0,0,0,0,0],
    [0,2,2,2,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,8,8,8,8,8,0,0],
    [0,0,0,8,0,0,0,8,0,0],
    [0,0,0,8,0,0,0,8,0,0],
    [0,0,0,8,0,0,0,8,0,0],
    [0,0,0,8,8,8,8,8,0,0]
])

# Example 2 Input
grid2_in = np.array([
    [0,0,0,6,0,0,0,0,0,0,0,0,0,0],
    [0,0,6,1,6,0,0,0,0,0,0,0,0,0],
    [0,6,1,1,1,6,0,0,0,0,0,0,0,0],
    [0,0,6,1,6,0,0,0,0,0,0,0,0,0],
    [0,0,0,6,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,8,8,8,8,8,8,8],
    [0,0,0,0,0,0,0,8,0,0,0,0,0,8],
    [0,0,0,0,0,0,0,8,0,0,0,0,0,8],
    [0,0,0,0,0,0,0,8,0,0,0,0,0,8],
    [0,0,0,0,0,0,0,8,0,0,0,0,0,8],
    [0,0,0,0,0,0,0,8,0,0,0,0,0,8],
    [0,0,0,0,0,0,0,8,8,8,8,8,8,8],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
])

analysis1 = analyze_example(grid1_in)
analysis2 = analyze_example(grid2_in)

print("--- Example 1 Analysis ---")
import json
print(json.dumps(analysis1, indent=2))

print("\n--- Example 2 Analysis ---")
print(json.dumps(analysis2, indent=2))

# Compare extracted pattern subgrid shape with hole shape
print(f"\nExample 1: Pattern Shape {analysis1['pattern_shape']} vs Hole Shape {analysis1['hole_shape']}")
print(f"Example 2: Pattern Shape {analysis2['pattern_shape']} vs Hole Shape {analysis2['hole_shape']}")

# Check if pattern fits into hole
fits1 = analysis1['pattern_shape'][0] <= analysis1['hole_shape'][0] and analysis1['pattern_shape'][1] <= analysis1['hole_shape'][1]
fits2 = analysis2['pattern_shape'][0] <= analysis2['hole_shape'][0] and analysis2['pattern_shape'][1] <= analysis2['hole_shape'][1]
print(f"Example 1: Pattern fits in hole: {fits1}")
print(f"Example 2: Pattern fits in hole: {fits2}")
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Example 1 Analysis ---
{
  "grid_shape": [
    10,
    10
  ],
  "frame_bbox": {
    "min_row": 5,
    "min_col": 3,
    "max_row": 9,
    "max_col": 7
  },
  "hole_bbox": {
    "min_row": 6,
    "min_col": 4,
    "max_row": 8,
    "max_col": 6
  },
  "hole_shape": [
    3,
    3
  ],
  "pattern_bbox": {
    "min_row": 1,
    "min_col": 1,
    "max_row": 3,
    "max_col": 3
  },
  "pattern_shape": [
    3,
    3
  ],
  "pattern_subgrid": [
    [
      2,
      2,
      2
    ],
    [
      2,
      4,
      2
    ],
    [
      2,
      2,
      2
    ]
  ]
}

--- Example 2 Analysis ---
{
  "grid_shape": [
    14,
    14
  ],
  "frame_bbox": {
    "min_row": 6,
    "min_col": 7,
    "max_row": 12,
    "max_col": 13
  },
  "hole_bbox": {
    "min_row": 7,
    "min_col": 8,
    "max_row": 11,
    "max_col": 12
  },
  "hole_shape": [
    5,
    5
  ],
  "pattern_bbox": {
    "min_row": 0,
    "min_col": 1,
    "max_row": 4,
    "max_col": 5
  },
  "pattern_shape": [
    5,
    5
  ],
  "pattern_subgrid": [
    [
      0,
      0,
      6,
      0,
      0
    ],
    [
      0,
      6,
      1,
      6,
      0
    ],
    [
      6,
      1,
      1,
      1,
      6
    ],
    [
      0,
      6,
      1,
      6,
      0
    ],
    [
      0,
      0,
      6,
      0,
      0
    ]
  ]
}

Example 1: Pattern Shape (3, 3) vs Hole Shape (3, 3)
Example 2: Pattern Shape (5, 5) vs Hole Shape (5, 5)
Example 1: Pattern fits in hole: True
Example 2: Pattern fits in hole: True

```
The analysis confirms the revised understanding:

*   The pattern is defined by all non-background, non-azure pixels.
*   The bounding box of these pixels defines the subgrid to be extracted.
*   This extracted subgrid includes background pixels.
*   The dimensions of the extracted pattern subgrid exactly match the dimensions of the hole in both examples.
*   Pasting the extracted `pattern_subgrid` (including its background '0's) into the `hole_bbox` location should produce the correct output.

**YAML Facts**


```yaml
task_description: Copy a pattern defined by non-background, non-frame pixels into a hole within an azure frame.

definitions:
  - name: background_pixel
    type: pixel
    properties:
      color: 0 (white)
  - name: frame_pixel
    type: pixel
    properties:
      color: 8 (azure)
  - name: pattern_pixel
    type: pixel
    properties:
      color: any color except 0 (white) and 8 (azure)
  - name: azure_frame
    type: object
    description: A contiguous object composed of frame_pixels (color 8) that encloses a rectangular area.
  - name: hole
    type: region
    description: A rectangular area within the azure_frame's bounding box composed entirely of background_pixels (color 0). It must be fully enclosed by the frame_pixels or the grid boundaries relative to the frame.
  - name: pattern_area
    type: region
    description: The minimal bounding box enclosing all pattern_pixels in the input grid.
  - name: pattern_subgrid
    type: grid
    description: The rectangular subgrid extracted from the input grid corresponding to the pattern_area. Includes all pixels within that area, regardless of color.

actions:
  - name: find_azure_frame_and_hole
    input: input_grid
    output: 
      - azure_frame object
      - hole region (bounding box)
    description: Identify the azure_frame object and locate the rectangular hole region within it.
  - name: find_pattern_pixels
    input: input_grid
    output: set of pattern_pixel coordinates
    description: Identify all pixels in the grid that are not background_pixel and not frame_pixel.
  - name: determine_pattern_area
    input: set of pattern_pixel coordinates
    output: pattern_area (bounding box)
    description: Calculate the minimal bounding box containing all pattern_pixels.
  - name: extract_pattern_subgrid
    input: 
      - input_grid
      - pattern_area (bounding box)
    output: pattern_subgrid (2D array)
    description: Extract the subgrid from the input_grid defined by the pattern_area.
  - name: prepare_output_grid
    input: input_grid
    output: output_grid
    description: Create a copy of the input_grid.
  - name: paste_pattern_into_hole
    input:
      - output_grid (mutable)
      - pattern_subgrid
      - hole region (bounding box)
    output: modified output_grid
    description: Paste the pattern_subgrid onto the output_grid. The top-left corner of the pattern_subgrid is placed at the top-left corner of the hole region. All pixels from the pattern_subgrid overwrite the existing pixels in the output_grid within the paste area.

input_output_relationship:
  - The output grid initially mirrors the input grid.
  - The transformation involves copying the pattern_subgrid (defined by the bounding box of all non-background, non-azure pixels) and pasting it into the hole found within the azure_frame.
```


**Natural Language Program**

1.  Create a copy of the input grid, which will become the output grid.
2.  Identify the azure (color 8) pixels that form a frame structure.
3.  Locate the rectangular region composed entirely of background (color 0) pixels that is enclosed within the azure frame (the "hole"). Determine the coordinates of the top-left corner and the dimensions (height, width) of this hole.
4.  Identify all pixels in the input grid that are neither background (color 0) nor azure (color 8). These are the "pattern pixels".
5.  Determine the minimal bounding box that encloses all identified pattern pixels.
6.  Extract the rectangular subgrid from the input grid defined by this pattern bounding box. This subgrid represents the complete pattern, including any background pixels within its bounds.
7.  Paste the extracted pattern subgrid onto the output grid. Align the top-left corner of the pattern subgrid with the top-left corner of the hole identified in step 3. Overwrite the pixels in the output grid within the target area with the corresponding pixels from the pattern subgrid.
8.  Return the modified output grid.
