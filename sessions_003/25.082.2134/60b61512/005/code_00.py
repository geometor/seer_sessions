"""
The transformation rule identifies yellow (4) clusters (horizontal or vertical lines) and changes adjacent white (0) pixels that extend the line of the cluster to orange (7).
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
    helper: find white pixels that extend the line of the cluster
    """
    extending_pixels = []
    rows, cols = grid.shape

    # Determine if the cluster is horizontal or vertical
    if len(cluster) > 1:  # Ensure cluster has at least 2 points
      if cluster[0][0] == cluster[1][0]:  # Same row, different col = horizontal
            direction = "horizontal"
            #sort by col
            cluster.sort(key=lambda x:x[1])
            start = cluster[0]
            end = cluster[-1]

            #check to the west
            west_neighbor = (start[0], start[1] - 1)
            if 0 <= west_neighbor[1] and grid[west_neighbor] == 0:
                extending_pixels.append(west_neighbor)

            #check to the east
            east_neighbor = (end[0], end[1] + 1)
            if east_neighbor[1] < cols and grid[east_neighbor] == 0 :
                extending_pixels.append(east_neighbor)
            
      else:
            direction = "vertical"
             #sort by row
            cluster.sort(key=lambda x:x[0])
            start = cluster[0]
            end = cluster[-1]

            # Check above
            north_neighbor = (start[0] - 1, start[1])
            if 0 <= north_neighbor[0] and grid[north_neighbor] == 0:
                extending_pixels.append(north_neighbor)

            # Check below
            south_neighbor = (end[0] + 1, end[1])
            if south_neighbor[0] < rows and grid[south_neighbor] == 0:
                extending_pixels.append(south_neighbor)
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