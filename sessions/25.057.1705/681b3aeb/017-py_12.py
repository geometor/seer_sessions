"""
1.  **Identify Objects and Key Features**: Find all distinct objects in the input. For each object, determine key feature pixels. At minimum, find the bounding box (min/max row and column). Also find a "center" pixel. (For lines, this can be a midpoint. For more complex shapes, consider a centroid.)

2.  **Establish Output Grid**: The output grid is always 3x3.

3.  **Map and Place**: Map the key pixels of the input objects onto the output grid.
    * The relative positioning of objects in the output grid should, to the extent possible, preserve the relative positions of the *key feature pixels* in the input.
        * Example: If object A's center is above and to the left of object B's center in the input, this relationship should be maintained in the output.
    * If any object has a dimension (height or width) of more than 1 pixel along a row or column, use more than one feature to determine orientation and placement.

4.  **Handle Conflicts**: If multiple objects' key pixels map to the same output cell, use the object order (first detected object takes priority) or a predefined priority rule.

5. **Fill Empty**: Fill any remaining cells in the output with 0 (white).
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous regions of non-zero pixels."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                obj_pixels = []
                dfs(row, col, grid[row, col], obj_pixels)
                objects.append(
                    {"color": grid[row, col], "pixels": obj_pixels}
                )
    return objects

def get_bounding_box(pixels):
    """Calculates the bounding box of a set of pixels."""
    rows, cols = zip(*pixels)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return min_row, max_row, min_col, max_col

def get_center(pixels):
    """Calculates the center (midpoint) of a set of pixels."""
    min_row, max_row, min_col, max_col = get_bounding_box(pixels)
    center_row = (min_row + max_row) // 2
    center_col = (min_col + max_col) // 2
    return center_row, center_col

def transform(input_grid):
    # 1. Identify Objects and Key Features
    objects = find_objects(input_grid)
    object_features = []
    for obj in objects:
        pixels = obj['pixels']
        color = obj['color']
        min_row, max_row, min_col, max_col = get_bounding_box(pixels)
        center_row, center_col = get_center(pixels)
        object_features.append({
            'color': color,
            'min_row': min_row,
            'max_row': max_row,
            'min_col': min_col,
            'max_col': max_col,
            'center_row': center_row,
            'center_col': center_col
        })

    # 2. Establish Output Grid
    output_grid = np.zeros((3, 3), dtype=int)

    # 3. Map and Place
    for obj_feat in object_features:
        color = obj_feat['color']
        # Normalize coordinates to 0-2 range
        norm_row = int(np.clip(2 * (obj_feat['center_row'] - obj_feat['min_row']) / (obj_feat['max_row'] - obj_feat['min_row'] + 1e-9), 0, 2))  if obj_feat['max_row'] != obj_feat['min_row'] else 1
        norm_col = int(np.clip(2 * (obj_feat['center_col'] - obj_feat['min_col']) / (obj_feat['max_col'] - obj_feat['min_col'] + 1e-9), 0, 2)) if obj_feat['max_col'] != obj_feat['min_col'] else 1

        # additional feature mapping
        if (obj_feat['max_row'] - obj_feat['min_row']) > 0:  # Vertical orientation
           output_grid[0:2, norm_col] = color
        elif (obj_feat['max_col'] - obj_feat['min_col']) > 0: # horizontal
           output_grid[norm_row, 0:2] = color
        else:
           output_grid[norm_row, norm_col] = color


    # 4. Handle Conflicts (Implicit in this case - later objects overwrite)

    # 5. Fill Empty (Already done by initializing with zeros)

    return output_grid