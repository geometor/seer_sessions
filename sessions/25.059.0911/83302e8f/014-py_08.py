"""
1.  **Identify Boundaries:** Locate all blue (1) pixels. These form the boundaries.

2.  **Flood Fill with Green (3):** Starting from any black (0) pixel, change its color to green (3). Continue expanding this green region in all four directions (up, down, left, right) until a blue (1) pixel or the edge of the grid is encountered. Repeat this for all disconnected black regions until no more black pixels can be filled with green.

3.  **Flood Fill with Yellow (4):** Starting from any remaining black (0) pixel, change its color to yellow (4).  Continue expanding in all four directions until any of the following is encountered:

    *   A blue (1) pixel.
    *   A green (3) pixel.
    *   A yellow (4) pixel that is also connected to a boundary (either an edge or another boundary color - 1 or 3)
    *   If the current black pixel is completely surrounded by boundary pixels, it should be converted to yellow, regardless of the number of unique boundary pixels.

4.  Repeat step 3 until there are no more black pixels.
"""

import numpy as np

def flood_fill(grid, r, c, fill_color, boundary_colors):
    """
    Fills a region in the grid with the specified fill_color, starting from
    the given coordinates, until it encounters a boundary color or reaches the grid edge.
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

def is_surrounded(grid, r, c, boundary_colors):
    """
    Checks if a cell is surrounded by boundary colors or edges.
    """
    rows, cols = grid.shape
    neighbors = []
    if r > 0:
        neighbors.append(grid[r - 1, c])
    else:
        neighbors.append(-1) # Use -1 to denote an edge
    if r < rows - 1:
        neighbors.append(grid[r + 1, c])
    else:
        neighbors.append(-1)  # Edge
    if c > 0:
        neighbors.append(grid[r, c - 1])
    else:
        neighbors.append(-1) # Edge
    if c < cols - 1:
        neighbors.append(grid[r, c + 1])
    else:
        neighbors.append(-1)  # Edge

    for neighbor in neighbors:
        if neighbor not in boundary_colors and neighbor != -1:
          return False
    return True
    

def flood_fill_yellow(grid, r, c, fill_color, boundary_colors):
    """
    Fills a region, stopping if it hits a boundary or a yellow that's already connected to a boundary.
    """
    rows, cols = grid.shape

    if (r < 0 or r >= rows or c < 0 or c >= cols or
        grid[r, c] in boundary_colors or grid[r, c] == fill_color):
        return

    # Check if surrounded
    if is_surrounded(grid, r, c, boundary_colors + [fill_color]):
        grid[r,c] = fill_color
        return

    # Check if the cell is already yellow and connected to boundary
    if grid[r,c] == fill_color:
       if is_surrounded(grid, r, c, boundary_colors):
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