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