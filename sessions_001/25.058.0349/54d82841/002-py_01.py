"""
1.  **Identify Magenta Clusters:** Locate the magenta (6) pixel clusters in the input grid.
2.  **Find Rightmost Magenta Pixels:** In the clusters that exist on rows 1 and two (index 0 and 1), locate the rightmost magenta pixel in each cluster.
3. **Add the new pixels:** In the bottom row, place a yellow (4) pixel directly beneath each of those rightmost magenta pixels from the clusters on rows one and two..
"""

import numpy as np

def find_clusters(grid, color):
    clusters = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, current_cluster):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        current_cluster.append((r, c))
        dfs(r + 1, c, current_cluster)
        dfs(r - 1, c, current_cluster)
        dfs(r, c + 1, current_cluster)
        dfs(r, c - 1, current_cluster)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                current_cluster = []
                dfs(r, c, current_cluster)
                clusters.append(current_cluster)
    return clusters

def find_rightmost_pixel(cluster):
    rightmost_pixel = cluster[0]
    for pixel in cluster:
      if pixel[1] > rightmost_pixel[1]:
        rightmost_pixel = pixel
    return rightmost_pixel

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Identify Magenta Clusters
    magenta_clusters = find_clusters(output_grid, 6)

    # Find Rightmost Magenta Pixels in the first two rows
    rightmost_pixels = []
    for cluster in magenta_clusters:
      for pixel in cluster:
        if pixel[0] == 0 or pixel[0] == 1:
          rightmost_pixels.append(find_rightmost_pixel(cluster))
          break # only check first cluster that starts on row 0 or 1

    # remove any duplicates
    rightmost_pixels = list(set(rightmost_pixels))

    # Add the new pixels
    for pixel in rightmost_pixels:
      output_grid[rows - 1, pixel[1]] = 4

    return output_grid