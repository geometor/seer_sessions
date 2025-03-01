"""
1. Identify Red Clusters: Locate all contiguous clusters of red (2) pixels within the input grid.
2. Focus on Top-Left Cluster: Select the red cluster located in the top-left region of the input grid.
3. Determine Bounding Box: Find minimal bounding box of shape that encloses the cluster.
4. Extract Subgrid: Extract the subgrid defined by the top-left red cluster's bounding box. This bounding box defines the output region from the input matrix. The top left starts from the first row, column.
5. Output: The extracted subgrid is the output.
"""

import numpy as np

def find_clusters(grid, color):
    visited = np.zeros_like(grid, dtype=bool)
    clusters = []

    def dfs(row, col, current_cluster):
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
        current_cluster.append((row, col))
        dfs(row + 1, col, current_cluster)
        dfs(row - 1, col, current_cluster)
        dfs(row, col + 1, current_cluster)
        dfs(row, col - 1, current_cluster)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_cluster = []
                dfs(row, col, current_cluster)
                clusters.append(current_cluster)
    return clusters

def get_bounding_box(cluster):
    min_row = min(cell[0] for cell in cluster)
    max_row = max(cell[0] for cell in cluster)
    min_col = min(cell[1] for cell in cluster)
    max_col = max(cell[1] for cell in cluster)
    return min_row, min_col, max_row, max_col



def transform(input_grid):
    # 1. Identify Red Clusters
    red_clusters = find_clusters(input_grid, 2)

    # 2. Focus on Top-Left Cluster
    if not red_clusters:
        return np.zeros((0, 0), dtype=int)  # Return empty grid if no red clusters

    top_left_cluster = min(red_clusters, key=lambda cluster: (cluster[0][0], cluster[0][1])) #find top left

    # 3. Determine Bounding Box
    min_row, min_col, max_row, max_col = get_bounding_box(top_left_cluster)

    # 4. Extract Subgrid
    output_grid = input_grid[min_row : max_row + 1, min_col : max_col + 1]

    # 5. Output
    return output_grid