"""
The transformation rule is as follows:
1. Identify the azure (8) and green (3) pixel clusters.
2. Calculate the vertical center of the green cluster.
3. Reflect the azure cluster vertically across the green cluster's vertical center.
4. Expand the azure cluster vertically.
5. Keep the green cluster in its original position.
"""

import numpy as np

def find_clusters(grid, color):
    clusters = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_cluster):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_cluster.append((r, c))

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, current_cluster)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                current_cluster = []
                dfs(r, c, current_cluster)
                clusters.append(current_cluster)
    return clusters

def get_cluster_center(cluster):
    row_sum = sum(r for r, _ in cluster)
    col_sum = sum(c for _, c in cluster)
    center_row = row_sum / len(cluster)
    center_col = col_sum / len(cluster)
    return center_row, center_col

def reflect_cluster(cluster, axis_row):
    reflected_cluster = []
    for r, c in cluster:
        dist = r - axis_row
        new_r = axis_row - dist
        reflected_cluster.append((int(new_r), c))
    return reflected_cluster

def transform(input_grid):
    # Initialize output grid
    output_grid = np.zeros_like(input_grid)

    # Find azure and green clusters
    azure_clusters = find_clusters(input_grid, 8)
    green_clusters = find_clusters(input_grid, 3)

    # Process each azure cluster (though there should only be one)
    for azure_cluster in azure_clusters:
      if len(green_clusters) > 0:
        # Calculate the vertical center of the green cluster (assume only one green)
        green_center_row, _ = get_cluster_center(green_clusters[0])

        # Reflect the azure cluster
        reflected_azure = reflect_cluster(azure_cluster, green_center_row)

        # original azure
        for r, c in azure_cluster:
          output_grid[r,c] = 8

        # Reflected parts
        for r, c in reflected_azure:
          if 0 <= r < output_grid.shape[0]:
            output_grid[r, c] = 8

        #expand top
        azure_center_row, _ = get_cluster_center(azure_cluster)
        dist_to_top = azure_center_row
        top_expand = []
        for r, c in azure_cluster:
          new_r = r - (2*int(dist_to_top))
          if 0 <= new_r < output_grid.shape[0]:
            top_expand.append( (new_r, c))
            output_grid[new_r, c] = 8

        # expand reflected
        reflected_center_row, _ = get_cluster_center(reflected_azure)
        dist_to_bottom = (output_grid.shape[0] -1) - reflected_center_row
        bottom_expand = []
        for r, c in reflected_azure:
          new_r = r + (2*int(dist_to_bottom))
          if 0 <= new_r < output_grid.shape[0]:
            bottom_expand.append((new_r, c))
            output_grid[new_r,c] = 8
      

    # Copy green cluster to output grid
    for green_cluster in green_clusters:
      for r, c in green_cluster:
        output_grid[r, c] = 3

    return output_grid