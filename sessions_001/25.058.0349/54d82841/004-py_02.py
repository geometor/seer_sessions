"""
1.  **Identify Magenta Clusters:** Find all contiguous clusters of magenta (color 6) pixels in the input grid.
2.  **Filter Clusters:** Consider only the clusters that contain at least one magenta pixel on the first or second row (index 0 or 1).
3.  **Find Rightmost Magenta Pixel (of filtered set):** For *each* of the filtered clusters, identify the rightmost magenta pixel.
4.  **Place Yellow Pixel:** For *each* rightmost magenta pixel found in the previous step, place a yellow (color 4) pixel in the last row of the output grid. The column index of the yellow pixel should be the same as the column index of the corresponding rightmost magenta pixel.
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

def filter_clusters_by_row(clusters, rows_to_check):
    filtered_clusters = []
    for cluster in clusters:
        for pixel in cluster:
            if pixel[0] in rows_to_check:
                filtered_clusters.append(cluster)
                break  # Move to the next cluster once a pixel is found in the specified rows
    return filtered_clusters

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Identify Magenta Clusters
    magenta_clusters = find_clusters(output_grid, 6)

    # Filter Clusters by rows 0 and 1
    filtered_clusters = filter_clusters_by_row(magenta_clusters, [0, 1])

    # Find Rightmost Magenta Pixels in the filtered clusters
    rightmost_pixels = []
    for cluster in filtered_clusters:
        rightmost_pixels.append(find_rightmost_pixel(cluster))

    # Place Yellow Pixels
    for pixel in rightmost_pixels:
        output_grid[rows - 1, pixel[1]] = 4

    return output_grid