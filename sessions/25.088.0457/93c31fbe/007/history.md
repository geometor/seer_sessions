
Previous Code:
```python
import numpy as np
from collections import defaultdict
import copy
import math

"""
Transformation Rule:

1.  Initialize the output grid as a copy of the input grid.
2.  Set all original blue (1) pixels in the output grid to white (0).
3.  Find all connected components (objects) in the input grid that are neither white (0) nor blue (1).
4.  For each object, calculate its canonical shape signature based on the relative coordinates of its pixels from its top-leftmost point.
5.  Group the identified objects based on having the exact same color and shape signature.
6.  Identify groups that contain exactly two objects (these are the pairs).
7.  For each identified pair of objects (Object A and Object B):
    a.  Determine the fixed translation (row offset `dr_obj`, column offset `dc_obj`) that maps the position of Object A's top-left corner to Object B's top-left corner.
    b.  Iterate through each pixel `(r_A, c_A)` belonging to Object A.
    c.  Find the corresponding pixel `(r_B, c_B)` in Object B using the translation: `r_B = r_A + dr_obj`, `c_B = c_A + dc_obj`.
    d.  Draw a line segment between the corresponding pixel pair `(r_A, c_A)` and `(r_B, c_B)` using a line drawing algorithm.
    e.  The line drawing process involves:
        i. Calculating the differences: `dr_line = r_B - r_A`, `dc_line = c_B - c_A`.
        ii. Determining the number of steps: `num_steps = max(abs(dr_line), abs(dc_line))`.
        iii. Iterating from step `i = 1` to `num_steps - 1` (excluding the start and end points).
        iv. Calculating the intermediate point coordinates: `r_intermediate = r_A + (dr_line * i) / num_steps`, `c_intermediate = c_A + (dc_line * i) / num_steps`.
        v. Rounding the intermediate coordinates to the nearest integer: `r_pixel = round(r_intermediate)`, `c_pixel = round(c_intermediate)`.
        vi. Checking if the pixel `(r_pixel, c_pixel)` is within the grid boundaries.
        vii. If the pixel `(r_pixel, c_pixel)` in the *output grid* is currently white (0), set its color to blue (1).
8.  Return the modified output grid.
"""

def find_objects(grid, ignore_colors={0}):
    """
    Finds connected objects of the same color in the grid, ignoring specified colors.

    Args:
        grid (np.ndarray): The input grid.
        ignore_colors (set): Set of color values to ignore.

    Returns:
        list: A list of dictionaries, each representing an object with
              'color' (int), 'coords' (set of (row, col) tuples),
              and 'min_coord' (tuple of (min_r, min_c)).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] not in ignore_colors:
                color = grid[r, c]
                obj_coords = set()
                q = [(r, c)]
                visited[r, c] = True
                min_r, min_c = r, c

                while q:
                    row, col = q.pop(0)
                    obj_coords.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if obj_coords:
                    # Find the true minimum coordinate after collecting all coords
                    actual_min_r = min(r_coord for r_coord, c_coord in obj_coords)
                    actual_min_c = min(c_coord for r_coord, c_coord in obj_coords)
                    objects.append({
                        'color': color,
                        'coords': obj_coords,
                        'min_coord': (actual_min_r, actual_min_c)
                    })
    return objects

def get_shape_signature(obj_coords):
    """
    Calculates a canonical representation (signature) of an object's shape.
    The signature is based on the relative coordinates of the object's pixels
    from its top-left corner.

    Args:
        obj_coords (set): A set of (row, col) tuples representing the object's pixels.

    Returns:
        frozenset: A frozenset of relative (dr, dc) coordinates, representing the shape.
                   Returns None if obj_coords is empty.
    """
    if not obj_coords:
        return None
    min_r = min(r for r, c in obj_coords)
    min_c = min(c for r, c in obj_coords)
    relative_coords = frozenset((r - min_r, c - min_c) for r, c in obj_coords)
    return relative_coords

def draw_line(grid, r1, c1, r2, c2, color):
    """
    Draws a line between (r1, c1) and (r2, c2) on the grid with the specified color.
    Only modifies pixels that are currently white (0). Uses integer rounding for points.
    Does not draw the start or end points themselves.

    Args:
        grid (np.ndarray): The grid to draw on (modified in-place).
        r1, c1 (int): Coordinates of the starting point.
        r2, c2 (int): Coordinates of the ending point.
        color (int): The color to draw the line with.
    """
    rows, cols = grid.shape
    dr = r2 - r1
    dc = c2 - c1

    if dr == 0 and dc == 0:
        return # Points are the same, no line needed

    num_steps = max(abs(dr), abs(dc))

    if num_steps == 0: # Should not happen if dr/dc != 0, but safety check
         return

    # Iterate through intermediate points (excluding start and end)
    for i in range(1, num_steps):
        t = i / num_steps
        r_intermediate = r1 + t * dr
        c_intermediate = c1 + t * dc

        # Round to nearest pixel coordinates
        r_pixel = int(round(r_intermediate))
        c_pixel = int(round(c_intermediate))

        # Check bounds and if the pixel is white
        if 0 <= r_pixel < rows and 0 <= c_pixel < cols:
            if grid[r_pixel, c_pixel] == 0:
                 grid[r_pixel, c_pixel] = color

def transform(input_grid):
    """
    Transforms the input grid by finding pairs of identical objects (non-white, non-blue),
    removing original blue pixels, and drawing blue lines between corresponding
    pixels of each pair using a line drawing algorithm.

    Args:
        input_grid (np.ndarray): The input 2D numpy array.

    Returns:
        np.ndarray: The transformed 2D numpy array.
    """
    # 1. Initialize Output Grid
    output_grid = copy.deepcopy(input_grid)
    rows, cols = output_grid.shape

    # 2. Clear Existing Blue pixels
    output_grid[output_grid == 1] = 0

    # 3. Identify non-white, non-blue objects in the *original* input grid
    # We ignore blue (1) here because they are irrelevant for pairing and already cleared in output
    objects = find_objects(input_grid, ignore_colors={0, 1})

    # 4 & 5. Group objects by color and shape signature
    objects_by_signature = defaultdict(list)
    for obj in objects:
        signature = (obj['color'], get_shape_signature(obj['coords']))
        if signature[1] is not None: # Ensure shape signature is valid
             objects_by_signature[signature].append(obj)

    # 6 & 7. Find pairs and connect them
    for signature, obj_list in objects_by_signature.items():
        if len(obj_list) == 2:
            # Found a pair
            obj_A, obj_B = obj_list[0], obj_list[1]

            # 7a. Determine translation between the pair based on top-left corners
            min_r_A, min_c_A = obj_A['min_coord']
            min_r_B, min_c_B = obj_B['min_coord']
            dr_obj = min_r_B - min_r_A
            dc_obj = min_c_B - min_c_A

            # 7b & 7c. Iterate through pixels of Object A and find corresponding in B
            for r_A, c_A in obj_A['coords']:
                r_B = r_A + dr_obj
                c_B = c_A + dc_obj

                # Check if the corresponding pixel actually exists in Object B
                # This is a sanity check, should always be true for identical shapes/translations
                if (r_B, c_B) in obj_B['coords']:
                    # 7d & 7e. Draw a line between the corresponding points (r_A, c_A) and (r_B, c_B)
                    # The draw_line function handles only coloring white pixels (0) with blue (1)
                    draw_line(output_grid, r_A, c_A, r_B, c_B, 1)

    # 8. Final Output
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 0 0 8 8 0
0 0 0 8 8 0 0 0 8 8 0 0 0 0 0 0 8 0 0 0 0 8 0
0 0 0 8 0 1 0 0 0 8 0 0 0 0 0 0 0 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0
0 0 0 8 1 1 0 0 0 8 0 0 1 1 0 0 0 0 1 1 0 0 0
0 0 0 8 8 0 0 0 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 8 0
0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 0 0 8 8 0 0 0 0 0 0 0 0
0 0 1 0 0 0 8 0 0 0 0 0 1 0 8 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 1 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 0 0 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 0 0 8 8 0
0 0 0 8 8 0 0 0 8 8 0 0 0 0 0 0 8 0 0 0 0 8 0
0 0 0 8 0 1 0 1 0 8 0 0 0 0 0 0 0 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0
0 0 0 8 1 1 0 1 1 8 0 0 0 0 0 0 0 0 1 1 0 0 0
0 0 0 8 8 0 0 0 8 8 0 0 0 0 0 0 0 0 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 0 0 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 1 0 0 0 1 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 0 0 0 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 1 0 1 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 0 0 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 0 0 8 8 0
0 0 0 8 8 0 0 0 8 8 0 0 0 0 0 0 8 0 0 0 0 8 0
0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 0 0 0 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 0 0 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 0 0 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 24
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 9.486166007905126

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 1 1 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 2 2 0 2 2 0
0 0 2 0 0 0 0 0 1 0 0 0 0 0 0 2 0 0 0 2 0 0 0 2 0
0 0 2 2 0 0 0 0 0 0 0 0 0 0 2 2 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 2 0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 2 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 0 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 2 2 0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 1 1 0 0 1 1 0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 0 0 2 2 0 2 2 0
0 0 2 0 0 0 0 0 1 1 0 0 0 0 0 2 0 0 0 2 0 0 0 2 0
0 0 2 2 0 0 0 0 0 0 0 0 0 0 2 2 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 2 2 0 2 2 0 0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 2 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 2 2 0 2 2 0
0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 2 0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 0 2 2 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 2 0 0 0 2 0
0 0 2 2 0 0 0 0 0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 2 0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 2 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 0 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 2 0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 22
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 7.65217391304347

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 3 3 0 0 0 1 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 1 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 0 1 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 3 0 0 0 0 0 3 0 0 0
0 0 1 1 0 0 0 0 0 0 0 3 3 0 0 0 3 3 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 1 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 1 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 0 1 0 1 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 1 1 0 0 0 3 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 0 0 0 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 0 0 0 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0 0 0 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 0 0 0 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 0 0 0 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1 1 0 0 0 1 1 0 0 0 0 0
0 0 0 3 0 0 0 0 0 3 1 1 0 0 0 1 1 0 0 0 0
0 0 0 3 3 1 0 0 3 3 1 1 0 0 0 1 1 0 0 0 0
0 0 0 0 1 1 1 0 0 1 1 3 3 0 0 0 3 3 0 0 0
0 0 0 0 0 0 1 1 1 0 0 3 1 1 1 0 0 3 0 0 0
0 0 0 0 0 0 0 0 1 1 1 0 0 1 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 1 1 3 0 0 1 1 1 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 68
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 32.38095238095238
