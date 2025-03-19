# be94b721 • 006 • refine_coder

---
```python
"""
1.  **Identify Objects:** Locate all contiguous blocks of pixels with the same color in the input grid.
2.  **Target Object(s):** Focus on objects of color 2 (red).
3.  **Find smallest red object:** Of the red objects, find the object with the smallest area.
4. **Determine Bounding Box of smallest shape:** Find the smallest rectangle that contains all pixels of the *smallest* red object.
5.  **Extract and Transform:** Create a new grid (the output grid) with the dimensions of the bounding box determined in the previous step. Copy *only* the pixels of the smallest red object to the output grid, maintaining their relative positions within the bounding box.
6.  **Discard Other Objects:** Ignore all other objects and colors.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, obj_coords):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        obj_coords.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r, c]
                obj_coords = []
                dfs(r, c, color, obj_coords)
                if obj_coords:
                    objects.append((color, obj_coords))
    return objects

def bounding_box(coords):
    """Calculates the bounding box of a set of coordinates."""
    min_r = min(r for r, _ in coords)
    max_r = max(r for r, _ in coords)
    min_c = min(c for _, c in coords)
    max_c = max(c for _, c in coords)
    return min_r, min_c, max_r, max_c

def calculate_area(coords):
    """Calculates the area of an object based on its coordinates."""
    return len(coords)
    

def transform(input_grid):
    # Find all objects
    objects = find_objects(input_grid)

    # Find all red objects (color 2)
    red_objects = []
    for color, coords in objects:
        if color == 2:
            red_objects.append(coords)
            
    if not red_objects:
        return np.zeros((0,0), dtype=int)

    # Find the smallest red object
    smallest_red_object = min(red_objects, key=calculate_area, default=None)

    if smallest_red_object is None:
       return np.zeros((0, 0), dtype=int)


    # Determine the bounding box of the smallest red object
    min_r, min_c, max_r, max_c = bounding_box(smallest_red_object)

    # Create an output grid based on the bounding box
    output_height = max_r - min_r + 1
    output_width = max_c - min_c + 1
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Copy the smallest red object to the output grid
    for r, c in smallest_red_object:
        output_grid[r - min_r, c - min_c] = 2

    return output_grid
```
