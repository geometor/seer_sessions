"""
1.  **Identify Objects:** Locate all contiguous regions (objects) within the input grid that are not gray (color value 5). Each object is defined by its constituent pixels having the same color.
2.  **Extract Object Data:** For each identified object, determine its bounding box (minimum and maximum row and column), width, height, the color of the pixels, and original position of the object in the input image.
3. **Order Objects**: Sort the objects based on the following criteria, in descending order of precedence:
    -   Height (largest to smallest)
    -   Width (smallest to largest)
    - For objects with identical height and width: by the original position (smallest to largest, first row and then col)
4.  **Create Output Grid:** Construct a new grid with a gray background (all pixels set to 5). The dimensions of this grid are determined by the objects:
    *   Width: The sum of the widths of all objects.
    *   Height: The maximum height of all objects.
5.  **Place Objects:** Iterate through the sorted list of objects. Place each object onto the output grid from left to right. The objects should maintain their shape by copying the pixels. The x-coordinate of the next object begins immediately after the previous object.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous non-gray (non-5) regions in the grid, preserving original position."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, current_object, color):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object, color)
        dfs(row - 1, col, current_object, color)
        dfs(row, col + 1, current_object, color)
        dfs(row, col - 1, current_object, color)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 5:
                current_object = []
                dfs(row, col, current_object, grid[row, col])
                # Store color, object pixels, and original position for tie-breaking
                objects.append((grid[row,col], current_object, row, col))
    return objects

def get_object_bounds(obj_pixels):
    """Compute bounding box of an object"""
    min_row = min(p[0] for p in obj_pixels)
    max_row = max(p[0] for p in obj_pixels)
    min_col = min(p[1] for p in obj_pixels)
    max_col = max(p[1] for p in obj_pixels)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    input_grid = np.array(input_grid)

    # 1. Identify Objects, preserving original position
    objects = find_objects(input_grid)

    # 2. Extract Object Data and Sort
    object_data = []
    for color, obj_pixels, orig_row, orig_col in objects:
        min_row, max_row, min_col, max_col = get_object_bounds(obj_pixels)
        width = max_col - min_col + 1
        height = max_row - min_row + 1
        object_data.append((color, obj_pixels, width, height, orig_row, orig_col))

    # Sort objects by height (descending), width (ascending), then original position
    object_data.sort(key=lambda x: (-x[3], x[2], x[4], x[5]))

    # 3. Determine Output Grid Size
    total_width = sum(width for _, _, width, _, _, _ in object_data)
    max_height = max(height for _, _, _, height, _, _ in object_data)

    # 4. Create Output Grid and Fill Background
    output_grid = np.full((max_height, total_width), 5, dtype=int)

    # 5. Place Objects
    current_x = 0
    for color, obj_pixels, width, _, _, _ in object_data:
        for r, c in obj_pixels:
            # Compute relative position within the object
            min_row, _, min_col, _ = get_object_bounds(obj_pixels)
            rel_r = r - min_row
            rel_c = c - min_col
            output_grid[rel_r, current_x + rel_c] = color
        current_x += width

    return output_grid.tolist()