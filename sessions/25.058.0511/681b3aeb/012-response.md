# 681b3aeb • 012 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find all distinct objects within the input grid. An object is a contiguous region of pixels sharing the same color (excluding black/background).
2.  **Bounding Boxes:** For *each* identified object, determine its bounding box. The bounding box is the smallest rectangle that completely encloses the object.
3.  **Sort Objects:** Sort the objects based on the top-left corner coordinates (row, then column) of their bounding boxes. This determines the order in which objects are placed.
4.  **Iterative Placement:** Create an initially empty output grid. Iterate through the sorted objects. For each object:
    *   Find the next available top-left position in the output grid. Initially, this is (0, 0). For subsequent objects find the next available position.
    *   Copy the object's pixels into the output grid, starting at the calculated top-left position.
    *   The size of output grid should change based on current object's placement.
5. **Output:** Return the final output grid.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies and returns a list of distinct colored objects in the grid.
    Each object is represented as a list of (row, col) coordinates.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, obj):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] != color:
            return
        visited.add((row, col))
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for row in range(rows):
        for col in range(cols):
            color = grid[row, col]
            if color != 0 and (row, col) not in visited:
                obj = []
                dfs(row, col, color, obj)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj)
    return objects

def get_object_bounding_box(obj):
    """Calculates the bounding box for a single object."""
    min_row, min_col = float('inf'), float('inf')
    max_row, max_col = float('-inf'), float('-inf')
    for row, col in obj:
        min_row = min(min_row, row)
        min_col = min(min_col, col)
        max_row = max(max_row, row)
        max_col = max(max_col, col)
    return min_row, min_col, max_row, max_col

def transform(input_grid):
    # Identify Objects
    objects = get_objects(input_grid)

    # Bounding Boxes and Sort Objects
    sorted_objects = []
    for color, obj_list in objects.items():
        for obj in obj_list:
           ob_min_row, ob_min_col, ob_max_row, ob_max_col = get_object_bounding_box(obj)
           sorted_objects.append((color, obj, (ob_min_row, ob_min_col, ob_max_row, ob_max_col)))

    sorted_objects.sort(key=lambda x: (x[3][0], x[3][1])) # sort by topleft corner

    # Iterative Placement
    output_grid = np.zeros((1, 1), dtype=int)  # Initialize with a small size

    for color, obj, (ob_min_row, ob_min_col, ob_max_row, ob_max_col) in sorted_objects:
        # Find next available top-left position
        next_row = 0
        next_col = 0
        
        if output_grid.size > 0 :
            max_r, max_c = output_grid.shape
            
            
        # get object bounding box dimensions
        o_rows = ob_max_row - ob_min_row + 1
        o_cols = ob_max_col - ob_min_col + 1
        
        # Resize output_grid if needed
        new_rows = max(output_grid.shape[0], next_row + o_rows)
        new_cols = max(output_grid.shape[1], next_col + o_cols)

        
        temp_grid = np.zeros((new_rows, new_cols), dtype=int)
        temp_grid[:output_grid.shape[0], :output_grid.shape[1]] = output_grid
        output_grid = temp_grid
        

        # Copy object's pixels
        for r in range(o_rows):
            for c in range(o_cols):
                output_grid[next_row + r, next_col + c] = input_grid[ob_min_row + r, ob_min_col + c]

    return output_grid
```
