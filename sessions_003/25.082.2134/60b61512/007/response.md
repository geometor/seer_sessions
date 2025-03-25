```python
"""
The transformation rule identifies yellow (4) clusters (horizontal or vertical lines) and changes adjacent white (0) pixels that extend the line of the cluster to orange (7). Only the *first* white pixel adjacent to each end of the yellow line is changed.
"""

import numpy as np

def get_yellow_clusters(grid):
    """
    helper: find yellow clusters (horizontal or vertical lines)
    """
    rows, cols = grid.shape
    clusters = []
    visited = set()

    def is_valid(row, col):
        return 0 <= row < rows and 0 <= col < cols

    def dfs(row, col, current_cluster, direction):
        if (row, col) in visited or not is_valid(row, col) or grid[row, col] != 4:
            return

        visited.add((row, col))
        current_cluster.append((row, col))

        if direction == "horizontal":
            dfs(row, col + 1, current_cluster, direction)
            dfs(row, col - 1, current_cluster, direction)
        elif direction == "vertical":
            dfs(row + 1, col, current_cluster, direction)
            dfs(row - 1, col, current_cluster, direction)


    for row in range(rows):
        for col in range(cols):
            if grid[row, col] == 4 and (row, col) not in visited:
                # Try horizontal first
                horizontal_cluster = []
                dfs(row, col, horizontal_cluster, "horizontal")
                if len(horizontal_cluster) > 1:
                    clusters.append(horizontal_cluster)
                    continue #move on, already have the whole cluster

                # Try vertical
                vertical_cluster = []
                dfs(row, col, vertical_cluster, "vertical")
                if len(vertical_cluster) > 1:
                    clusters.append(vertical_cluster)

    return clusters

def get_extending_pixels(grid, cluster):
    """
    helper: find *first* white pixel that extends the line of the cluster
    """
    extending_pixels = []
    rows, cols = grid.shape

    # Determine if the cluster is horizontal or vertical
    if len(cluster) > 1:
        if cluster[0][0] == cluster[1][0]:
            direction = "horizontal"
            cluster.sort(key=lambda x: x[1])
            start = cluster[0]
            end = cluster[-1]

            # Check west
            c = start[1] - 1
            if 0 <= c and grid[start[0], c] == 0:
                extending_pixels.append((start[0], c))

            # Check east
            c = end[1] + 1
            if c < cols and grid[end[0], c] == 0:
                extending_pixels.append((end[0], c))

        else:
            direction = "vertical"
            cluster.sort(key=lambda x: x[0])
            start = cluster[0]
            end = cluster[-1]

            # Check north
            r = start[0] - 1
            if 0 <= r and grid[r, start[1]] == 0:
                extending_pixels.append((r, start[1]))
            # Check south
            r = end[0] + 1
            if r < rows and grid[r, end[1]] == 0:
                extending_pixels.append((r, end[1]))

    return extending_pixels


def transform(input_grid):
    """
    transform input grid to output grid
    """
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # get yellow clusters
    yellow_clusters = get_yellow_clusters(input_grid)

    # find extending white pixels and change them to orange
    for cluster in yellow_clusters:
        extending_pixels = get_extending_pixels(input_grid, cluster)
        for r, c in extending_pixels:
            output_grid[r, c] = 7

    return output_grid
```
