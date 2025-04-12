
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 0 0 0 0
0 0 0 2 0 2 0 0 0 0
0 0 0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 1 1 1 1 0
0 3 3 0 0 1 0 0 1 0
0 3 3 0 0 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0
0 0
0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 4 4 0
0 0 0 0 0 4 4 4 4 0
0 7 7 7 0 4 4 4 4 0
0 7 0 7 0 4 4 4 4 0
0 7 0 7 0 0 0 0 0 0
0 7 0 7 0 8 8 8 0 0
0 7 0 7 0 8 0 8 0 0
0 7 7 7 0 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
```


## train_3

**input:**
```
0 6 6 6 6 6 0 8 8 8
0 6 0 0 0 6 0 8 0 8
0 6 6 6 6 6 0 8 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 0
0 2 2 2 0 0 4 0 4 0
0 2 2 2 0 0 4 0 4 0
0 2 2 2 0 0 4 4 4 0
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
```


**output:**
```
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
```

*   **Perception of the elements:**
    *   Each input grid contains multiple distinct geometric shapes (objects) composed of contiguous pixels of the same non-white color.
    *   The objects have different colors, shapes, sizes (heights and widths), and positions.
    *   The output grid is always composed entirely of white pixels.
    *   The size (dimensions) of the output grid varies between examples and appears to depend on properties derived from the objects in the input grid.

*   **YAML block documenting facts:**
    
```yaml
    examples:
      train_1:
        input_objects:
          - color: 2 (red)
            shape: G
            height: 3
            width: 3
          - color: 3 (green)
            shape: L
            height: 3
            width: 2
          - color: 1 (blue)
            shape: T
            height: 3
            width: 4
        properties:
          num_objects: 3
          unique_colors: 3 # (1, 2, 3)
          max_height: 3
          object_with_color_equals_height: # Green object (color 3, height 3)
            height: 3
            width: 2
          condition_N_equals_C: True # num_objects (3) == unique_colors (3)
        derived_output_dims:
          rule_C_equals_H: 3x2
          rule_MaxH_x_C_minus_1: 3x2 # MaxH=3, C=3 -> 3 x (3-1)
        output_dimensions: 3x2
        rule_applied: rule_C_equals_H # or either as they match
      train_2:
        input_objects:
          - color: 4 (yellow)
            shape: Square
            height: 4
            width: 4
          - color: 7 (orange)
            shape: H
            height: 5
            width: 3
          - color: 8 (azure)
            shape: G
            height: 3
            width: 3
        properties:
          num_objects: 3
          unique_colors: 3 # (4, 7, 8)
          max_height: 5
          object_with_color_equals_height: # Yellow object (color 4, height 4)
            height: 4
            width: 4
          condition_N_equals_C: True # num_objects (3) == unique_colors (3)
        derived_output_dims:
          rule_C_equals_H: 4x4
          rule_MaxH_x_C_minus_1: 5x2 # MaxH=5, C=3 -> 5 x (3-1)
        output_dimensions: 4x4
        rule_applied: rule_C_equals_H
      train_3:
        input_objects:
          - color: 6 (magenta)
            shape: C
            height: 3
            width: 5
          - color: 8 (azure)
            shape: G
            height: 3
            width: 3
          - color: 4 (yellow)
            shape: T
            height: 4
            width: 3
          - color: 2 (red)
            shape: Bar1
            height: 5
            width: 1
          - color: 2 (red)
            shape: Bar2
            height: 5
            width: 1
        properties:
          num_objects: 5
          unique_colors: 4 # (2, 4, 6, 8)
          max_height: 5
          object_with_color_equals_height: # Yellow object (color 4, height 4)
            height: 4
            width: 3
          condition_N_equals_C: False # num_objects (5) != unique_colors (4)
        derived_output_dims:
          rule_C_equals_H: 4x3
          rule_MaxH_x_C_minus_1: 5x3 # MaxH=5, C=4 -> 5 x (4-1)
        output_dimensions: 5x3
        rule_applied: rule_MaxH_x_C_minus_1

    ```


*   **Natural language program:**
    1.  Identify all distinct contiguous objects of non-white color in the input grid.
    2.  For each object, determine its height, width, and color value.
    3.  Count the total number of distinct objects found (N).
    4.  Count the number of unique non-white colors present across all objects (C).
    5.  Check if the number of objects (N) is equal to the number of unique colors (C).
    6.  **If N equals C:**
        a.  Search for an object where its color value is numerically equal to its height. (Assume there will be at most one such object relevant).
        b.  If such an object is found, the output grid's dimensions are the height and width of this specific object.
        c.  (Implicit fallback, though not needed for examples: If no such object is found, calculate MaxH (maximum height among all objects) and the output dimensions are MaxH by (C-1)).
    7.  **If N is not equal to C:**
        a.  Calculate MaxH, the maximum height among all identified objects.
        b.  The output grid's dimensions are MaxH by (C - 1).
    8.  Create the output grid with the determined height and width, filling all its pixels with the white color (0).
```python
import numpy as np
from collections import deque

"""
1. Identify all distinct contiguous objects of non-white color (0) in the input grid.
2. For each object, determine its height, width, and color value.
3. Count the total number of distinct objects found (N).
4. Count the number of unique non-white colors present across all objects (C).
5. Check if N equals C.
6. If N equals C:
   a. Search for an object where its color value is numerically equal to its height.
   b. If found, the output grid's dimensions are the height and width of this specific object.
   c. (Fallback, not explicitly needed by examples) If no such object found, use the N != C rule.
7. If N is not equal to C:
   a. Calculate MaxH, the maximum height among all identified objects.
   b. The output grid's dimensions are MaxH by (C - 1). Ensure width is at least 0.
8. Create the output grid with the determined height and width, filling all its pixels with the white color (0).
"""

def find_objects(grid: np.ndarray) -> list[dict]:
    """
    Finds all contiguous objects of non-white colors in the grid.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains its color, pixels (list of tuples), height, and width.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0 and not visited[r, c]:
                obj_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.popleft()
                    obj_pixels.append((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check neighbors (4-directional adjacency)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                height = max_r - min_r + 1
                width = max_c - min_c + 1
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'height': height,
                    'width': width
                })
    return objects

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the properties of the contained objects.
    The output grid is always white, with dimensions determined by rules
    comparing the number of objects (N), the number of unique colors (C),
    the maximum object height (MaxH), and a condition where an object's
    color value equals its height.
    """
    grid_np = np.array(input_grid, dtype=int)

    # 1. Find all objects
    objects = find_objects(grid_np)

    # Handle case with no non-white objects
    if not objects:
        return [[0]] # Or based on specific requirement for empty inputs

    # 2. Gather properties: N, C, MaxH
    num_objects = len(objects)
    unique_colors = set(obj['color'] for obj in objects)
    num_unique_colors = len(unique_colors)
    max_height = 0
    if objects: # Ensure there are objects before calculating max height
        max_height = max(obj['height'] for obj in objects)

    output_height = 0
    output_width = 0

    # 5. Check if N equals C
    if num_objects == num_unique_colors:
        # 6a. Search for object where color == height
        found_special_object = False
        for obj in objects:
            if obj['color'] == obj['height']:
                # 6b. Use this object's dimensions
                output_height = obj['height']
                output_width = obj['width']
                found_special_object = True
                break
        # 6c. Fallback (if no special object found, use N != C rule)
        if not found_special_object:
             output_height = max_height
             # Ensure width is non-negative
             output_width = max(0, num_unique_colors - 1)
    else:
        # 7. N is not equal to C
        # 7a. Calculate MaxH (already done)
        # 7b. Dimensions are MaxH by (C - 1)
        output_height = max_height
        # Ensure width is non-negative
        output_width = max(0, num_unique_colors - 1)

    # Handle cases where calculated dimensions might be zero
    if output_height <= 0 or output_width <= 0:
       # Default to a 1x1 white grid if dimensions are invalid,
       # although the logic seems to prevent this with the given examples.
       output_height = max(1, output_height)
       output_width = max(1, output_width)
       # print(f"Warning: Calculated zero dimension. N={num_objects}, C={num_unique_colors}, MaxH={max_height}. Defaulting to {output_height}x{output_width}")


    # 8. Create the output grid filled with white (0)
    output_grid_np = np.zeros((output_height, output_width), dtype=int)

    return output_grid_np.tolist()
```
