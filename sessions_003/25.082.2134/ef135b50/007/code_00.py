"""
1.  **Copy Input:** Create a copy of the input grid. This copy will be modified and returned as the output grid.

2.  **Iterate:** Examine each pixel in the input grid.

3.  **Identify White Regions:** If a pixel is white (color 0) and has not been visited yet:

    *   Perform a Breadth-First Search (BFS) or Depth-First Search (DFS) to find all connected white pixels, forming a 'white region'.
    *   **Enclosure Check:** For *every* pixel in this white region:
        *   Check *all* possible paths from that pixel to the edge of the grid. A path consists of steps to adjacent or diagonally adjacent cells.
        *   If *any* path reaches the edge of the grid *without* encountering a red (color 2) pixel, the entire region is *not* enclosed. Stop checking paths for this region.
        *   If *all* paths from *all* pixels in the region encounter a red pixel *before* reaching the edge, the region is considered enclosed.

4.  **Fill Enclosed Regions:** For each white region identified as *enclosed*:

    *   Change the color of *all* pixels in that region to maroon (color 9) in the output grid.

5.  **Preserve Other Colors:** Any pixel in the input grid that is *not* white (0) should remain unchanged in the output grid.

6.  **Return:** Return the modified grid (the output grid).
"""

import numpy as np
from collections import deque

def get_neighbors(grid, row, col):
    """Gets the coordinates of all 8 neighbors (cardinal and diagonal) of a cell."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append((i, j))
    return neighbors

def get_white_region(grid, start_row, start_col, visited):
    """
    Finds all connected white pixels using BFS.
    Returns the region as a set of (row, col) tuples.
    """
    region = set()
    queue = deque([(start_row, start_col)])
    visited.add((start_row, start_col))

    while queue:
        row, col = queue.popleft()
        region.add((row, col))

        for r, c in get_neighbors(grid, row, col):
            if grid[r, c] == 0 and (r, c) not in visited:
                visited.add((r, c))
                queue.append((r, c))
    return region

def is_enclosed(grid, region):
    """
    Checks if a region is enclosed by red (2) pixels.
    """
    rows, cols = grid.shape

    for row, col in region:
        # Check all paths from this pixel to the edge
        queue = deque([(row, col)])
        visited_path = set()

        while queue:
            curr_row, curr_col = queue.popleft()

            if (curr_row, curr_col) in visited_path:
                continue  # Avoid cycles
            visited_path.add((curr_row, curr_col))
            
            if curr_row == 0 or curr_row == rows - 1 or curr_col == 0 or curr_col == cols - 1:
                 if grid[curr_row,curr_col] != 2:
                    return False # Reached the edge without encountering red

            neighbors = get_neighbors(grid, curr_row, curr_col)
            for nr, nc in neighbors:
              if grid[nr,nc] != 2: # only expand if not red.
                if (nr,nc) not in visited_path: # Avoid infinite loops and check all paths.
                    queue.append((nr, nc))


    return True  # All paths from all pixels in region hit red before edge


def transform(input_grid):
    """
    Transforms the input grid according to the enclosure rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    visited = set()

    # Iterate through the grid
    for i in range(rows):
        for j in range(cols):
            # Check for '0' pixels and enclosure
            if input_grid[i, j] == 0 and (i, j) not in visited:
                region = get_white_region(input_grid, i, j, visited)
                if is_enclosed(input_grid, region):
                    # Fill enclosed region
                    for r, c in region:
                        output_grid[r, c] = 9

    return output_grid