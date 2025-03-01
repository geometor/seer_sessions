"""
1.  **Identify Objects:** Locate all distinct objects within the input grid, focusing particularly on azure (8) colored objects. Other colored objects should also be noted, as they might be relevant.
2.  **Azure Focus:**  If an azure object exists, determine its bounding box.
3.  **Relational Extraction:** The output grid's dimensions and content are determined by the azure object's bounding box, *and the relationship of pixels within and potentially around the box*. It is not a simple extraction of the bounding box contents. The relationship might involve:
    *   **Complete Inclusion:** If other objects or parts of objects are *fully contained* within the azure object's bounding box, they are included in the output.
    * **Relative Offset:** If the examples show a consistent offset or shift of other colored pixels relative to the azure object's position, apply this offset to extract the relevant region from the input grid.
    * **Partial Inclusion**: Parts of other objects outside of the bounding box may be relevant.
4.  **Output Construction:** Create a new grid. Copy the pixels from input to output grid, according the relation extraction.
5. **No Azure Case:** If there is not azure object, output an empty grid.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous regions of the same color in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row,col] != 0:
                obj_pixels = []
                dfs(row, col, grid[row, col], obj_pixels)
                if obj_pixels:
                    objects.append(obj_pixels)
    return objects

def get_bounding_box(pixels):
    """Calculates the bounding box of a set of pixels."""
    min_row = min(p[0] for p in pixels)
    max_row = max(p[0] for p in pixels)
    min_col = min(p[1] for p in pixels)
    max_col = max(p[1] for p in pixels)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # Find all objects
    objects = find_objects(input_grid)

    # Find azure object
    azure_object = None
    for obj in objects:
        if input_grid[obj[0]] == 8:
            azure_object = obj
            break

    # Handle no azure case
    if azure_object is None:
        return np.zeros((0, 0), dtype=int)

    # Get bounding box for azure object
    top_left, bottom_right = get_bounding_box(azure_object)
    
    # compute height, width of azure object bounding box
    azure_height = bottom_right[0] - top_left[0] + 1
    azure_width = bottom_right[1] - top_left[1] + 1

    # Initialize output (start by assuming same size of azure bounding box)
    output_grid = np.zeros((azure_height, azure_width), dtype=int)

    # Relational Extraction (attempting complete inclusion first)
    for row in range(input_grid.shape[0]):
        for col in range(input_grid.shape[1]):
            # Check if pixel is within the bounding box *relative to the azure object's top-left*
            if top_left[0] <= row <= bottom_right[0] and top_left[1] <= col <= bottom_right[1]:
                output_row = row - top_left[0]
                output_col = col - top_left[1]
                output_grid[output_row, output_col] = input_grid[row, col]
    
    return output_grid