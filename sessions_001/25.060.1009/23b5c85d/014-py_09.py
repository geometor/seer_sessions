"""
1.  **Identify Objects:** Scan the input grid to identify all distinct rectangular objects. A rectangular object is a contiguous block of pixels with the same color. Record the color, dimensions (height and width), and position of each object.
2.  **Find the Largest Object:** Determine the *largest* object among all identified objects. The size of an object is determined by the product of its height and width (number of pixels).
3.  **Determine Output Dimensions:** The dimensions of the output grid will be the same as the dimensions of the largest object found.
4.  **Create Output:** Create an output grid with the dimensions of the largest object. Fill the output grid with the *same color* as the largest object.
"""

import numpy as np

def find_objects(grid):
    """Finds rectangular objects in a grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c, color):
        return 0 <= r < rows and 0 <= c < cols and grid[r, c] == color and (r, c) not in visited

    def dfs(r, c, color, object_coords):
        visited.add((r, c))
        object_coords.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc, color):
                dfs(nr, nc, color, object_coords)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r,c] != 0:
                color = grid[r, c]
                object_coords = []
                dfs(r, c, color, object_coords)
                if object_coords:
                    min_r = min(coord[0] for coord in object_coords)
                    max_r = max(coord[0] for coord in object_coords)
                    min_c = min(coord[1] for coord in object_coords)
                    max_c = max(coord[1] for coord in object_coords)
                    objects.append({
                        "color": color,
                        "position": (min_r, min_c),
                        "dimensions": (max_r - min_r + 1, max_c - min_c + 1)
                    })
    return objects

def transform(input_grid):
    # Find all objects in the input grid
    objects = find_objects(input_grid)

    # If no objects are found, return an empty array
    if not objects:
        return np.array([])

    # Find the largest object
    largest_object = max(objects, key=lambda obj: obj['dimensions'][0] * obj['dimensions'][1])

    # Create the output grid with the dimensions of the largest object
    height, width = largest_object['dimensions']
    output_grid = np.full((height, width), largest_object['color'], dtype=int)

    return output_grid