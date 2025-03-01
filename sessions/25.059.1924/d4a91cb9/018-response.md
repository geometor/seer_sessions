# d4a91cb9 • 018 • refine_coder

---
```python
"""
1.  **Identify Key Pixels:** Locate the azure (8) and red (2) pixels within the input grid.
2.  **Determine Relative Position:** Calculate the row and column differences between the red and azure pixels.
3.  **Draw Connector:** Draw a yellow (4) line *adjacent* to both the azure and red pixel. The line connects the closest points *adjacent* to the azure and red pixels. The line will always be vertical or horizontal, with up to one turn.
    * The connection is made by drawing a straight, one-pixel-wide line.
    * The line drawn will always be adjacent to both start and end pixel.
"""

import numpy as np

def find_pixel(grid, color):
    # Find the coordinates of a pixel of the specified color.
    coords = np.where(grid == color)
    if len(coords[0]) > 0:
        return (coords[0][0], coords[1][0])  # Return first instance as (row, col)
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find the azure and red pixels.
    azure_pixel = find_pixel(input_grid, 8)
    red_pixel = find_pixel(input_grid, 2)

    if azure_pixel is None or red_pixel is None:
        return output_grid  # Return original if pixels are not found

    # Determine adjacent positions.
    azure_adj = []
    red_adj = []

    # Adjacent positions for azure.
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
      r, c = azure_pixel[0] + dr, azure_pixel[1] + dc
      if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
          azure_adj.append((r,c))


    # Adjacent positions for red.
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
      r, c = red_pixel[0] + dr, red_pixel[1] + dc
      if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
          red_adj.append((r,c))

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

    # Draw the connector line, either horizontal or vertical.
    if best_azure_adj[0] == best_red_adj[0]:  # Same row, draw horizontal line.
        for col in range(min(best_azure_adj[1], best_red_adj[1]), max(best_azure_adj[1], best_red_adj[1]) + 1):
            output_grid[best_azure_adj[0], col] = 4
    elif best_azure_adj[1] == best_red_adj[1]: # Same column, draw a vertical line
        for row in range(min(best_azure_adj[0],best_red_adj[0]), max(best_azure_adj[0], best_red_adj[0])+1):
            output_grid[row, best_azure_adj[1]] = 4
    else:
        # Draw a two-part connector (L-shape).
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
