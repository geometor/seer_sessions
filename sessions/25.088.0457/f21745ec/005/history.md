
Previous Code:
```python
import numpy as np
from collections import deque

# Define white color constant
WHITE = 0

def find_objects(grid):
    """
    Finds connected components of non-white colors in the grid using BFS.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of tuples, where each tuple contains:
              (color (int), set_of_pixels (set of (r, c) tuples)).
    """
    objects = []
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)

    for r in range(height):
        for c in range(width):
            if grid[r, c] != WHITE and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if obj_pixels:
                    objects.append((color, obj_pixels))

    return objects

def get_bounding_box(pixels):
    """
    Calculates the bounding box for a set of pixels.

    Args:
        pixels (set): A set of (row, col) tuples.

    Returns:
        tuple: (min_row, min_col, max_row, max_col) or None if pixels is empty.
    """
    if not pixels:
        return None
    rows = [r for r, c in pixels]
    cols = [c for r, c in pixels]
    return min(rows), min(cols), max(rows), max(cols)

def transform(input_grid):
    """
    Transforms the input grid based on object properties.

    Rule:
    1. Identify all non-white connected objects.
    2. For each object:
       a. Determine its bounding box.
       b. Check if the object perfectly forms the border of its bounding box AND
          all pixels strictly inside the bounding box are white. Call this a "perfect hollow rectangle".
       c. Calculate the area of the region strictly inside the bounding box (interior area).
    3. Apply transformation:
       a. If the object is a perfect hollow rectangle:
          i. If its interior area is >= 10: Fill the interior white pixels with the object's color.
          ii. If its interior area is < 10: Remove the object (set its pixels to white).
       b. Else (if the object is not a perfect hollow rectangle OR its interior contains non-white pixels):
          Keep the object as is.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    objects = find_objects(input_grid)

    for color, object_pixels in objects:
        # Find bounding box
        bbox = get_bounding_box(object_pixels)
        if bbox is None:
            continue
        min_r, min_c, max_r, max_c = bbox

        # Calculate dimensions and interior area
        obj_height = max_r - min_r + 1
        obj_width = max_c - min_c + 1
        interior_area = max(0, obj_height - 2) * max(0, obj_width - 2)

        # Check properties: perfect hollow rectangle and interior content
        is_perfect_hollow_rectangle = True
        interior_is_only_white = True
        interior_pixels_to_fill = [] # Keep track of pixels to fill later

        # If width or height is less than 3, it cannot have a hollow interior
        if obj_width < 3 or obj_height < 3:
             is_perfect_hollow_rectangle = False # Cannot be hollow if too small
             # We still need to check if *all* pixels match the border in this case,
             # otherwise it's a complex shape.
             if len(object_pixels) != (obj_height * obj_width): # check if solid rectangle
                 is_perfect_hollow_rectangle = False # If not solid, it's complex/irregular

        # Check if the object pixels perfectly match the border and if interior is white
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                is_border = (r == min_r or r == max_r or c == min_c or c == max_c)

                if is_border:
                    # If a border pixel is NOT part of the object, it's not a perfect hollow rect
                    if (r, c) not in object_pixels:
                        is_perfect_hollow_rectangle = False
                else: # Inside the bounding box
                    # If an interior pixel IS part of the object, it's not a perfect hollow rect
                    if (r, c) in object_pixels:
                        is_perfect_hollow_rectangle = False
                    # If an interior pixel is NOT white, the interior is not only white
                    if input_grid[r, c] != WHITE:
                        interior_is_only_white = False
                    # If interior is white, add to potential fill list
                    elif input_grid[r, c] == WHITE:
                        interior_pixels_to_fill.append((r, c))

        # One final check: ensure the number of object pixels matches the border pixel count
        # for potential perfect hollow rectangles (this guards against extra pixels).
        # Border pixel count = 2 * width + 2 * height - 4 (subtract corners counted twice)
        # Handle edge cases where width or height is 1 or 2
        if obj_width <= 1 or obj_height <= 1:
             border_pixel_count = obj_width * obj_height
        elif obj_width == 2 or obj_height == 2:
             border_pixel_count = obj_width * obj_height # Border is the whole thing
        else:
             border_pixel_count = 2 * obj_width + 2 * (obj_height - 2)

        if len(object_pixels) != border_pixel_count:
            is_perfect_hollow_rectangle = False


        # Apply transformation rule based on checks
        if is_perfect_hollow_rectangle and interior_is_only_white:
            if interior_area >= 10:
                # Fill the interior white pixels
                for r_in, c_in in interior_pixels_to_fill:
                     # Double check it's inside the bounding box and white (safety)
                     if min_r < r_in < max_r and min_c < c_in < max_c and output_grid[r_in, c_in] == WHITE:
                         output_grid[r_in, c_in] = color
            else: # interior_area < 10
                # Remove the object
                for r_obj, c_obj in object_pixels:
                    output_grid[r_obj, c_obj] = WHITE
        # Else (not perfect hollow rect OR interior not only white): Keep the object (do nothing)

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 3 0 0 0 0 2 2 2 2 2
0 0 0 0 0 0 0 3 0 0 0 3 0 0 0 0 2 0 0 0 2
0 0 0 0 0 0 0 3 0 0 0 3 0 0 0 0 2 0 0 0 2
0 0 0 0 0 0 0 3 0 0 0 3 0 0 0 0 2 0 0 0 2
0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 2 0 0 0 2
0 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2
0 4 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 4 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 5 0 5 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 0 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 0 0 5 0 0 0 0 0
0 0 0 7 7 7 7 7 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 7 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 3 0 3 0 0 0 0 2 2 2 2 2
0 0 0 0 0 0 0 3 3 3 0 3 0 0 0 0 2 0 2 0 2
0 0 0 0 0 0 0 3 0 3 3 3 0 0 0 0 2 2 2 0 2
0 0 0 0 0 0 0 3 3 0 0 3 0 0 0 0 2 0 2 2 2
0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 2 2 0 0 2
0 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2
0 4 0 4 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 4 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 5 0 5 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 0 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 2 2 2 2 2
0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 2 2 2 2 2
0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 2 2 2 2 2
0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 2 2 2 2 2
0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 2 2 2 2 2
0 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2
0 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 5 0 5 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 0 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 18
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 8.163265306122469

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 8 0 0 6 6 6 6 6 6 6 6
0 8 0 8 8 0 0 0 8 0 0 6 0 0 0 0 0 0 6
0 8 8 8 0 8 8 0 8 0 0 6 0 0 0 0 0 0 6
0 8 0 0 8 8 0 8 8 0 0 6 0 0 0 0 0 0 6
0 8 0 0 0 0 8 0 8 0 0 6 0 0 0 0 0 0 6
0 8 8 8 8 8 8 8 8 0 0 6 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 4 0 0 5 5 5 5 5 0
0 0 0 4 0 0 0 0 0 0 4 0 0 5 0 0 0 5 0
0 0 0 4 0 0 0 0 0 0 4 0 0 5 0 0 0 5 0
0 0 0 4 0 0 0 0 0 0 4 0 0 5 0 0 0 5 0
0 0 0 4 0 0 0 0 0 0 4 0 0 5 5 5 5 5 0
0 0 0 4 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 8 0 0 6 6 6 6 6 6 6 6
0 8 0 8 8 0 0 0 8 0 0 6 0 0 0 0 0 6 6
0 8 8 8 0 8 8 0 8 0 0 6 0 6 6 0 0 0 6
0 8 0 0 8 8 0 8 8 0 0 6 6 6 0 6 6 0 6
0 8 0 0 0 0 8 0 8 0 0 6 0 0 6 6 0 6 6
0 8 8 8 8 8 8 8 8 0 0 6 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 4 4 0 0 0 0 0 0 0 0
0 0 0 4 0 4 4 0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 4 4 0 4 0 0 0 0 0 0 0 0
0 0 0 4 0 0 4 4 0 4 4 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 4 0 4 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 8 0 0 6 6 6 6 6 6 6 6
0 8 0 8 8 0 0 0 8 0 0 6 6 6 6 6 6 6 6
0 8 8 8 0 8 8 0 8 0 0 6 6 6 6 6 6 6 6
0 8 0 0 8 8 0 8 8 0 0 6 6 6 6 6 6 6 6
0 8 0 0 0 0 8 0 8 0 0 6 6 6 6 6 6 6 6
0 8 8 8 8 8 8 8 8 0 0 6 6 6 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 38
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 21.05263157894737

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 3 3 3 3 0 0
0 0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 3 0 0 3 0 0
0 0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 3 0 0 3 0 0
0 0 0 0 0 2 2 2 2 2 2 2 0 0 0 0 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 0 8 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 0 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 0 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 8 0 8 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0
8 8 8 8 8 8 8 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0
0 0 7 7 7 7 7 7 0 0 0 1 0 0 0 0 0 1 0 0 0 0
0 0 7 0 0 0 0 7 0 0 0 1 0 0 0 0 0 1 0 0 0 0
0 0 7 0 0 0 0 7 0 0 0 1 1 1 1 1 1 1 0 0 0 0
0 0 7 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 2 0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 0 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 2 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 0 8 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 0 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 0 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 8 0 8 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0
8 8 8 8 8 8 8 0 0 0 0 1 0 1 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1 0 1 1 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 0 8 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 0 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 0 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 8 0 8 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0
8 8 8 8 8 8 8 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0
0 0 7 7 7 7 7 7 0 0 0 1 1 1 1 1 1 1 0 0 0 0
0 0 7 7 7 7 7 7 0 0 0 1 1 1 1 1 1 1 0 0 0 0
0 0 7 7 7 7 7 7 0 0 0 1 1 1 1 1 1 1 0 0 0 0
0 0 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 62
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 51.23966942148763
