"""
Identify contiguous regions of white (0) pixels surrounded by azure (8) pixels. Change these enclosed white pixels to green (3).
"""

import numpy as np

def get_neighbors(grid, r, c):
    """Returns the valid neighbors of a cell (r, c) in a grid."""
    rows, cols = grid.shape
    neighbors = []
    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Only orthogonal neighbors
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def is_enclosed(grid, r, c, visited):
    """Checks if a white pixel is part of an enclosed region."""
    if (r, c) in visited:
        return True, visited  # Already checked, avoid infinite loops

    visited.add((r, c))
    neighbors = get_neighbors(grid, r, c)

    # If any neighbor is out of bounds, it is not fully enclosed by azure
    if not neighbors:
        return False, visited

    all_neighbors_enclosed = True
    for nr, nc in neighbors:
        if grid[nr, nc] == 0:
            neighbor_enclosed, visited = is_enclosed(grid, nr, nc, visited)
            if not neighbor_enclosed:
                all_neighbors_enclosed = False  # Propagate non-enclosure
        elif grid[nr, nc] != 8:  # Check neighbor is azure
                return False, visited  # Not enclosed if neighbor is not 0 or 8
        
    return all_neighbors_enclosed, visited

def transform(input_grid):
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    visited = set()

    # Iterate through all pixels
    for r in range(rows):
        for c in range(cols):
            # If the pixel is white (0), check if it's enclosed
            if output_grid[r, c] == 0 and (r,c) not in visited:
                enclosed, visited = is_enclosed(output_grid, r, c, set())
                if enclosed:
                    # Fill the enclosed region with green
                    for enclosed_r, enclosed_c in visited:
                      if output_grid[enclosed_r, enclosed_c] == 0:
                        output_grid[enclosed_r, enclosed_c] = 3
                else:
                    #clear visited set from failed enclosure checks
                    visited = set()

    return output_grid