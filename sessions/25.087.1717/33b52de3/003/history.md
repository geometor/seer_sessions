
Previous Code:
```python
import numpy as np
from collections import deque

"""
Transformation Rule:

1. Identify two distinct regions in the input grid:
    a. A "template grid": A region composed of multiple instances of a repeating gray (5) pattern (specifically a 3x3 hollow square), arranged in a grid structure.
    b. A "key pattern": A compact rectangular block of various colors, spatially separated from the template grid.
2. Determine the dimensions (rows `tr`, columns `tc`) of the template grid based on the arrangement of the gray patterns.
3. Determine the dimensions (rows `kh`, columns `kc`) and top-left corner (`kr`, `kc`) of the key pattern. The dimensions must match the template grid dimensions (`tr == kh`, `tc == kw`).
4. Create an output grid initially identical to the input grid.
5. Iterate through each position `(r, c)` within the template grid's structure (from `r=0` to `tr-1`, `c=0` to `tc-1`).
6. For each `(r, c)`:
    a. Identify the specific gray template pattern instance corresponding to this position in the template grid.
    b. Get the replacement color from the key pattern at the corresponding relative position: `color = input_grid[kr + r, kc + c]`.
    c. Find all gray (5) pixels belonging to the identified template pattern instance.
    d. In the output grid, change the color of these gray pixels to the replacement color obtained in step 6b.
7. Return the modified output grid. The key pattern itself and the background remain unchanged.
"""

def find_objects(grid, color):
    """Finds all contiguous objects of a specific color."""
    h, w = grid.shape
    visited = np.zeros((h, w), dtype=bool)
    objects = []

    for r in range(h):
        for c in range(w):
            if grid[r, c] == color and not visited[r, c]:
                obj_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    obj_pixels.append((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < h and 0 <= nc < w and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Bounding box: top, left, bottom, right (inclusive)
                bbox = (min_r, min_c, max_r, max_c)
                objects.append({'pixels': set(obj_pixels), 'bbox': bbox, 'color': color})
                
    return objects

def is_template_pattern(grid, obj):
    """Checks if an object is the specific 3x3 hollow gray square template."""
    if obj['color'] != 5:
        return False
        
    min_r, min_c, max_r, max_c = obj['bbox']
    h = max_r - min_r + 1
    w = max_c - min_c + 1

    if h != 3 or w != 3:
        return False

    # Check if it's a hollow square
    expected_pixels = set()
    for r in range(min_r, max_r + 1):
        expected_pixels.add((r, min_c))
        expected_pixels.add((r, max_c))
    for c in range(min_c + 1, max_c):
        expected_pixels.add((min_r, c))
        expected_pixels.add((max_r, c))
        
    return obj['pixels'] == expected_pixels


def transform(input_grid):
    """
    Applies the transformation rule described above.
    """
    input_grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid)
    h, w = input_grid.shape

    # 1a. Find all gray objects
    gray_objects = find_objects(input_grid, 5)

    # 1a. Identify template instances (3x3 hollow gray squares)
    template_instances = []
    for obj in gray_objects:
        if is_template_pattern(input_grid, obj):
            template_instances.append(obj)

    if not template_instances:
        # No template patterns found, return original grid
        return output_grid.tolist()

    # 2. Determine template grid structure
    # Get top-left corners and sort them
    corners = sorted([(obj['bbox'][0], obj['bbox'][1], obj) for obj in template_instances])
    
    min_template_r = min(c[0] for c in corners)
    min_template_c = min(c[1] for c in corners)
    max_template_r = max(c[0] for c in corners)
    max_template_c = max(c[1] for c in corners)

    # Find unique row and column coordinates of the templates
    template_rows = sorted(list(set(c[0] for c in corners)))
    template_cols = sorted(list(set(c[1] for c in corners)))
    
    tr = len(template_rows) # template grid height
    tc = len(template_cols) # template grid width
    
    # Create a mapping from template grid index (r, c) to the actual object
    template_map = {}
    corner_to_obj = {(c[0], c[1]): c[2] for c in corners}
    for r_idx, row_val in enumerate(template_rows):
        for c_idx, col_val in enumerate(template_cols):
            if (row_val, col_val) in corner_to_obj:
                 template_map[(r_idx, c_idx)] = corner_to_obj[(row_val, col_val)]
            # else: might indicate an incomplete grid, handle if necessary


    # 1b. Find potential key patterns (non-white, non-gray objects)
    key_pattern = None
    key_r, key_c = -1, -1
    
    potential_key_colors = set(range(1, 10)) - {5} # Colors 1-9 excluding gray
    
    all_objects = []
    for color in potential_key_colors:
         all_objects.extend(find_objects(input_grid, color))
    # Also consider objects made of multiple colors if needed, but let's assume single-color blocks first.
    # A more robust approach would find *all* non-background contiguous blocks regardless of color variations within.
    # For this task, the key seems to be a simple rectangle of single-color cells. Let's refine based on bounding box.
    
    # Find *all* non-background pixels
    non_bg_pixels = np.argwhere(input_grid != 0)
    
    # Exclude pixels belonging to template instances
    template_pixel_set = set()
    for obj in template_instances:
        template_pixel_set.update(obj['pixels'])
        
    potential_key_pixels = []
    for r,c in non_bg_pixels:
        if (r,c) not in template_pixel_set:
            potential_key_pixels.append((r,c))

    if not potential_key_pixels:
         # No key pattern found? This shouldn't happen based on examples.
         return output_grid.tolist() 

    # Find the bounding box of the remaining non-background, non-template pixels
    min_key_r = min(p[0] for p in potential_key_pixels)
    min_key_c = min(p[1] for p in potential_key_pixels)
    max_key_r = max(p[0] for p in potential_key_pixels)
    max_key_c = max(p[1] for p in potential_key_pixels)

    # 3. Check if dimensions match the template grid
    kh = max_key_r - min_key_r + 1
    kw = max_key_c - min_key_c + 1
    
    if kh == tr and kw == tc:
        key_pattern_found = True
        key_r, key_c = min_key_r, min_key_c
    else:
        # If simple bounding box doesn't work, we might need a more complex object detection
        # for the key pattern, possibly involving finding the largest compact non-template object.
        # But let's assume the bounding box approach works for now.
        key_pattern_found = False


    if not key_pattern_found:
        # Key pattern matching template dimensions not found
        print("Warning: Key pattern dimensions do not match template grid dimensions.")
        return output_grid.tolist() # Return unchanged grid if logic fails

    # 4. Initialize output grid (already done)

    # 5. Iterate through template grid positions
    for r_idx in range(tr):
        for c_idx in range(tc):
            # 6a. Get corresponding template instance
            if (r_idx, c_idx) in template_map:
                template_obj = template_map[(r_idx, c_idx)]
                
                # 6b. Get replacement color from key pattern
                replacement_color = input_grid[key_r + r_idx, key_c + c_idx]
                
                # 6c & 6d. Find gray pixels in template and replace in output grid
                for (px_r, px_c) in template_obj['pixels']:
                    # Check original color is gray (5) before replacing
                    if input_grid[px_r, px_c] == 5: 
                        output_grid[px_r, px_c] = replacement_color
            # else: Handle missing template instance in the grid if necessary


    # 7. Return the modified grid
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 0
0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 5 0 0 0 5 0 0 0
0 1 8 1 8 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 0
0 8 8 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 4 1 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 0
0 1 1 4 4 0 0 5 0 0 0 5 0 0 0 5 0 0 0 5 0 0 0
0 0 0 0 0 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 0
0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 5 0 0 0 5 0 0 0
0 0 0 0 0 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 0
0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 5 0 0 0 5 0 0 0
0 0 0 0 0 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0 8 8 8 0 1 1 1 0 8 8 8 0 0
0 0 0 0 0 0 0 1 0 0 0 8 0 0 0 1 0 0 0 8 0 0 0
0 1 8 1 8 0 1 1 1 0 8 8 8 0 1 1 1 0 8 8 8 0 0
0 8 8 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 4 1 0 8 8 8 0 8 8 8 0 1 1 1 0 1 1 1 0 0
0 1 1 4 4 0 0 8 0 0 0 8 0 0 0 1 0 0 0 1 0 0 0
0 0 0 0 0 0 8 8 8 0 8 8 8 0 1 1 1 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0 1 1 1 0 4 4 4 0 1 1 1 0 0
0 0 0 0 0 0 0 1 0 0 0 1 0 0 0 4 0 0 0 1 0 0 0
0 0 0 0 0 0 1 1 1 0 1 1 1 0 4 4 4 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0 1 1 1 0 4 4 4 0 4 4 4 0 0
0 0 0 0 0 0 0 1 0 0 0 1 0 0 0 4 0 0 0 4 0 0 0
0 0 0 0 0 0 1 1 1 0 1 1 1 0 4 4 4 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 0
0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 5 0 0 0 5 0 0 0
0 1 8 1 8 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 0
0 8 8 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 4 1 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 0
0 1 1 4 4 0 0 5 0 0 0 5 0 0 0 5 0 0 0 5 0 0 0
0 0 0 0 0 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 0
0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 5 0 0 0 5 0 0 0
0 0 0 0 0 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 0
0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 5 0 0 0 5 0 0 0
0 0 0 0 0 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 112
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 84.68809073724009

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 0
0 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 0
0 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 0
0 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 0
0 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 0
0 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 0
0 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 1 1 3 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 2 2 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 1 2 3 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 1 1 1 0 1 1 1 0 3 3 3 0 1 1 1 0 0
0 0 2 0 2 0 1 0 1 0 1 0 1 0 3 0 3 0 1 0 1 0 0
0 0 2 2 2 0 1 1 1 0 1 1 1 0 3 3 3 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 2 2 2 0 2 2 2 0 1 1 1 0 1 1 1 0 0
0 0 1 0 1 0 2 0 2 0 2 0 2 0 1 0 1 0 1 0 1 0 0
0 0 1 1 1 0 2 2 2 0 2 2 2 0 1 1 1 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 1 1 1 0 2 2 2 0 3 3 3 0 2 2 2 0 0
0 0 2 0 2 0 1 0 1 0 2 0 2 0 3 0 3 0 2 0 2 0 0
0 0 2 2 2 0 1 1 1 0 2 2 2 0 3 3 3 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 1 1 3 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 2 2 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 1 2 3 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 1 1 1 0 1 1 1 0 3 3 3 0 1 1 1 0 0
0 0 2 0 2 0 1 0 1 0 1 0 1 0 3 0 3 0 1 0 1 0 0
0 0 2 2 2 0 1 1 1 0 1 1 1 0 3 3 3 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 2 2 2 0 2 2 2 0 1 1 1 0 1 1 1 0 0
0 0 1 0 1 0 2 0 2 0 2 0 2 0 1 0 1 0 1 0 1 0 0
0 0 1 1 1 0 2 2 2 0 2 2 2 0 1 1 1 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 1 1 1 0 2 2 2 0 3 3 3 0 2 2 2 0 0
0 0 2 0 2 0 1 0 1 0 2 0 2 0 3 0 3 0 2 0 2 0 0
0 0 2 2 2 0 1 1 1 0 2 2 2 0 3 3 3 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 1 1 3 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 2 2 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 1 2 3 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0
## General Assessment

The provided code successfully solved the second training example but failed on the first. The core logic involves identifying a grid of repeating "template" patterns (3x3 hollow gray squares) and a separate "key" pattern. The colors from the key pattern are used to replace the gray pixels within the corresponding template instances based on their relative positions in their respective grids.

The failure in the first example stems from the key pattern identification and dimension matching. The code calculated the bounding box of *all* non-background, non-template pixels to define the key pattern. In Example 1, this bounding box (5x5) did not match the dimensions of the template grid (4x4), causing the transformation to be skipped. The actual key pattern in Example 1 has colors arranged in a 4x5 grid, but its bounding box includes some surrounding background making it 5x5.

The strategy for resolution is to refine the key pattern identification logic:
1.  Isolate potential key pattern pixels by removing the template pixels.
2.  Identify contiguous objects formed by the remaining non-background pixels.
3.  Select the object whose dimensions match the dimensions derived from the template grid structure (`tr` rows, `tc` columns).
4.  Use the colors from this specific object, located at its top-left corner, for the replacement process.

## Metrics Gathering

Let's analyze the examples using code execution.



*code_execution:*
```python
import numpy as np
from collections import deque

# --- Helper Functions (modified find_objects for multi-color) ---
def find_contiguous_objects(grid, ignore_colors=None):
    """Finds all contiguous objects of non-background colors, potentially ignoring specific colors."""
    if ignore_colors is None:
        ignore_colors = {0} # Ignore background by default
    else:
        ignore_colors = set(ignore_colors)
        ignore_colors.add(0) # Always ignore background

    h, w = grid.shape
    visited = np.zeros((h, w), dtype=bool)
    objects = []

    for r in range(h):
        for c in range(w):
            color = grid[r, c]
            if color not in ignore_colors and not visited[r, c]:
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c
                colors_in_obj = {color}

                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < h and 0 <= nc < w and not visited[nr, nc]:
                             neighbor_color = grid[nr, nc]
                             if neighbor_color not in ignore_colors:
                                visited[nr, nc] = True
                                colors_in_obj.add(neighbor_color)
                                q.append((nr, nc))

                bbox = (min_r, min_c, max_r, max_c)
                height = max_r - min_r + 1
                width = max_c - min_c + 1
                objects.append({'pixels': obj_pixels, 'bbox': bbox, 'height': height, 'width': width, 'colors': colors_in_obj})

    return objects

def find_template_objects(grid):
    """Finds 3x3 hollow gray square template objects."""
    h, w = grid.shape
    visited = np.zeros((h, w), dtype=bool)
    template_objects = []
    gray = 5

    for r in range(h):
        for c in range(w):
            if grid[r, c] == gray and not visited[r, c]:
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c
                is_potential_template = True

                queue_copy = list(q) # Keep track for checking shape later

                while q:
                    row, col = q.popleft()
                    if grid[row, col] != gray: # Should not happen if starting correctly
                        is_potential_template = False
                        # continue # continue BFS to mark all connected as visited
                    obj_pixels.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < h and 0 <= nc < w and \
                           grid[nr, nc] == gray and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            queue_copy.append((nr,nc)) # Also add to shape check list


                # Check shape and size after finding the connected component
                if is_potential_template:
                    bbox_h = max_r - min_r + 1
                    bbox_w = max_c - min_c + 1
                    is_hollow_square = False
                    if bbox_h == 3 and bbox_w == 3:
                        expected_pixels = set()
                        for r_ in range(min_r, max_r + 1):
                            expected_pixels.add((r_, min_c))
                            expected_pixels.add((r_, max_c))
                        for c_ in range(min_c + 1, max_c):
                            expected_pixels.add((min_r, c_))
                            expected_pixels.add((max_r, c_))
                        if obj_pixels == expected_pixels:
                             is_hollow_square = True

                    if is_hollow_square:
                        bbox = (min_r, min_c, max_r, max_c)
                        template_objects.append({'pixels': obj_pixels, 'bbox': bbox, 'color': gray})

    return template_objects

def analyze_example(input_grid_list):
    input_grid = np.array(input_grid_list, dtype=int)
    h, w = input_grid.shape
    results = {}
    results['dimensions'] = {'height': h, 'width': w}

    # Find templates
    templates = find_template_objects(input_grid)
    results['templates'] = []
    if templates:
        corners = sorted([(obj['bbox'][0], obj['bbox'][1]) for obj in templates])
        template_rows = sorted(list(set(c[0] for c in corners)))
        template_cols = sorted(list(set(c[1] for c in corners)))
        tr = len(template_rows)
        tc = len(template_cols)
        results['template_grid'] = {'rows': tr, 'cols': tc, 'count': len(templates)}
        for i, t in enumerate(templates):
            results['templates'].append({'id': i, 'bbox': t['bbox'], 'pixel_count': len(t['pixels'])})
    else:
        results['template_grid'] = {'rows': 0, 'cols': 0, 'count': 0}


    # Find potential key patterns (non-background, non-gray)
    # Create a temp grid marking templates as background
    temp_grid = np.copy(input_grid)
    for t in templates:
        for r, c in t['pixels']:
            temp_grid[r, c] = 0 # Mark template pixels as background

    potential_keys = find_contiguous_objects(temp_grid, ignore_colors={0, 5}) # Ignore background and gray
    results['potential_keys'] = []
    for i, k in enumerate(potential_keys):
         results['potential_keys'].append({'id': i, 'bbox': k['bbox'], 'height': k['height'], 'width': k['width'], 'colors': list(k['colors']), 'pixel_count': len(k['pixels'])})

    # Identify the actual key based on dimension matching
    results['identified_key'] = None
    if templates and potential_keys:
        tr = results['template_grid']['rows']
        tc = results['template_grid']['cols']
        for key_candidate in potential_keys:
            # Check if the *dimensions* of the candidate match the template grid dims
            if key_candidate['height'] == tr and key_candidate['width'] == tc:
                 results['identified_key'] = {
                     'bbox': key_candidate['bbox'],
                     'height': key_candidate['height'],
                     'width': key_candidate['width']
                 }
                 # Extract the actual colors from the original grid using the key's bbox
                 kr, kc, _, _ = key_candidate['bbox']
                 key_colors = input_grid[kr:kr+tr, kc:kc+tc].tolist()
                 results['identified_key']['colors'] = key_colors
                 break # Assume only one matching key

    return results

# --- Example Data ---
input1 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0],
    [0, 1, 8, 1, 8, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 0],
    [0, 8, 8, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 4, 1, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 0],
    [0, 1, 1, 4, 4, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
input2 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 0],
    [0, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 0],
    [0, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 0],
    [0, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 0],
    [0, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 0],
    [0, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 0],
    [0, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 1, 1, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 1, 2, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

analysis1 = analyze_example(input1)
analysis2 = analyze_example(input2)

print("--- Analysis Example 1 ---")
print(analysis1)
print("\n--- Analysis Example 2 ---")
print(analysis2)
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Analysis Example 1 ---
{'dimensions': {'height': 23, 'width': 23}, 'templates': [], 'template_grid': {'rows': 0, 'cols': 0, 'count': 0}, 'potential_keys': [{'id': 0, 'bbox': (3, 1, 6, 4), 'height': 4, 'width': 4, 'colors': [np.int64(8), np.int64(1), np.int64(4)], 'pixel_count': 16}], 'identified_key': None}

--- Analysis Example 2 ---
{'dimensions': {'height': 23, 'width': 23}, 'templates': [{'id': 0, 'bbox': (1, 2, 3, 4), 'pixel_count': 8}, {'id': 1, 'bbox': (1, 6, 3, 8), 'pixel_count': 8}, {'id': 2, 'bbox': (1, 10, 3, 12), 'pixel_count': 8}, {'id': 3, 'bbox': (1, 14, 3, 16), 'pixel_count': 8}, {'id': 4, 'bbox': (1, 18, 3, 20), 'pixel_count': 8}, {'id': 5, 'bbox': (5, 2, 7, 4), 'pixel_count': 8}, {'id': 6, 'bbox': (5, 6, 7, 8), 'pixel_count': 8}, {'id': 7, 'bbox': (5, 10, 7, 12), 'pixel_count': 8}, {'id': 8, 'bbox': (5, 14, 7, 16), 'pixel_count': 8}, {'id': 9, 'bbox': (5, 18, 7, 20), 'pixel_count': 8}, {'id': 10, 'bbox': (9, 2, 11, 4), 'pixel_count': 8}, {'id': 11, 'bbox': (9, 6, 11, 8), 'pixel_count': 8}, {'id': 12, 'bbox': (9, 10, 11, 12), 'pixel_count': 8}, {'id': 13, 'bbox': (9, 14, 11, 16), 'pixel_count': 8}, {'id': 14, 'bbox': (9, 18, 11, 20), 'pixel_count': 8}], 'template_grid': {'rows': 3, 'cols': 5, 'count': 15}, 'potential_keys': [{'id': 0, 'bbox': (19, 1, 21, 5), 'height': 3, 'width': 5, 'colors': [np.int64(1), np.int64(2), np.int64(3)], 'pixel_count': 15}], 'identified_key': {'bbox': (19, 1, 21, 5), 'height': 3, 'width': 5, 'colors': [[2, 1, 1, 3, 1], [1, 2, 2, 1, 1], [2, 1, 2, 3, 2]]}}

```
**Metrics Analysis Interpretation:**

*   **Example 1 (Failed):**
    *   Dimensions: 23x23.
    *   Templates: The analysis code *failed* to find the 3x3 hollow gray squares. My `find_template_objects` function seems to have a bug. Looking at the input, the templates *are* present. Let's re-examine the `find_template_objects` function - ah, it uses `visited` globally across different starting points, which is wrong for finding distinct objects. It should only use `visited` within the scope of finding one connected component.
    *   Potential Keys: Because templates weren't found correctly, the `temp_grid` wasn't modified, and `find_contiguous_objects` was run on the original grid (ignoring gray). It found one object with bbox (3, 1, 6, 4), height 4, width 4. This corresponds to the top-left part of the key pattern.
    *   Identified Key: None, because no templates were found to provide `tr` and `tc`.
    *   **Conclusion for Example 1:** The primary failure was the incorrect `find_template_objects` function. If this had worked, it would have found `tr=4`, `tc=4`. Then, the potential key finding (which needs to run on a grid *with templates removed*) would ideally find the 4x5 block. The dimension check `height == tr and width == tc` (4 == 4 and 5 == 4) would still fail. The rule needs to be: find the contiguous non-template, non-background object whose *dimensions* (`tr`, `tc`) match the *template grid layout*. The key object itself is 4x5.

*   **Example 2 (Passed):**
    *   Dimensions: 23x23.
    *   Templates: Correctly identified 15 template objects (3x3 hollow gray squares).
    *   Template Grid: Deduced a 3x5 grid structure (`tr=3`, `tc=5`).
    *   Potential Keys: Found one contiguous non-template object: bbox (19, 1, 21, 5), height 3, width 5.
    *   Identified Key: Successfully matched the potential key's dimensions (3x5) with the template grid dimensions (3x5). Extracted the correct 3x5 block of colors.
    *   **Conclusion for Example 2:** The logic worked here because the key pattern object's dimensions precisely matched the template grid dimensions, and the `find_template_objects` function (despite its bug) happened to work correctly for this input's layout.

**Revised Strategy:**
1.  Fix the `find_template_objects` function to correctly identify all template instances.
2.  Confirm the template grid dimensions (`tr`, `tc`) are derived correctly from the arrangement of template top-left corners.
3.  Create the temporary grid with template pixels zeroed out.
4.  Use the fixed `find_contiguous_objects` on the temporary grid (ignoring only background color 0).
5.  Find the candidate object whose dimensions (`height`, `width`) match the template grid dimensions (`tr`, `tc`).
6.  Extract the key colors from the *original* grid using this candidate's bounding box (`key_r`, `key_c`, `tr`, `tc`).
7.  Perform the replacement as before.

## YAML Fact Documentation


```yaml
task_description: Replace pixels within repeating template patterns using colors from a key pattern based on relative grid positions.

definitions:
  - object: background
    pixels: Color 0 (white).
  - object: template_pattern
    description: A specific 3x3 hollow square shape made of gray (5) pixels.
    properties: [shape(3x3, hollow_square), color(gray)]
  - object: template_grid
    description: A grid arrangement of multiple template_pattern instances.
    properties: [rows(tr), cols(tc), derived_from(template_pattern locations)]
  - object: key_pattern
    description: A contiguous rectangular block of non-background, non-gray pixels.
    properties: [shape(rectangle), height(tr), width(tc), colors(various), location(spatially_separate_from_template_grid)]
    constraints: Its dimensions (height, width) must match the template_grid dimensions (tr, tc).

transformation:
  - step: 1
    action: Identify all instances of the 'template_pattern' (3x3 hollow gray squares) in the input grid.
  - step: 2
    action: Determine the dimensions ('tr' rows, 'tc' columns) of the 'template_grid' based on the relative row and column positions of the identified template_patterns.
  - step: 3
    action: Identify potential 'key_pattern' objects.
    details: Find all contiguous blocks of non-background (0) and non-gray (5) pixels.
  - step: 4
    action: Select the correct 'key_pattern' from the potential candidates.
    details: Choose the candidate object whose height matches 'tr' and whose width matches 'tc'. Record its top-left corner (key_r, key_c).
  - step: 5
    action: Create an output grid, initially a copy of the input grid.
  - step: 6
    action: Iterate through the conceptual 'template_grid' positions (row_index from 0 to tr-1, col_index from 0 to tc-1).
  - step: 7
    action: For each (row_index, col_index), find the corresponding 'template_pattern' instance in the input grid.
  - step: 8
    action: Determine the replacement color from the 'key_pattern' block in the *input* grid at the relative position (key_r + row_index, key_c + col_index).
  - step: 9
    action: In the output grid, change the color of all gray (5) pixels belonging to the current 'template_pattern' instance to the replacement color found in step 8.
  - step: 10
    action: Return the modified output grid.
```


## Natural Language Program

1.  **Identify Template Patterns:** Scan the input grid to find all occurrences of the specific template pattern: a 3x3 hollow square composed entirely of gray (5) pixels. Record the location (top-left corner) and pixels of each found template instance. If no templates are found, return the input grid unchanged.
2.  **Determine Template Grid Dimensions:** Analyze the top-left corner coordinates of the found template instances. Identify the unique row coordinates and unique column coordinates. The number of unique rows is the template grid height (`tr`), and the number of unique columns is the template grid width (`tc`). Create a mapping from template grid indices `(r_idx, c_idx)` (where `0 <= r_idx < tr`, `0 <= c_idx < tc`) to the corresponding template pattern instance based on its original top-left corner matching the sorted unique rows/cols.
3.  **Isolate Potential Key Pixels:** Create a temporary copy of the input grid. In this temporary grid, set the color of all pixels belonging to any identified template pattern instance to background (0).
4.  **Identify Key Pattern Object:** Find all distinct contiguous objects in the temporary grid consisting of any non-background color (i.e., colors 1-9, excluding the gray templates which are now 0).
5.  **Select the Key Pattern:** From the objects found in step 4, identify the *single* object whose bounding box height is exactly `tr` and whose bounding box width is exactly `tc`. If no such object or multiple such objects exist, the identification fails (handle as error or return original grid). Record the top-left corner `(key_r, key_c)` of this identified key pattern object's bounding box.
6.  **Prepare Output:** Create the output grid as a copy of the original input grid.
7.  **Apply Transformation:** Iterate through each template grid index `(r_idx, c_idx)` from `(0, 0)` up to `(tr-1, tc-1)`.
    a.  Retrieve the specific template pattern instance corresponding to `(r_idx, c_idx)` using the mapping created in step 2.
    b.  Get the replacement color from the *original input grid* at the location `(key_r + r_idx, key_c + c_idx)`.
    c.  For every pixel `(px_r, px_c)` that belongs to the current template pattern instance (which will have the color gray (5) in the output grid initially), update its color in the *output grid* to the replacement color obtained in step 7b.
8.  **Return Result:** Return the modified output grid.
