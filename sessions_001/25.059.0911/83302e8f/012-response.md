# 83302e8f • 012 • refine_coder

---
```python
"""
1.  **Identify Boundaries:** Locate all blue (1) pixels that form continuous horizontal and vertical lines. These lines serve as boundaries for the filling process.

2.  **Flood Fill with Green (3):** Starting from any black (0) pixel, change its color to green (3). Continue expanding this green region in all four directions (up, down, left, right) until a blue (1) pixel line or the edge of the grid is encountered. Repeat this for all disconnected black regions until no more black pixels can be filled with green.

3.  **Flood Fill with Yellow (4):** Starting from any remaining black (0) pixel, change its color to yellow (4). Continue expanding in all four directions until any of the following is encountered:
    *   A blue (1) pixel.
    *   A green (3) pixel.
    *   Two edges of the grid (e.g. a corner or a black region adjacent to two non-connected edges)

4. Repeat step 3 until there are no more black pixels.
"""

import numpy as np

def flood_fill(grid, r, c, fill_color, boundary_colors):
    """
    Fills a region in the grid with the specified fill_color, starting from
    the given coordinates, until it encounters a boundary color or reaches grid edge twice.
    """
    rows, cols = grid.shape
    if (r < 0 or r >= rows or c < 0 or c >= cols or
        grid[r, c] in boundary_colors or grid[r,c] == fill_color):
        return

    grid[r, c] = fill_color

    flood_fill(grid, r + 1, c, fill_color, boundary_colors)
    flood_fill(grid, r - 1, c, fill_color, boundary_colors)
    flood_fill(grid, r, c + 1, fill_color, boundary_colors)
    flood_fill(grid, r, c - 1, fill_color, boundary_colors)

def flood_fill_yellow(grid, r, c, fill_color, boundary_colors):
    """
    Fills a region in the grid, stopping if it touches two or more edges or other boundary_colors.
    """
    rows, cols = grid.shape

    if (r < 0 or r >= rows or c < 0 or c >= cols or
        grid[r, c] in boundary_colors or grid[r, c] == fill_color):
        return

    edge_count = 0
    if r == 0 or r == rows - 1:
        edge_count += 1
    if c == 0 or c == cols - 1:
        edge_count += 1

    # If we hit another edge while filling, and the cell is not already the fill color, stop filling this path
    neighbor_edge_count = 0;
    if r > 0 and (grid[r-1,c] in boundary_colors or (r-1 == 0 or r-1 == rows -1)):
          neighbor_edge_count +=1
    if r < rows - 1 and (grid[r+1,c] in boundary_colors or (r+1 == 0 or r+1 == rows - 1)):
          neighbor_edge_count += 1
    if c > 0 and (grid[r,c-1] in boundary_colors or (c-1 == 0 or c-1 == cols -1)):
          neighbor_edge_count +=1
    if c < cols - 1 and (grid[r,c+1] in boundary_colors or (c+1 == 0 or c+1 == cols - 1)):
          neighbor_edge_count += 1

    if edge_count >=1 and neighbor_edge_count >=1 and grid[r,c] != fill_color:
        return

    grid[r, c] = fill_color

    flood_fill_yellow(grid, r + 1, c, fill_color, boundary_colors)
    flood_fill_yellow(grid, r - 1, c, fill_color, boundary_colors)
    flood_fill_yellow(grid, r, c + 1, fill_color, boundary_colors)
    flood_fill_yellow(grid, r, c - 1, fill_color, boundary_colors)
    

def transform(input_grid):
    # initialize output_grid
    output_grid = input_grid.copy()
    rows, cols = output_grid.shape

    # Flood fill with green, treating blue as the boundary.
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 0:
                flood_fill(output_grid, r, c, 3, [1])

    # Flood fill remaining black areas with yellow.
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 0:
                flood_fill_yellow(output_grid, r, c, 4, [1, 3])

    return output_grid
```
