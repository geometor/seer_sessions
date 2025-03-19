"""
1. **Identify Red Clusters:** Find all connected groups of red pixels (value 2) in the input grid. Consider pixels connected if they are adjacent horizontally, vertically, or diagonally (8-connectivity).

2. **Calculate Centroids:** For each red cluster, calculate its centroid. The centroid is the average row and average column of all pixels within the cluster.

3. **Scale and Map:**  Scale down the input grid dimensions to a 3x3 grid.  Calculate scaling factors: `scale_row = input_rows / 3` and `scale_col = input_cols / 3`. Map each centroid to the output grid by dividing its row and column coordinates by the respective scaling factors. Round the result down to the nearest integer to get the row and column indices in the 3x3 output grid.

4. **Handle Collisions**: If two or more cluster centroids map to the same cell in the output, prioritize the cluster with more pixels.

5. **Create Output:** Create a 3x3 output grid, initially filled with zeros (white/0).  Set the pixels corresponding to the mapped and adjusted centroid positions to red (2).
"""

import numpy as np

def find_connected_components(input_grid):
    """
    Finds connected components of red pixels (value 2) in the input grid.
    Uses 8-connectivity (includes diagonals).
    """
    visited = set()
    components = []

    def dfs(row, col, current_component):
        if (
            row < 0
            or row >= input_grid.shape[0]
            or col < 0
            or col >= input_grid.shape[1]
            or (row, col) in visited
            or input_grid[row, col] != 2
        ):
            return

        visited.add((row, col))
        current_component.append((row, col))

        # Explore all 8 neighbors (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(row + dr, col + dc, current_component)

    for row in range(input_grid.shape[0]):
        for col in range(input_grid.shape[1]):
            if input_grid[row, col] == 2 and (row, col) not in visited:
                current_component = []
                dfs(row, col, current_component)
                components.append(current_component)
    return components

def calculate_centroid(coordinates):
    """Calculates the centroid of a list of (row, col) coordinates."""
    if not coordinates:
        return None
    return (
        sum([c[0] for c in coordinates]) / len(coordinates),
        sum([c[1] for c in coordinates]) / len(coordinates),
    )

def transform(input_grid):
    # 1. Identify Red Clusters
    red_clusters = find_connected_components(input_grid)

    # 2. Calculate Centroids
    centroids = [calculate_centroid(cluster) for cluster in red_clusters]

    # 3. Scale and Map & 4. Handle Collisions (combined)
    output_grid = np.zeros((3, 3), dtype=int)
    scale_row = input_grid.shape[0] / 3
    scale_col = input_grid.shape[1] / 3

    # Keep track of which output cells are occupied and the size of the cluster that occupies it.
    occupied = {}  # (row, col): size_of_cluster

    for i, centroid in enumerate(centroids):
      if centroid: #handle empty cluster
        output_row = int(centroid[0] / scale_row)
        if output_row > 2: output_row = 2
        output_col = int(centroid[1] / scale_col)
        if output_col > 2: output_col = 2

        cluster_size = len(red_clusters[i])

        if (output_row, output_col) not in occupied:
            occupied[(output_row, output_col)] = cluster_size
            output_grid[output_row, output_col] = 2
        elif occupied[(output_row, output_col)] < cluster_size:
              # Replace if current cluster size is greater.
            occupied[(output_row, output_col)] = cluster_size
            output_grid[output_row, output_col] = 2 #need to iterate and clear previous

    # 5. Create Output (already done within the mapping loop)
    return output_grid