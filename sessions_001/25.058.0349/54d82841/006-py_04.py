"""
1.  **Identify Magenta Clusters:** Find all contiguous clusters of magenta (color 6) pixels in the input grid.
2.  **Filter Clusters:** Select only the magenta clusters that have at least one pixel in the first or second row (index 0 or 1) of the input grid.
3.  **Place Yellow Pixels:** For *every* magenta pixel within the *filtered* clusters, place a yellow pixel (color 4) in the last row of the output grid.  The column index of each yellow pixel should match the column index of its corresponding magenta pixel.
"""

import numpy as np

def find_clusters(grid, color):
    """Finds contiguous clusters of a given color in a grid."""
    clusters = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, current_cluster):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        current_cluster.append((r, c))
        dfs(r + 1, c, current_cluster)
        dfs(r - 1, c, current_cluster)
        dfs(r, c + 1, current_cluster)
        dfs(r, c - 1, current_cluster)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                current_cluster = []
                dfs(r, c, current_cluster)
                clusters.append(current_cluster)
    return clusters

def filter_clusters_by_row(clusters, rows_to_check):
    """Filters clusters based on whether they have pixels in specified rows."""
    filtered_clusters = []
    for cluster in clusters:
        for pixel in cluster:
            if pixel[0] in rows_to_check:
                filtered_clusters.append(cluster)
                break  # Move to the next cluster once a pixel is found
    return filtered_clusters

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Identify Magenta Clusters
    magenta_clusters = find_clusters(output_grid, 6)

    # Filter Clusters by rows 0 and 1
    filtered_clusters = filter_clusters_by_row(magenta_clusters, [0, 1])

    # Place Yellow Pixels based on filtered magenta pixels
    for cluster in filtered_clusters:
        for r, c in cluster:
            output_grid[rows - 1, c] = 4

    return output_grid