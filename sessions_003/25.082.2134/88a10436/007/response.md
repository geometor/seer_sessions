```python
"""
1.  **Identify Objects:** Find all distinct objects in the input grid. An object is a contiguous block of non-zero pixels.
2.  **Categorize Objects:** Divide objects into two groups: "single-pixel objects" (containing only one pixel) and "multi-pixel objects" (containing more than one pixel).
3. **Conditional Transformation**
   * If no single pixel object, or if no multi-pixel objects: no change. Output is the same as the Input.
   * If both single-pixel and multi-pixel object(s) are present:
        1.  **Retain Multi-Pixel Object(s):** Copy the multi-pixel object(s) from the input to the output grid, unchanged.
        2. **Duplicate and Position:** Create a duplicate of the *first multi-pixel object* found in the input.
        3. **Anchor:** Use the location of the *first single-pixel object* found in the input as an anchor point. Position the duplicated multi-pixel object such that its bounding box is centered on the single pixel.
        4. **Remove the single pixel:** set the value of the original single pixel to 0

4.  **Output:** The final output grid consists of the original multi-pixel object(s) and the newly positioned, duplicated multi-pixel object, with the single pixel object removed.
"""

import numpy as np

def find_objects(grid):
    """
    Finds distinct objects in the grid.  An object is a group of
    contiguous non-zero pixels.
    Uses depth first search
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(row, col, current_object):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] == 0):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] != 0 and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def bounding_box(object_pixels):
    """
    Find the smallest rectangle enclosing a single object.
    """
    min_row = float('inf')
    max_row = float('-inf')
    min_col = float('inf')
    max_col = float('-inf')

    for row, col in object_pixels:
        min_row = min(min_row, row)
        max_row = max(max_row, row)
        min_col = min(min_col, col)
        max_col = max(max_col, col)

    return (min_row, max_row, min_col, max_col)

def copy_object(grid, object_pixels):
    """
    Copies an object's pixel values. Returns a dictionary mapping
    (row, col) to pixel value.
    """
    object_data = {}
    for row, col in object_pixels:
        object_data[(row, col)] = grid[row, col]
    return object_data

def transform(input_grid):
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)  # Start with a copy
    objects = find_objects(input_grid)

    single_pixel_objects = [obj for obj in objects if len(obj) == 1]
    multi_pixel_objects = [obj for obj in objects if len(obj) > 1]

    if single_pixel_objects and multi_pixel_objects:
        # Get the first single-pixel object and its position
        single_pixel_obj = single_pixel_objects[0]
        single_pixel_row, single_pixel_col = single_pixel_obj[0]

        # Get the first multi-pixel object
        multi_pixel_obj = multi_pixel_objects[0]
        multi_pixel_bbox = bounding_box(multi_pixel_obj)
        min_row, max_row, min_col, max_col = multi_pixel_bbox

        # Duplicate object data
        duplicated_object = copy_object(input_grid, multi_pixel_obj)
        
        # Remove the original single pixel
        output_grid[single_pixel_row, single_pixel_col] = 0

        # Calculate dimensions of the multi-pixel object
        height = max_row - min_row + 1
        width = max_col - min_col + 1

        # Calculate the new top-left corner for the duplicated object
        new_min_row = single_pixel_row - height // 2
        new_min_col = single_pixel_col - width // 2

        # Place the duplicated object in the output grid
        for (row, col), value in duplicated_object.items():
            new_row = row - min_row + new_min_row
            new_col = col - min_col + new_min_col
            if 0 <= new_row < output_grid.shape[0] and 0 <= new_col < output_grid.shape[1]:
                 output_grid[new_row, new_col] = value
    return output_grid.tolist()
```