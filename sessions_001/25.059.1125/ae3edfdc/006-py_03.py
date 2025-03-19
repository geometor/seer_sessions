"""
Moves clusters of colored pixels. A green(3) cluster is moved down and left, and a new green cell is placed to its right, adjacent to red(2) pixels within the cluster.
A cross-shaped cluster of orange(7) and blue(1) pixels is moved up by one, preserving the cross shape.
A T-shaped cluster of orange(7) and blue(1) is not moved.
Other clusters remain in their original position.
"""

import numpy as np

def find_clusters(grid):
    """Finds clusters of connected non-zero pixels."""
    clusters = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, cluster):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] == 0:
            return
        visited.add((r, c))
        cluster.append((r, c, grid[r, c]))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, cluster)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                cluster = []
                dfs(r, c, cluster)
                clusters.append(cluster)
    return clusters

def move_cluster(cluster, dr, dc):
    """Moves a cluster by (dr, dc)."""
    moved_cluster = []
    for r, c, val in cluster:
        moved_cluster.append((r + dr, c + dc, val))
    return moved_cluster

def is_cross_shape(cluster):
    """Checks if a cluster is cross-shaped (orange/blue/orange)."""
    if len(cluster) != 5:
        return False
    
    blue_count = sum(1 for _, _, val in cluster if val == 1)
    if blue_count != 1:
        return False

    orange_count = sum(1 for _, _, val in cluster if val == 7)
    if orange_count != 4:
        return False

    # Find the blue cell
    blue_r, blue_c = None, None
    for r, c, val in cluster:
        if val == 1:
            blue_r, blue_c = r, c
            break
    
    # Check for orange cells around the blue
    neighbors = [(blue_r - 1, blue_c), (blue_r + 1, blue_c), (blue_r, blue_c - 1), (blue_r, blue_c + 1)]
    orange_neighbors = 0
    for r, c, val in cluster:
      if (r,c) in neighbors:
        orange_neighbors +=1

    return orange_neighbors == 4
    

def is_t_shape(cluster):
    """Checks if a cluster is T-shaped (orange/blue/orange)."""
    if len(cluster) != 5:
        return False

    blue_count = sum(1 for _, _, val in cluster if val == 1)
    if blue_count != 1:
        return False
    
    orange_count = sum(1 for _, _, val in cluster if val == 7)
    if orange_count != 4:
        return False
    
    # Find the blue cell
    blue_r, blue_c = None, None
    for r, c, val in cluster:
        if val == 1:
            blue_r, blue_c = r, c
            break

    # Check for T-shape
    neighbors = [(blue_r - 1, blue_c), (blue_r + 1, blue_c), (blue_r, blue_c - 1), (blue_r, blue_c + 1)]
    orange_neighbors_count = 0
    for nr, nc in neighbors:
        for cr, cc, cv in cluster:
            if (nr, nc) == (cr, cc) and cv == 7:
                orange_neighbors_count += 1

    if orange_neighbors_count != 3:
        return False  # Not exactly 3 orange neighbors

    # Ensure it's a T, and not a cross
    horizontal = 0
    vertical = 0
    for nr, nc in neighbors:
      for cr, cc, cv in cluster:
        if (nr, nc) == (cr, cc) and cv == 7:
          if nr == blue_r:
            horizontal += 1
          if nc == blue_c:
            vertical += 1
    return horizontal >= 1 and vertical >=1 and (horizontal == 3 or vertical==3)

def transform(input_grid):
    # Initialize output grid
    output_grid = np.zeros_like(input_grid)
    
    clusters = find_clusters(input_grid)

    for cluster in clusters:
        first_cell_color = cluster[0][2]

        if first_cell_color == 3:
            # Move the green cluster down and left.
            moved_cluster = move_cluster(cluster, 1, -1)
            red_cells = []
            for r, c, val in cluster:
                if val == 2:
                    red_cells.append((r, c))
            for r, c, val in moved_cluster:
                if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                    output_grid[r,c] = val


            # Place an additional 3 to the right of the red cells in original cluster
            for r, c in red_cells:
                new_r, new_c = r+1, c+1  # offset by move of cluster
                if 0 <= new_r < output_grid.shape[0] and 0 <= new_c < output_grid.shape[1]:
                    output_grid[new_r, new_c] = 3

        elif is_cross_shape(cluster):
            # Move cross-shaped cluster up.
            moved_cluster = move_cluster(cluster, -1, 0)
            for r, c, val in moved_cluster:
                if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                    output_grid[r, c] = val

        elif is_t_shape(cluster):
          # do not move t-shapes
          for r, c, val in cluster:
            if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
              output_grid[r,c] = val
            
        else:
            # Copy any others
            for r, c, val in cluster:
                if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                    output_grid[r,c] = val

    return output_grid