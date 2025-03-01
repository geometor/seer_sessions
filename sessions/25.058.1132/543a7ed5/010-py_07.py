"""
1.  **Identify Magenta Shapes:** Locate all contiguous blocks of magenta (6) pixels. These are the initial shapes.
2.  **Replace and Outline:** For each magenta shape, replace *all* the magenta pixels with green (3). Then replace all the azure pixels(8) that are directly adjacent (up, down, left, or right, *not* diagonally) to the original magenta with green(3).
3.  **Find Topmost Shape:** Among all identified and filled shapes, determine the "topmost" shape. The topmost shape is the one whose bounding box's top edge (minimum row index) is closest to the top of the grid.
4.  **Center Calculation:** Calculate the center of the topmost shape's *bounding box*. The bounding box is defined by the minimum and maximum row and column indices of the original magenta shape. The center is calculated as `(min_row + max_row) // 2` and `(min_col + max_col) // 2`.
5.  **Insert Yellow Square:**  Place a 2x2 yellow (4) square within the topmost shape, centered on the calculated center coordinates of the bounding box. The top-left corner of the yellow square will be at the calculated center coordinates.
"""

import numpy as np

def find_objects(grid, color):
    # Find contiguous blocks of the specified color.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
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
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def replace_and_outline(grid, object_coords, fill_color, outline_color):
    # Create a copy of the grid
    modified_grid = np.copy(grid)

    # Store original magenta pixel locations for outlining
    original_magenta_pixels = set(object_coords)

    # Replace magenta with green
    for row, col in object_coords:
        modified_grid[row, col] = fill_color

    # Outline: Check neighbors of original magenta pixels
    for row, col in original_magenta_pixels:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if (0 <= nr < modified_grid.shape[0] and 0 <= nc < modified_grid.shape[1] and
                modified_grid[nr, nc] == 8):  # Check for azure
                modified_grid[nr, nc] = outline_color

    return modified_grid

def get_topmost_object(objects):
    # Return the object with the smallest minimum row.
    if not objects:
        return None
    return min(objects, key=lambda obj: min(r for r, c in obj))

def get_bounding_box_center(object_coords):
    # compute the center of the object bounding box
    min_row = min(r for r, c in object_coords)
    max_row = max(r for r, c in object_coords)
    min_col = min(c for r, c in object_coords)
    max_col = max(c for r, c in object_coords)
    center_row = (min_row + max_row) // 2
    center_col = (min_col + max_col) // 2

    return center_row, center_col

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find magenta objects.
    magenta_objects = find_objects(output_grid, 6)

    # Replace and outline each magenta object with green.
    for obj in magenta_objects:
        output_grid = replace_and_outline(output_grid, obj, 3, 3)

    # Find the topmost object based on original magenta coordinates.
    topmost_object = get_topmost_object(magenta_objects)

    # Insert yellow square in the topmost object
    if topmost_object:
        center_row, center_col = get_bounding_box_center(topmost_object)
        # Place 2x2 yellow square
        output_grid[center_row, center_col] = 4
        output_grid[center_row + 1, center_col] = 4
        output_grid[center_row, center_col + 1] = 4
        output_grid[center_row + 1, center_col + 1] = 4

    return output_grid