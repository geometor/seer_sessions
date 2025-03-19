# d4a91cb9 • 020 • refine_coder

---
```python
"""
1.  **Identify Key Pixels:** Find the azure (8) and red (2) pixels in the input grid.

2.  **Check for Direct Connection or No Connection:**
    *   If the Manhattan distance between the azure and red pixels is 1, do not draw any connector. The output grid is identical to the input grid.
    *   If the azure and red pixels are in the same row or column, and the distance is greater than one, draw a direct yellow (4) line *between* them by changing existing pixel values in the grid to yellow.

3.  **Draw Adjacent Connector (L-Shaped):**
     * If the azure and red pixels are *not* in the same row or column,
       draw a yellow (4) line connecting *adjacent* pixels to create an "L" shaped connector.
        * Find the adjacent pixels to azure and red.
        * Find the shortest path by Manhattan distance between azure and red *adjacent* positions.
        * Change the values of the pixels along this shortest adjacent path to yellow.
"""

import numpy as np

def find_pixel(grid, color):
    # Find the coordinates of a pixel of the specified color.
    coords = np.where(grid == color)
    if len(coords[0]) > 0:
        return (coords[0][0], coords[1][0])  # Return first instance as (row, col)
    return None

def calculate_distance(pixel1, pixel2):
  #Calculate the Manhattan distance
  if pixel1 is None or pixel2 is None:
      return float('inf')
  return abs(pixel1[0] - pixel2[0]) + abs(pixel1[1] - pixel2[1])

def get_adjacent_pixels(grid, pixel):
    #returns list of adjacent pixels to a given pixel
    adjacent_pixels = []
    if pixel is not None:
      for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        r, c = pixel[0] + dr, pixel[1] + dc
        if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
            adjacent_pixels.append((r,c))
    return adjacent_pixels

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find the azure and red pixels.
    azure_pixel = find_pixel(input_grid, 8)
    red_pixel = find_pixel(input_grid, 2)

    if azure_pixel is None or red_pixel is None:
        return output_grid  # Return original if pixels are not found

    # Calculate Manhattan Distance
    distance = calculate_distance(azure_pixel, red_pixel)

    #Check Distance = 1, return unchanged
    if distance == 1:
      return output_grid

    # Check for direct connection
    if azure_pixel[0] == red_pixel[0] or azure_pixel[1] == red_pixel[1]:
        #draw direct line
        if azure_pixel[0] == red_pixel[0]:  # Same row, draw horizontal line.
            for col in range(min(azure_pixel[1], red_pixel[1]), max(azure_pixel[1], red_pixel[1])):
                output_grid[azure_pixel[0], col] = 4
        else: # Same column, draw a vertical line
            for row in range(min(azure_pixel[0],red_pixel[0]), max(azure_pixel[0], red_pixel[0])):
                output_grid[row, azure_pixel[1]] = 4
    else:
      #draw L shape connector
      azure_adj = get_adjacent_pixels(input_grid, azure_pixel)
      red_adj = get_adjacent_pixels(input_grid, red_pixel)

      # Find the closest adjacent positions using Manhattan distance.
      min_dist = float('inf')
      best_azure_adj = None
      best_red_adj = None

      for a_adj in azure_adj:
          for r_adj in red_adj:
              dist = abs(a_adj[0] - r_adj[0]) + abs(a_adj[1] - r_adj[1])
              if dist < min_dist:
                  min_dist = dist
                  best_azure_adj = a_adj
                  best_red_adj = r_adj

      if best_azure_adj is None or best_red_adj is None:
          return output_grid

      # Draw the connector line, always L-shape.
      # First draw from azure adjacent point to the corner point
      corner_row = best_red_adj[0]
      corner_col = best_azure_adj[1]

      if best_azure_adj[0] == corner_row: #horizontal segment first
        for col in range(min(best_azure_adj[1], corner_col), max(best_azure_adj[1],corner_col)+1):
          output_grid[best_azure_adj[0],col] = 4
        #then draw vertical segment from the corner
        for row in range(min(corner_row,best_red_adj[0]), max(corner_row,best_red_adj[0])+1):
          output_grid[row, corner_col] = 4
      else: #draw vertical segment first
        for row in range(min(best_azure_adj[0],corner_row), max(best_azure_adj[0], corner_row)+1):
          output_grid[row, best_azure_adj[1]] = 4
        #then draw horizontal segment from the corner
        for col in range(min(corner_col, best_red_adj[1]), max(corner_col,best_red_adj[1])+1):
          output_grid[corner_row,col] = 4

    return output_grid
```

