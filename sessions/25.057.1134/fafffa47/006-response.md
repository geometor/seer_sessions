# fafffa47 • 006 • refine_coder

---
```python
"""
1.  **Identify Key Maroon Object:** Within the input grid, identify a *specific* maroon (9) object.  The selection criteria varies:
    *   If there's only one maroon object, select it.
    *   If there are multiple maroon objects, and one is a distinct, longest horizontal line at the bottom, select it.
    *   If there's a connected maroon structure with a central vertical line, select the vertical line.
2.  **Extract Dimensions:** Determine the dimensions (height and width) of the *selected* maroon object.
3.  **Color Change:** Change the color of the selected maroon object to red (2).
4.  **Create Output:** Create an output grid with the dimensions of the selected and recolored object, filled entirely with the red (2) color.
"""

import numpy as np

def find_all_objects(grid, color):
    # Find the coordinates of all cells with the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return []  # Return empty list if color not found

    objects = []
    visited = set()

    def dfs(row, col, current_object):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row, col in coords:
        if (row, col) not in visited:
            current_object = []
            dfs(row, col, current_object)
            objects.append(current_object)
    return objects

def get_object_dimensions(obj_coords):
    if not obj_coords:
        return 0, 0
    rows, cols = zip(*obj_coords)
    height = max(rows) - min(rows) + 1
    width = max(cols) - min(cols) + 1
    return height, width

def get_longest_horizontal_line(objects):
    longest_line = []
    max_width = 0
    for obj in objects:
        rows, cols = zip(*obj)
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)
        height = max_row - min_row + 1
        width = max_col - min_col + 1
        if height == 1 and width > max_width:  # Check if it's a horizontal line
                max_width = width
                longest_line = obj
    return longest_line


def get_central_vertical_line(objects, input_grid):
   #Find central vertical line. This one is the trickiest.
    best_vertical_line = []
    max_height = 0

    for obj in objects:
        rows, cols = zip(*obj)
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)
        height = max_row - min_row + 1
        width = max_col - min_col + 1

        # prioritize height and centeredness
        if width == 1:  # Check if it's a vertical line
            obj_center_col = (min_col + max_col) / 2
            grid_center_col = input_grid.shape[1] / 2
            if height > max_height:
                max_height = height
                best_vertical_line = obj
    return best_vertical_line


def transform(input_grid):
    # Find all maroon objects.
    maroon_objects = find_all_objects(input_grid, 9)

    if not maroon_objects:  # Handle cases with no maroon objects
        return np.zeros((0, 0), dtype=int)

    # Select the key maroon object.
    if len(maroon_objects) == 1:
        key_object = maroon_objects[0]
    else:
        longest_horizontal = get_longest_horizontal_line(maroon_objects)
        if longest_horizontal:
            key_object = longest_horizontal
        else:
            central_vertical = get_central_vertical_line(maroon_objects, input_grid)
            if central_vertical:
                key_object = central_vertical
            else:
                # default to first if the others don't exist.  This might
                # happen if there are multiple small objects.
                key_object = maroon_objects[0]

    # Get dimensions of the key object.
    height, width = get_object_dimensions(key_object)

    # Create output grid and fill with red (2).
    output_grid = np.full((height, width), 2, dtype=int)

    return output_grid
```
