"""
1.  **Identify:** Locate all clusters of red (2) pixels within the checkerboard pattern of gray(5) and white(0) pixels.
2.  **Check Adjacency:** For each red cluster, examine the immediately adjacent gray (5) pixels. *Adjacent* means horizontally or vertically touching, not diagonally.
3. **Conditional Modification:** If an adjacent pixel is a gray(5), change the color of some of these gray pixels to azure(8). I say 'some' because some of the gray pixels remain unchanged. It appears that the modification is done only if gray(5) is a part of the underlying checkerboard pattern. In other words, if gray(5) is surrounded by white(0), it may become an azure(8)
"""

import numpy as np

def find_clusters(grid, color):
    """Finds clusters of a specific color in a grid."""
    visited = np.zeros_like(grid, dtype=bool)
    clusters = []

    def dfs(row, col, current_cluster):
        """Depth-first search to explore a cluster."""
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

def get_adjacent_pixels(grid, pixel, include_diagonal=False):
   """Returns a list of adjacent pixel coordinates to the given pixel."""
   row, col = pixel
   adjacent = []
   for dr in [-1, 0, 1]:
       for dc in [-1, 0, 1]:
           if (dr == 0 and dc == 0) or (include_diagonal is False and (dr != 0 and dc != 0)):
               continue
           new_row, new_col = row + dr, col + dc
           if 0 <= new_row < grid.shape[0] and 0 <= new_col < grid.shape[1]:
               adjacent.append((new_row, new_col))
   return adjacent

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.copy(input_grid)
    red_clusters = find_clusters(output_grid, 2)

    for cluster in red_clusters:
        for red_pixel in cluster:
            adjacent_pixels = get_adjacent_pixels(output_grid, red_pixel)
            for adj_row, adj_col in adjacent_pixels:
                if output_grid[adj_row, adj_col] == 5:
                    # Check the checkerboard pattern.
                    neighbors = get_adjacent_pixels(output_grid, (adj_row, adj_col))
                    white_neighbors = 0
                    for nr, nc in neighbors:
                         if output_grid[nr, nc] == 0:
                            white_neighbors +=1
                    
                    if white_neighbors > 0:
                        output_grid[adj_row, adj_col] = 8

    return output_grid