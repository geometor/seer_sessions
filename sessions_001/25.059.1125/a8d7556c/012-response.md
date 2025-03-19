# a8d7556c • 012 • refine_coder

---
```python
"""
The transformation involves changing white pixels to red if they are adjacent to grey pixels and form enclosed interior spaces.
"""

import numpy as np

def get_neighbors(grid, r, c):
    """Returns the coordinates of valid neighbors (up, down, left, right) of a pixel."""
    rows, cols = grid.shape
    neighbors = []
    if r > 0:
        neighbors.append((r - 1, c))  # Up
    if r < rows - 1:
        neighbors.append((r + 1, c))  # Down
    if c > 0:
        neighbors.append((r, c - 1))  # Left
    if c < cols - 1:
        neighbors.append((r, c + 1))  # Right
    return neighbors

def is_enclosed(grid, r, c, visited):
    """
    Checks if a white pixel is part of an enclosed region using a flood-fill-like approach.
    This function recursively checks if a path of white pixels can reach the boundary.
    """

    # Check the edges of the grid. If reached, it's not enclosed.
    if r == 0 or r == grid.shape[0] - 1 or c == 0 or c == grid.shape[1] - 1:
        return False
        
    visited.add((r,c))
    neighbors = get_neighbors(grid, r, c)

    for nr, nc in neighbors:
        if (nr, nc) not in visited:
            if grid[nr, nc] == 0:
                if not is_enclosed(grid, nr, nc, visited):
                    return False  # If a neighbor can reach the boundary, so can this.
            elif grid[nr,nc] == 5: # Gray
                continue # Continue to the boundary check, grey is the boundary.
            else:
               return False

    return True # Didn't find the boundary

def transform(input_grid):
    """
    Transforms the input grid by changing white pixels to red based on adjacency to grey
    and enclosure within grey boundaries.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    visited = set()

    # Iterate through all pixels
    for r in range(rows):
        for c in range(cols):
            # Process only white pixels
            if input_grid[r, c] == 0:
                # Check for adjacency to grey
                is_adjacent = False
                for nr, nc in get_neighbors(input_grid, r, c):
                    if input_grid[nr, nc] == 5:
                        is_adjacent = True
                        break
                
                visited.clear()

                # If adjacent to grey, check for enclosure and only color if enclosed
                if is_adjacent and is_enclosed(input_grid, r, c, visited):
                    output_grid[r, c] = 2  # Change to red

    return output_grid
```
