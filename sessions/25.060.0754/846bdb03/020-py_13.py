"""
1. **Identify Objects:** Find all distinct objects in the input grid. An object is a contiguous block of non-white pixels.
2. **Copy Objects:**  Create copies of each object in the input.
3. **Assemble Output:**  Create an output grid by arranging the copied objects. The objects are arranged by their appearance from left to right and top to bottom. The top-left corner of each object's bounding box in the input determines its position, row by row, in the output.
"""

import numpy as np

def find_clusters(grid):
    """Finds clusters of non-zero pixels in a grid."""
    visited = set()
    clusters = []

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, current_cluster):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] == 0:
            return
        visited.add((r, c))
        current_cluster.append((r, c))
        neighbors = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        for nr, nc in neighbors:
            dfs(nr, nc, current_cluster)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_cluster = []
                dfs(r, c, current_cluster)
                clusters.append(current_cluster)
    return clusters

def bounding_box(cluster):
    """Calculates the bounding box of a cluster."""
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')
    for r, c in cluster:
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)
    return min_r, min_c, max_r, max_c

def extract_object(grid, cluster):
    """Extracts the object from the grid based on the cluster."""
    min_r, min_c, max_r, max_c = bounding_box(cluster)
    object_grid = grid[min_r:max_r+1, min_c:max_c+1]
    return object_grid, min_r, min_c

def transform(input_grid):
    # Convert input grid to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify Objects (Clusters)
    clusters = find_clusters(input_grid)

    # Sort clusters by top-left corner (min_r, then min_c)
    clusters.sort(key=lambda cluster: (bounding_box(cluster)[0], bounding_box(cluster)[1]))

    # 2. Copy Objects and 3. Assemble Output
    output_objects = []
    for cluster in clusters:
        object_grid, _, _ = extract_object(input_grid, cluster)
        output_objects.append(object_grid)

    # Calculate output grid dimensions
    total_width = 0
    max_height = 0
    for obj in output_objects:
        if obj.shape[1] > 0:  #avoid zero width objects
            total_width += obj.shape[1]
        max_height = max(max_height, obj.shape[0])

    output_grid = np.zeros((max_height, total_width), dtype=int)

    current_x = 0
    for obj in output_objects:
       if obj.shape[1] > 0: #avoid zero width objects
          output_grid[0:obj.shape[0], current_x:current_x + obj.shape[1]] = obj
          current_x += obj.shape[1]

    return output_grid.tolist()