"""
Identify clusters of non-blue, non-white pixels within blue regions.
Duplicate some colored pixels horizontally based on their color.
"""

import numpy as np

def find_clusters(grid):
    # Find clusters of non-blue, non-white pixels
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    clusters = []

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, cluster):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        cluster.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, cluster)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] not in [0, 1]:
                color = grid[r, c]
                cluster = []
                dfs(r, c, color, cluster)
                clusters.append((color, cluster))
    return clusters

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    clusters = find_clusters(input_grid)
    # Apply duplication based on the rules
    for color, cluster in clusters:

        if color in [2,4,8,9]:  #red, yellow, azure, maroon
            for r, c in cluster:
                output_grid[r,c] = input_grid[r,c]

            for r, c in cluster:
               output_grid[r,c+1] =  input_grid[r,c] # duplicate to right by 1

            if color == 9: #maroon extends 2 more pixels
                for r,c in cluster:
                    output_grid[r,c+2] = input_grid[r,c]
                    output_grid[r,c+3] = input_grid[r,c]
            if color == 8:
                for r, c in cluster:
                    output_grid[r,c+2] = input_grid[r,c] # 9 expands by 2
                    output_grid[r,c+3] = input_grid[r,c]
    return output_grid