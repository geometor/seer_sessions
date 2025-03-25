"""
1.  **Identify Walls:** Locate all pixels of the designated "wall" color (8/azure). This includes both the horizontal and vertical lines formed by this color and the diagonal color line (4/yellow in the first pair and 3/green in the second).

2.  **Fill Adjacent Pixels:** For each pixel identified as part of a wall, change the color of all adjacent pixels (up, down, left, and right, but *not* diagonally) to the "fill" color (2/red), *unless* the adjacent pixel is also part of a wall (color 8, 4 in example 1 or 8,3 in example 2).

3.  **Propagate Fill:** Continue this filling process iteratively. For each newly filled pixel (color 2/red), repeat step 2, changing the color of its adjacent pixels to 2/red, again respecting the wall boundaries.

4. **Termination Condition**: Stop when no more pixels can be filled. This means no more azure (8) or other background colored pixels.

In summary, it's a region-filling algorithm where "walls" of a specific color define the boundaries of the regions, and a "fill" color propagates outwards from the walls until the entire region is filled.
"""

import numpy as np

def find_walls(grid, wall_colors):
    """
    Locates the wall pixels in the grid.
    """
    wall_pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] in wall_colors:
                wall_pixels.append((r, c))
    return wall_pixels

def get_neighbors(grid, r, c):
    """
    Gets the valid neighbors (up, down, left, right) of a pixel.
    """
    neighbors = []
    rows, cols = grid.shape
    if r > 0:
        neighbors.append((r - 1, c))  # Up
    if r < rows - 1:
        neighbors.append((r + 1, c))  # Down
    if c > 0:
        neighbors.append((r, c - 1))  # Left
    if c < cols - 1:
        neighbors.append((r, c + 1))  # Right
    return neighbors

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # Identify the set of wall colors
    wall_colors_set1 = {8, 4}
    wall_colors_set2 = {8,3}
    # Determine which wall set using the number of times the color occurs
    unique, counts = np.unique(input_grid, return_counts=True)
    if (3 in unique):
       wall_colors = wall_colors_set2
    else:
       wall_colors = wall_colors_set1

    # Identify wall pixels
    wall_pixels = find_walls(output_grid, wall_colors)

    # Fill color
    fill_color = 2

    # Initialize a queue with the initial fill pixels (neighbors of walls)
    fill_queue = []
    for r, c in wall_pixels:
        neighbors = get_neighbors(output_grid, r, c)
        for nr, nc in neighbors:
            if output_grid[nr, nc] not in wall_colors:
                fill_queue.append((nr, nc))

    # Iteratively fill the regions
    while fill_queue:
        r, c = fill_queue.pop(0)  # Get the next pixel to fill

        # Check again if it hasn't been filled or become a wall
        if output_grid[r, c] not in wall_colors and output_grid[r,c] != fill_color :
           output_grid[r, c] = fill_color
           neighbors = get_neighbors(output_grid, r, c)
           for nr, nc in neighbors:
               if output_grid[nr,nc] != fill_color:  # Add neighbors to queue if not already filled
                   fill_queue.append((nr, nc))
    return output_grid