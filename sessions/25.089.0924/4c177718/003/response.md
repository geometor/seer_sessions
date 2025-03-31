Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np
from typing import List, Tuple, Dict, Set, Optional
import math

"""
Transforms an input grid based on identifying objects above and below a gray horizontal separator line.

1.  Identifies a horizontal line composed entirely of gray (5) pixels, separating the grid into upper and lower sections.
2.  Finds all contiguous, single-color, non-background objects in both sections. Expects exactly one object ('bottom_object') below the separator and three objects above it.
3.  Identifies the three upper objects based on color:
    a. 'ignore_object': The unique object with color red (2).
    b. 'match_object': The unique object whose color matches the color of the 'bottom_object'.
    c. 'target_top_object': The third remaining unique object.
4.  Creates a new output grid with 9 rows and the same width as the input grid, filled with the background color (0).
5.  Determines the vertical stacking order for the output based on the color of the 'target_top_object':
    a. If target_top_object.color > 5, the 'bottom_object' is placed above the 'target_top_object'.
    b. Otherwise (color <= 5), the 'target_top_object' is placed above the 'bottom_object'.
6.  Calculates the horizontal center column based on the bounding box of the 'bottom_object' in the original input grid.
7.  Places the two selected objects ('target_top_object' and 'bottom_object') into the output grid.
    a. The vertically topmost object starts at row 0.
    b. The vertically bottommost object starts at row 4 (leaving a 1-row gap of background color at row 3).
    c. Both objects are positioned horizontally such that their calculated center aligns with the reference center column calculated in step 6.
8.  Returns the constructed output grid.
"""

# --- Helper Functions ---

def find_separator_row(grid: np.ndarray, separator_color: int = 5) -> Optional[int]:
    """Finds the row index of the horizontal separator line."""
    for r in range(grid.shape[0]):
        if np.all(grid[r, :] == separator_color):
            return r
    return None

def get_neighbors(r: int, c: int, height: int, width: int) -> List[Tuple[int, int]]:
    """Gets valid 4-directional neighbors for a cell."""
    neighbors = []
    if r > 0: neighbors.append((r - 1, c))
    if r < height - 1: neighbors.append((r + 1, c))
    if c > 0: neighbors.append((r, c - 1))
    if c < width - 1: neighbors.append((r, c + 1))
    return neighbors

def find_objects(grid: np.ndarray, background_color: int = 0) -> List[Dict]:
    """Finds all contiguous objects of non-background colors."""
    height, width = grid.shape
    visited = set()
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] != background_color and (r, c) not in visited:
                color = grid[r, c]
                obj_pixels = set()
                q = [(r, c)]
                visited.add((r, c))
                min_r, min_c = r, c
                max_r, max_c = r, c

                # Perform BFS to find all connected pixels of the same color
                head = 0
                while head < len(q):
                    curr_r, curr_c = q[head]
                    head += 1
                    
                    obj_pixels.add((curr_r, curr_c))
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)

                    for nr, nc in get_neighbors(curr_r, curr_c, height, width):
                        if grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))

                # Extract shape relative to bounding box
                obj_height = max_r - min_r + 1
                obj_width = max_c - min_c + 1
                shape = np.full((obj_height, obj_width), background_color, dtype=int)
                for pr, pc in obj_pixels:
                    shape[pr - min_r, pc - min_c] = color
                
                objects.append({
                    "pixels": obj_pixels,
                    "color": color,
                    "bbox": (min_r, min_c, max_r, max_c), # Bbox relative to the input grid slice
                    "shape": shape
                })
    return objects

def place_object(target_grid: np.ndarray, obj_shape: np.ndarray, color: int, top_left_coord: Tuple[int, int]):
    """Places an object's shape onto a target grid at the specified top-left coordinate."""
    start_r, start_c = top_left_coord
    obj_h, obj_w = obj_shape.shape
    target_h, target_w = target_grid.shape

    for r in range(obj_h):
        for c in range(obj_w):
            # Only copy non-background pixels of the shape
            if obj_shape[r, c] == color: 
                target_r, target_c = start_r + r, start_c + c
                # Check bounds before placing
                if 0 <= target_r < target_h and 0 <= target_c < target_w:
                    target_grid[target_r, target_c] = color

# --- Main Transformation Function ---

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid according to the identified rules.
    """
    input_h, input_w = input_grid.shape
    output_h = 9
    output_w = input_w
    background_color = 0
    ignore_color = 2 # Red

    # 1. Find the separator row
    separator_r = find_separator_row(input_grid)
    if separator_r is None:
        # Handle error case: No separator found
        print("Error: Separator row not found.")
        return np.zeros((output_h, output_w), dtype=int)

    # 2. Split grid and find objects
    upper_grid = input_grid[:separator_r, :]
    lower_grid = input_grid[separator_r + 1:, :] # Skip the separator row itself

    upper_objects = find_objects(upper_grid, background_color)
    lower_objects = find_objects(lower_grid, background_color)

    # Basic validation based on example structure
    if len(lower_objects) != 1 or len(upper_objects) != 3:
        print(f"Error: Expected 1 lower object and 3 upper objects, found {len(lower_objects)} and {len(upper_objects)}.")
        return np.zeros((output_h, output_w), dtype=int)

    bottom_object = lower_objects[0]
    bottom_color = bottom_object["color"]
    
    # Adjust bottom_object bbox row coordinates to be relative to the original input grid
    # for accurate centering calculation.
    bottom_obj_orig_bbox = (
        bottom_object["bbox"][0] + separator_r + 1,
        bottom_object["bbox"][1],
        bottom_object["bbox"][2] + separator_r + 1,
        bottom_object["bbox"][3]
    )

    # 3. Identify the three specific upper objects by color
    ignore_object = None
    match_object = None 
    target_top_object = None
    processed_indices = set()

    # Find ignore object (red=2)
    found_ignore = False
    for i, obj in enumerate(upper_objects):
        if obj["color"] == ignore_color:
            if found_ignore: # More than one red object found
                 print(f"Error: Found multiple objects with ignore color {ignore_color}.")
                 return np.zeros((output_h, output_w), dtype=int)
            ignore_object = obj
            processed_indices.add(i)
            found_ignore = True
            
    if ignore_object is None:
        print(f"Error: Ignore object with color {ignore_color} not found.")
        return np.zeros((output_h, output_w), dtype=int)

    # Find match object (matches bottom_object color)
    found_match = False
    for i, obj in enumerate(upper_objects):
        if i in processed_indices: continue
        if obj["color"] == bottom_color:
            if found_match: # More than one matching color object found
                print(f"Error: Found multiple objects matching bottom color {bottom_color}.")
                return np.zeros((output_h, output_w), dtype=int)
            match_object = obj
            processed_indices.add(i)
            found_match = True

    if match_object is None:
        print(f"Error: Match object with color {bottom_color} not found.")
        return np.zeros((output_h, output_w), dtype=int)
        
    # Find target object (the remaining one)
    found_target = False
    for i, obj in enumerate(upper_objects):
         if i not in processed_indices:
             if found_target: # Should only be one left
                 print(f"Error: Found multiple potential target objects.")
                 return np.zeros((output_h, output_w), dtype=int)
             target_top_object = obj
             processed_indices.add(i)
             found_target = True

    if target_top_object is None:
        print(f"Error: Target object not found.")
        return np.zeros((output_h, output_w), dtype=int)

    # 4. Create output grid
    output_grid = np.full((output_h, output_w), background_color, dtype=int)

    # 5. Determine stacking order
    if target_top_object["color"] > 5:
        top
---
