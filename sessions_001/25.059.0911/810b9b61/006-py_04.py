"""
1.  **Identify Enclosing Regions:** Find all contiguous regions of blue (1) pixels that completely enclose one or more white (0) pixels.  "Completely enclose" means that there is no path from a white pixel in the enclosed region to the edge of the grid without crossing a blue pixel.
2.  **Transform Enclosing Region:** Change all blue pixels that form the enclosing region(s) to green (3).
3.  **Preserve Unchanged Pixels:** All other pixels remain their original color.
"""

import numpy as np
from collections import deque

def is_enclosed(grid, start_row, start_col):
    """
    Checks if a white region is enclosed by blue pixels using a flood fill algorithm.
    """
    rows, cols = grid.shape
    if grid[start_row, start_col] != 0:
        return False  # Start with a white pixel

    visited = set()
    queue = deque([(start_row, start_col)])

    while queue:
        row, col = queue.popleft()

        if (row, col) in visited:
            continue
        visited.add((row, col))

        # Check if we've reached the edge of the grid
        if row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
            return False  # Not enclosed

        # Explore adjacent cells
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr, nc] == 0 and (nr, nc) not in visited:
                    queue.append((nr, nc))
                # If we encounter blue, we just stop exploring in that direction (it's a boundary)

    return True  # Enclosed

def find_enclosing_blue_pixels(grid):
    """
    Finds all blue pixels that are part of an enclosing region.
    """
    rows, cols = grid.shape
    enclosing_blue_pixels = set()

    # Find all white regions and check if they are enclosed
    white_regions = []
    visited = set()
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 0 and (r, c) not in visited:
                if is_enclosed(grid, r, c):
                    white_regions.append((r, c))
                # mark this region as visited so we don't process again.
                queue = deque([(r, c)])
                while queue:
                    row, col = queue.popleft()
                    if (row, col) in visited:
                        continue
                    visited.add((row, col))
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 0 and (nr, nc) not in visited:
                            queue.append((nr, nc))

    # For each enclosed white region, find the surrounding blue pixels
    for start_row, start_col in white_regions:
        queue = deque([(start_row, start_col)])
        visited_white = set()
        while queue:
            row, col = queue.popleft()
            if (row, col) in visited_white:
                continue
            visited_white.add((row,col))

            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr, nc] == 1:
                        enclosing_blue_pixels.add((nr, nc))
                    elif grid[nr, nc] == 0 and (nr, nc) not in visited_white:
                        queue.append((nr, nc))

    return enclosing_blue_pixels
    

def transform(input_grid):
    """
    Transforms the input grid by changing blue pixels enclosing white regions to green.
    """
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find blue pixels that enclose white regions
    enclosing_blue_pixels = find_enclosing_blue_pixels(input_grid)

    # change output pixels
    for row, col in enclosing_blue_pixels:
        output_grid[row, col] = 3

    return output_grid