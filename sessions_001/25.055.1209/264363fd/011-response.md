# 264363fd • 011 • refine_coder

---
```python
"""
The transformation rule involves iteratively changing the color of pixels
based on the color of their adjacent neighbors.  Red (2) pixels change to
green (3) if adjacent to green (3). Yellow (4) pixels change to green (3)
if adjacent to green (3), Yellow (4) changes to Red (2) if adjacent to red(2). It's a cascading effect, where the
green "spreads" from its initial inferred position, converting adjacent
red and yellow pixels. The green color does not exist in the input, but exists in the output.
"""

import numpy as np

def get_seed_point(grid):
    """
    Finds the 'seed' point for green propagation. This is a non-green pixel adjacent to red or yellow,
    and is where we'll infer green starts.
    """
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] in (2, 4): # Look for red or yellow
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 0:
                            #check for adjacent background
                            #check if other red/yellow exists adjacent
                            for dr2 in [-1,0,1]:
                                for dc2 in [-1,0,1]:
                                    if dr2 == 0 and dc2 == 0:
                                        continue
                                    nr2, nc2 = nr + dr2, nc + dc2
                                    if 0<= nr2 < rows and 0 <= nc2 < cols and grid[nr2,nc2] in (2,4):
                                       
                                        return (nr, nc)
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the seed point for green.
    seed_point = get_seed_point(output_grid)
    if seed_point is None:
        return output_grid

    # Create green at the seed point
    output_grid[seed_point] = 3

    # Iteratively propagate the green color
    changed = True
    while changed:
        changed = False
        new_grid = np.copy(output_grid)
        for r in range(rows):
            for c in range(cols):
                # Check for adjacencies and apply striping
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue

                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if output_grid[r, c] == 2 and output_grid[nr, nc] == 3:
                                new_grid[r,c] = 3
                                changed = True
                            elif output_grid[r,c] == 4 and output_grid[nr,nc] == 3:
                                new_grid[r,c] = 3
                                changed = True
                            elif output_grid[r,c] == 4 and output_grid[nr,nc] == 2:
                                new_grid[r,c] = 2
                                changed = True
        output_grid = new_grid
    return output_grid
```
