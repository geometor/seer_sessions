"""
1. Identify Colored Clusters: Find all contiguous regions (clusters) of non-background (non-zero) colored pixels in the input grid. A cluster is defined as a group of pixels of the same color that are connected by edges (not just corners).
2. Optional Grey Removal: If a grey pixel (color 5) is present, remove it (set its value to 0).
3. Select Largest Cluster: If multiple clusters are found, select the largest cluster based on the total number of pixels. If clusters have the same size, select the cluster whose top-left corner is closest to the origin (0,0).
4. Move Selected Cluster: Move the selected cluster so that its top-left corner aligns with the top-left corner (0, 0) of the output grid. Preserve the relative positions of pixels within the cluster.
5. Fill Background: All other pixels in the output grid should be the background color (0). If no clusters are found the output is all 0.
"""

import numpy as np

def find_clusters(grid):
    """Finds all contiguous clusters of non-background pixels."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    clusters = []

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_cluster):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] == 0:
            return
        visited[r, c] = True
        current_cluster.append((r, c, grid[r, c]))
        dfs(r + 1, c, current_cluster)
        dfs(r - 1, c, current_cluster)
        dfs(r, c + 1, current_cluster)
        dfs(r, c - 1, current_cluster)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                current_cluster = []
                dfs(r, c, current_cluster)
                clusters.append(current_cluster)
    return clusters

def select_largest_cluster(clusters):
    """Selects the largest cluster, with tie-breaking by top-leftmost."""
    if not clusters:
        return None

    largest_cluster = max(clusters, key=len)
    max_size = len(largest_cluster)
    
    #check for ties
    tied_clusters = [cluster for cluster in clusters if len(cluster) == max_size]
    
    if len(tied_clusters) > 1:
      # select the top-left most
      # find top-left corner of each cluster
      top_left_corners = []
      for cluster in tied_clusters:
        min_row = min(pixel[0] for pixel in cluster)
        min_col = min(pixel[1] for pixel in cluster)
        top_left_corners.append((min_row, min_col))
      
      # find the minimum top-left corner
      min_corner = min(top_left_corners)
      
      #get index of this corner
      min_index = top_left_corners.index(min_corner)
      largest_cluster = tied_clusters[min_index]
    
    return largest_cluster


def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    # Initialize output grid with the same dimensions and default color (0).
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Optional Grey Removal: remove grey pixel (5) if present
    input_grid = np.where(input_grid == 5, 0, input_grid)

    # Identify Colored Clusters
    clusters = find_clusters(input_grid)
    
    # Select Largest Cluster (or handle no clusters)
    selected_cluster = select_largest_cluster(clusters)
    
    if selected_cluster is None:
      return output_grid
    
    #find top left of selected cluster
    min_row = min(pixel[0] for pixel in selected_cluster)
    min_col = min(pixel[1] for pixel in selected_cluster)

    # Calculate the shift needed to move the cluster's top-left to (0, 0).
    row_shift = -min_row
    col_shift = -min_col

    # Move the selected cluster to (0, 0) in output grid.
    for r, c, color in selected_cluster:
        new_r = r + row_shift
        new_c = c + col_shift
        if 0 <= new_r < rows and 0 <= new_c < cols:  # Boundary check
            output_grid[new_r, new_c] = color

    return output_grid