"""
1.  **Identify Objects:** Scan the input grid and identify contiguous blocks of non-zero pixels. Consider each block as a separate object. Record the color and bounding box of each object.
2.  **Sort Objects:** Sort identified objects by their *column position*. Specifically, sort in descending order based on the rightmost column of each object's bounding box. If multiple objects share same column, sort them in decending order by the bottom most row of their bounding box.
3. **Fill output:**
    - Create a 3x3 output grid initialized with zeros.
    - For each object (in sorted order from Step 2) find the object's color, and fill the output grid with the object's color. Start at the top, left cell of output grid (0,0) and fill to the right.
    - After the first color, all additional colors are appended to the grid from left to right, top to bottom, and will overwrite previous cells.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_coords):
        """Depth-first search to find contiguous pixels."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1]
                or visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_coords.append((row, col))
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r, c] != 0:
                obj_coords = []
                dfs(r, c, grid[r, c], obj_coords)
                # Calculate bounding box
                min_row = min(obj_coords, key=lambda item: item[0])[0]
                max_row = max(obj_coords, key=lambda item: item[0])[0]
                min_col = min(obj_coords, key=lambda item: item[1])[1]
                max_col = max(obj_coords, key=lambda item: item[1])[1]

                objects.append({
                    'color': grid[r, c],
                    'bounding_box': [[min_row, min_col], [max_row, max_col]]
                })
    return objects

def sort_objects(objects):
    """Sorts objects by rightmost column, then bottom-most row."""
    return sorted(objects, key=lambda obj: (obj['bounding_box'][1][1], obj['bounding_box'][1][0]), reverse=True)

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""

    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Sort the objects
    sorted_objects = sort_objects(objects)

    # Initialize a 3x3 output grid
    output_grid = np.zeros((3, 3), dtype=int)

     # Fill the output grid
    count = 0
    for obj in sorted_objects:
        for r in range(3):
            for c in range(3):
                if count < 9:
                    output_grid[r,c] = obj['color']
                    count+=1


    return output_grid