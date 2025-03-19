"""
1.  **Identify Red Clusters:** Find all connected groups of red pixels (color 2) in the input grid. Two red pixels are considered connected if they are adjacent horizontally, vertically, or diagonally (8-connectivity).

2.  **Calculate Centroids:** For each identified red cluster, determine its centroid. The centroid is the average of the row coordinates and the average of the column coordinates of all pixels within that cluster.

3.  **Scale and Map:** Scale the input grid down to a 3x3 output grid. Calculate the scaling factors: `scale_row = input_rows / 3` and `scale_col = input_cols / 3`. Map each cluster's centroid to a cell in the output grid by dividing its row and column by the corresponding scaling factors. Round down the result (floor division) to get the row and column indices for the 3x3 output.

4.  **Collision Handling:** If multiple centroids map to the same cell in the 3x3 output grid, prioritize the centroid of the largest cluster (the cluster with the most pixels). Overwrite any previous value.

5. **Rotate if Necessary:** If there are exactly two red clusters, rotate the output grid 90 degrees Counter Clockwise.

6.  **Create Output:** Create a 3x3 output grid filled with white (color 0) by default. For each mapped centroid, change the corresponding cell in the output grid to red (color 2), applying collision and rotation rules as necessary.
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

def rotate_ccw(grid):
    """Rotates a grid 90 degrees counter-clockwise."""
    return np.rot90(grid)

def transform(input_grid):
    # 1. Identify Red Clusters
    red_clusters = find_connected_components(input_grid)

    # 2. Calculate Centroids
    centroids = [calculate_centroid(cluster) for cluster in red_clusters]

    # 3. Scale and Map & 4. Handle Collisions (combined)
    output_grid = np.zeros((3, 3), dtype=int)
    scale_row = input_grid.shape[0] / 3
    scale_col = input_grid.shape[1] / 3

    # Keep track of which output cells are occupied and the size of the cluster
    # that occupies it.
    occupied = {}  # (row, col): size_of_cluster

    for i, centroid in enumerate(centroids):
        if centroid:  # Handle empty cluster
            output_row = int(centroid[0] / scale_row)
            if output_row > 2:
                output_row = 2
            output_col = int(centroid[1] / scale_col)
            if output_col > 2:
                output_col = 2

            cluster_size = len(red_clusters[i])

            if (output_row, output_col) not in occupied:
                occupied[(output_row, output_col)] = cluster_size
                output_grid[output_row, output_col] = 2
            elif occupied[(output_row, output_col)] < cluster_size:
                # Clear all for remapping
                for k, v in occupied.items():
                    output_grid[k[0], k[1]] = 0
                # Replace if current cluster size is greater.
                occupied[(output_row, output_col)] = cluster_size
                output_grid[output_row, output_col] = 2  # Iterate and clear

    # 5. Rotate if necessary
    if len(red_clusters) == 2:
        output_grid = rotate_ccw(output_grid)

    # 6. Create Output (already done within mapping and rotation)
    return output_grid