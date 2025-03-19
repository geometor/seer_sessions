# 88a62173 • 010 • refine_coder

---
```python
"""
1.  **Identify Clusters:** Examine the input grid and identify distinct clusters of blue (1) pixels. A cluster is defined as a group of blue pixels connected orthogonally (not diagonally).

2.  **Simplify each Cluster:** For each cluster, select the blue pixels that compose the diagonal from the top-left to bottom-right of the smallest bounding box that contains the entire cluster.

3. **Arrange Output:** Create an output grid. Maintain the relative positioning of the simplified representations of each input cluster. That is, if cluster A's simplified form is to the left of cluster B's simplified form in the input, the same relative positioning should hold in the output. If a cluster simplifies to an empty set of pixels, it does not appear in the output. The overall size and spacing of output simplifies to the minimal bounding box needed.
"""

import numpy as np

def find_clusters(grid):
    # helper to find clusters of orthogonally connected blue pixels
    visited = set()
    clusters = []

    def dfs(row, col, current_cluster):
        # Depth-first search to explore a cluster
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] == 0:
            return

        visited.add((row, col))
        current_cluster.append((row, col))

        # Explore adjacent cells
        dfs(row + 1, col, current_cluster)
        dfs(row - 1, col, current_cluster)
        dfs(row, col + 1, current_cluster)
        dfs(row, col - 1, current_cluster)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == 1 and (row, col) not in visited:
                current_cluster = []
                dfs(row, col, current_cluster)
                clusters.append(current_cluster)
    return clusters

def simplify_cluster(cluster):
    # helper to select the diagonal pixels of the bounding box of a cluster
    if not cluster:
        return []

    rows, cols = zip(*cluster)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    simplified = []
    for i in range(min(max_row - min_row, max_col-min_col)+1):
        simplified.append( (min_row + i, min_col + i) )
    return simplified

def transform(input_grid):
    input_grid = np.array(input_grid)

    # 1. Identify Clusters
    clusters = find_clusters(input_grid)

    # 2. Simplify each Cluster
    simplified_clusters = [simplify_cluster(cluster) for cluster in clusters]
    
    #remove empty clusters
    simplified_clusters = [cluster for cluster in simplified_clusters if len(cluster) > 0]

    # 3. Arrange Output
    if not simplified_clusters:
        return []  # Return empty grid if no clusters

    # Find relative offsets and combined bounds
    all_simplified_pixels = []
    for cluster in simplified_clusters:
        all_simplified_pixels.extend(cluster)

    if len(all_simplified_pixels) == 0:
        return []
        
    rows, cols = zip(*all_simplified_pixels)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)


    output_grid = np.zeros((max_row - min_row + 1, max_col - min_col + 1), dtype=int)

    for cluster in simplified_clusters:
        for row, col in cluster:
            output_grid[row - min_row, col - min_col] = 1

    return output_grid.tolist()
```
