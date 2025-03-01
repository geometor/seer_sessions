# 0e206a2e • 020 • refine_coder

---
```python
"""
1.  **Identify Single Pixels:** Find all single-pixel occurrences of blue (1), red (2), and yellow (4).
2.  **Identify Azure Cluster:** Find the contiguous cluster of azure (8) pixels.
3.  **Preserve Single Pixel Positions:** Maintain the original positions of the identified single pixels (blue, red, and yellow) in the output grid.
4.  **Move Azure Cluster:**
    *   Find the lowest row among all the identified single pixels.
    * Calculate the height of the azure cluster.
    * Move the azure cluster so it's bottom row aligns with the row *above* the lowest single pixel.
    *   Maintain the azure cluster's original horizontal (column) position.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the coordinates of pixels of a specific color."""
    return np.argwhere(grid == color)

def find_cluster(grid, color):
    """Finds a cluster of connected pixels of a specific color."""
    coords = find_pixels_by_color(grid, color)
    if len(coords) == 0:
        return []

    cluster = []
    visited = set()
    
    def dfs(row, col):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        cluster.append((row, col))
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)
        
    start_row, start_col = coords[0]
    dfs(start_row, start_col)

    return cluster

def get_lowest_single_pixel_row(blue_pixel, red_pixel, yellow_pixel):
    """
    Finds the row index of the lowest single pixel among blue, red, and yellow.
    """

    lowest_row = -1

    if len(blue_pixel) > 0:
      lowest_row = max(lowest_row, blue_pixel[0][0])
    if len(red_pixel) > 0:
      lowest_row = max(lowest_row, red_pixel[0][0])
    if len(yellow_pixel) > 0:
      lowest_row = max(lowest_row, yellow_pixel[0][0])
    
    return lowest_row
    
def transform(input_grid):
    # Initialize output_grid as all zeros
    output_grid = np.zeros_like(input_grid)

    # Find the single pixels (blue, red, yellow)
    blue_pixel = find_pixels_by_color(input_grid, 1)
    red_pixel = find_pixels_by_color(input_grid, 2)
    yellow_pixel = find_pixels_by_color(input_grid, 4)

    # Find the azure cluster
    azure_cluster = find_cluster(input_grid, 8)

    # Place the single pixels in the output grid
    if len(blue_pixel) > 0:
        output_grid[blue_pixel[0][0], blue_pixel[0][1]] = 1
    if len(red_pixel) > 0:
        output_grid[red_pixel[0][0], red_pixel[0][1]] = 2
    if len(yellow_pixel) > 0:
         output_grid[yellow_pixel[0][0], yellow_pixel[0][1]] = 4
   
    # Transform and place azure cluster
    if len(azure_cluster) > 0:
      # find lowest single pixel row
      lowest_row = get_lowest_single_pixel_row(blue_pixel, red_pixel, yellow_pixel)

      # calculate height of cluster
      cluster_height = max(row for row, _ in azure_cluster) - min(row for row, _ in azure_cluster) + 1

      # Target row is *one above* the lowest single pixel
      target_row = lowest_row - cluster_height
      
      # shift up if extends above grid
      if (target_row < 0):
          target_row = 0

      # calculate cluster shift
      row_shift = target_row - min(row for row, _ in azure_cluster)

      # Original leftmost column of the cluster
      original_col = min(col for _, col in azure_cluster)

      # Place the shifted cluster, maintaining original column
      for row, _ in azure_cluster: # Use _ since we calculate the column
        output_grid[row + row_shift, original_col] = 8
          
    return output_grid
```

