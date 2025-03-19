"""
Identify a specific red cluster in the input grid, define a bounding box around it,
and extract the subgrid corresponding to the bounding box, enlarging it by one in all directions.
"""

import numpy as np

def find_object(grid, color):
    """
    Finds all objects of a given color in the grid.
    Returns a list of bounding box coordinates (top_left_row, top_left_col, bottom_right_row, bottom_right_col) for each object.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
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
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                if current_object:
                    rows, cols = zip(*current_object)
                    top_left_row = min(rows)
                    top_left_col = min(cols)
                    bottom_right_row = max(rows)
                    bottom_right_col = max(cols)
                    objects.append(
                        (top_left_row, top_left_col, bottom_right_row, bottom_right_col)
                    )
    return objects

def get_bounding_box(coordinates):
    """
    Get the bounding box from a list of coordinates.
    """
    rows, cols = zip(*coordinates)
    return min(rows), min(cols), max(rows), max(cols)
    

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    input_grid = np.array(input_grid)

    # 1. Identify Red Clusters
    red_clusters = find_object(input_grid, 2)

    # 2. Select Target Cluster (the one starting at [2,2])
    target_cluster = None
    for cluster_box in red_clusters:
      if input_grid[cluster_box[0],cluster_box[1]] == 2 and cluster_box[0] == 2 and cluster_box[1] == 2:
          target_cluster = cluster_box
          break
          
    if target_cluster is None:
      # find the first object
      target_cluster = red_clusters[0]

    # 3. Define Bounding Box
    top_left_row, top_left_col, bottom_right_row, bottom_right_col = target_cluster
    
    # 4. Extract with Enlarging
    top_left_row = max(0, top_left_row - 1)
    top_left_col = max(0, top_left_col - 1)
    bottom_right_row = min(input_grid.shape[0] -1, bottom_right_row + 1)
    bottom_right_col = min(input_grid.shape[1] -1, bottom_right_col + 1)

    # Extract the subgrid
    output_grid = input_grid[
        top_left_row : bottom_right_row + 1, top_left_col : bottom_right_col + 1
    ].copy()

    return output_grid.tolist()