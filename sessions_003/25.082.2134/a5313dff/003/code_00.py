"""
The transformation identifies closed shapes made of red (2) pixels and fills the area they enclose with blue (1) pixels, leaving a red (2) boundary, while leaving any other regions untouched.
"""

import numpy as np

def get_neighbors(grid, r, c):
    """
    Gets the valid neighbors of a cell in the grid.
    """
    rows, cols = grid.shape
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def is_enclosed(grid, start_r, start_c):
    """
    Checks if a region starting from (start_r, start_c) is enclosed by red (2) pixels.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    stack = [(start_r, start_c)]
    visited[start_r, start_c] = True
    enclosed = True

    while stack:
        r, c = stack.pop()

        if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
            enclosed = False  # Reached the edge

        for nr, nc in get_neighbors(grid, r, c):
            if not visited[nr, nc]:
                if grid[nr, nc] == 0:  # Continue flood fill only for white pixels
                    visited[nr, nc] = True
                    stack.append((nr, nc))
                elif grid[nr,nc] == 2:
                    continue # red pixel is boundary
                else:
                    enclosed = False # other color pixel is not enclosed
    return enclosed, visited
def transform(input_grid):
    """
    Transforms the input grid according to the rule:
    Find closed shapes made of red (2) pixels and fill their enclosed area with blue (1) pixels.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    processed = np.zeros_like(input_grid, dtype=bool)

    # Iterate through all pixels
    for r in range(rows):
        for c in range(cols):
            # Only consider white pixels that haven't been processed
            if output_grid[r, c] == 0 and not processed[r,c]:
                # Check if this white pixel is part of an enclosed region
                enclosed, visited_region = is_enclosed(output_grid, r, c)

                # If enclosed, fill the region with blue
                if enclosed:
                    for vr, vc in np.ndindex(output_grid.shape):  # Use ndindex for easy iteration
                        if visited_region[vr, vc]:
                            output_grid[vr, vc] = 1
                processed = np.logical_or(processed,visited_region) # combine

    return output_grid