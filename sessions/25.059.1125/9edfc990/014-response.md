# 9edfc990 • 014 • refine_coder

---
```python
"""
1.  **Identify Enclosed Areas:** Scan the input grid to identify areas completely enclosed by a continuous, single-pixel-wide boundary. The boundary can be of *any* color (not just black), including blue itself.
2.  **Fill Enclosed Areas:** For each identified enclosed area, change all pixels *within* that area to blue (1).
3.  **No Extraneous Expansion:** Do *not* change any pixels outside the enclosed areas. The transformation only involves filling identified enclosed regions.
"""

import numpy as np
from scipy.ndimage import label, measurements

def get_neighbors(grid, row, col, include_diag = False):
    """
    Returns a list of valid neighbors (up, down, left, right, and optionally diagonals) for a given cell.
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    if include_diag:
        if row > 0 and col > 0:
            neighbors.append((row - 1, col - 1))  # Up-Left
        if row > 0 and col < cols - 1:
            neighbors.append((row - 1, col + 1))  # Up-Right
        if row < rows - 1 and col > 0:
            neighbors.append((row + 1, col - 1))  # Down-Left
        if row < rows - 1 and col < cols - 1:
            neighbors.append((row + 1, col + 1))  # Down-Right
    return neighbors
    

def is_enclosed(grid, row, col, boundary_pixels):
    """
    Checks if a given pixel is part of an enclosed area using a flood-fill approach.
    Returns True if enclosed, False otherwise.
    """
    rows, cols = grid.shape
    visited = set()
    to_visit = [(row, col)]

    while to_visit:
        r, c = to_visit.pop()

        if (r, c) in visited:
            continue
        visited.add((r, c))

        # If we hit the edge of the grid, it's not enclosed
        if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
            return False

        neighbors = get_neighbors(grid, r, c)
        for nr, nc in neighbors:
            # If the neighbor is a boundary pixel, we don't explore it
            if (nr, nc) in boundary_pixels:
                continue
            # Otherwise, add the neighbor to the list to visit
            if (nr,nc) not in visited:
                to_visit.append((nr, nc))

    return True


def find_enclosed_areas(grid):
    """
    Identifies and returns a list of enclosed areas within the grid.
    Each enclosed area is represented as a set of (row, col) tuples.
    """
    rows, cols = grid.shape
    enclosed_areas = []
    boundary_pixels = set()
    # first create list of possible boundary pixels - any pixel that touches a different color
    for r in range(rows):
        for c in range(cols):
            neighbors = get_neighbors(grid, r, c, include_diag=True)
            for nr, nc in neighbors:
                if grid[r,c] != grid[nr,nc]:
                    boundary_pixels.add((r,c))
                    break # found boundary

    # now loop for non-boundary pixels
    visited = set()  # Keep track of visited pixels to avoid redundant checks
    for r in range(rows):
        for c in range(cols):
            if (r,c) not in boundary_pixels and (r,c) not in visited:
                # check if is enclosed, using boundary_pixels list
                if is_enclosed(grid, r, c, boundary_pixels):
                    # now get fill pixels
                    enclosed_area = set()
                    to_visit = [(r, c)]
                    while to_visit:
                        vr, vc = to_visit.pop()
                        if (vr, vc) in visited:
                            continue
                        visited.add((vr,vc))
                        if (vr, vc) not in boundary_pixels:
                            enclosed_area.add((vr,vc)) # part of the fill
                            # add neighbors that aren't boundary
                            neighbors = get_neighbors(grid, vr, vc)
                            for nr, nc in neighbors:
                                if (nr, nc) not in boundary_pixels and (nr,nc) not in visited:
                                    to_visit.append((nr,nc))

                    enclosed_areas.append(enclosed_area)

    return enclosed_areas

def transform(input_grid):
    """
    Fills enclosed areas in the input grid with blue (1).
    """
    output_grid = np.copy(input_grid)
    enclosed_areas = find_enclosed_areas(input_grid)

    # Fill each enclosed area with blue
    for area in enclosed_areas:
        for row, col in area:
            output_grid[row, col] = 1

    return output_grid
```
