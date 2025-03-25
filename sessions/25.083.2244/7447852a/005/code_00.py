"""
The transformation identifies '0's enclosed by '2's, considering only orthogonal adjacency, and replaces these '0's with '4's. The '2' pixels act as boundaries for a flood fill operation.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # helper function to check for valid neighbors (orthogonal only)
    def get_neighbors(r, c):
        neighbors = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
        return neighbors

    # helper function to check if a region of 0s is fully enclosed by 2s
    def is_enclosed(zeros):
        for r, c in zeros:
            neighbors = get_neighbors(r, c)
            for nr, nc in neighbors:
                if input_grid[nr, nc] != 2 and (nr, nc) not in zeros:
                    return False  # Found a neighbor that's not 2 and not part of the zeros
        return True

    # helper function for flood fill, using only orthogonal neighbors
    def flood_fill(r, c, visited):
        region_zeros = []
        q = [(r,c)]

        while q:
          curr_r, curr_c = q.pop(0)
          if (curr_r, curr_c) in visited:
            continue
          visited.add((curr_r, curr_c))

          if input_grid[curr_r, curr_c] == 0:
            region_zeros.append((curr_r,curr_c))
            for nr, nc in get_neighbors(curr_r, curr_c):
                if input_grid[nr,nc] == 0:
                  q.append((nr,nc))
        return region_zeros


    # change output pixels - flood fill algorithm
    visited = set()
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 0 and (r, c) not in visited:
                region_zeros = flood_fill(r,c, visited)
                if is_enclosed(region_zeros):
                    for zr, zc in region_zeros:
                        output_grid[zr, zc] = 4

    return output_grid