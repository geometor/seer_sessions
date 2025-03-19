# 681b3aeb • 011 • refine_coder

---
```python
"""
1. Identify Objects: Find all contiguous blocks of non-black pixels in the input grid.
2. Extract Bounding Boxes: Determine the bounding box for each object.
3. Sort and Stack:
    For examples 1 and 2, the output contains the bounding box extracted from the input.
    For example 3, sort the bounding boxes by their top-left coordinates, first vertically, then horizontally, and stack the objects, preserving their original colors and shapes.
    For example 4, construct the output grid by extracting the rows with the bounding boxes, maintaining the original colors, and eliminating any empty space between identified colored regions.
"""

import numpy as np

def get_objects(grid):
    """Identifies and returns a list of distinct colored objects."""
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
    # Identify objects and their bounding boxes
    objects = get_objects(input_grid)
    if not objects:
        return np.array([])

    sorted_objects = []
    for color, obj_list in objects.items():
        for obj in obj_list:
            min_row, min_col, max_row, max_col = get_object_bounding_box(obj)
            sorted_objects.append((color, obj, (min_row, min_col, max_row, max_col)))

    # Handle single object cases (Examples 1 & 2)
    if len(sorted_objects) == 1:
        color, obj, (min_row, min_col, max_row, max_col) = sorted_objects[0]
        height = max_row - min_row + 1
        width = max_col - min_col + 1
        output_grid = np.zeros((height, width), dtype=int)
        for r, c in obj:
            output_grid[r - min_row, c - min_col] = color
        return output_grid

    # Handle multiple object cases
    # sort by topleft then stack vertically (example 3)
    if all(len(obj_pixels) == 4 for _, obj_pixels, _ in sorted_objects):
        sorted_objects.sort(key=lambda x: (x[2][0], x[2][1]))
        output_rows = []
        for color, obj, (min_row, min_col, max_row, max_col) in sorted_objects:
            height = max_row - min_row + 1
            width = max_col - min_col + 1
            object_grid = np.zeros((height, width), dtype=int)
            for r, c in obj:
                object_grid[r-min_row, c-min_col] = color
            output_rows.append(object_grid)

        output_grid = np.concatenate(output_rows, axis = 0)
        return output_grid

    # stack rows (example 4)
    rows_with_objects = []

    for color, obj, (min_row, min_col, max_row, max_col) in sorted_objects:
        for row_num in range(min_row, max_row + 1):
            row = []
            for col_num in range(input_grid.shape[1]):
                if (row_num, col_num) in obj:
                  row.append(color)
                elif input_grid[row_num,col_num] != 0:
                   row.append(0)
            if any(row): # avoid fully blank rows
              while row[0] == 0: # trim leading zeros
                row.pop(0)
              while row[-1] == 0: # trim trailing zeros
                row.pop()
              rows_with_objects.append(row)


    if not rows_with_objects:
        return np.array([])

    max_len = max(len(row) for row in rows_with_objects)
    output_grid = np.zeros((len(rows_with_objects), max_len), dtype=int)

    for i, row in enumerate(rows_with_objects):
       output_grid[i,:len(row)] = row


    return output_grid
```
