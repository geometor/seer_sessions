```python
"""
1.  **Initialization:** Start with the input grid.
2.  **Magenta Rule:** Any azure (8) pixel that is *orthogonally* adjacent (directly above, below, left, or right) to a magenta (6) pixel changes to orange (7).
3.  **Blue Left Rule:** Any azure (8) pixel that has a blue (1) pixel directly to its left changes to orange (7).
4.  **Propagation:**
    *   Identify azure(8) pixels that became (7) in the current iteration.
    *   **Blue becomes Orange:** Check the neighbors of azure(8) pixels that became (7): If an orthogonally adjacent pixel is blue (1), change it to orange (7).
5.  **Iteration:** Repeat steps 2-4 until no pixels change color in an iteration. This ensures all cascading changes are captured.
"""

import numpy as np

def get_orthogonal_neighbors(grid, row, col):
    """Gets the orthogonally adjacent neighbors of a cell."""
    rows, cols = grid.shape
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        r, c = row + dr, col + dc
        if 0 <= r < rows and 0 <= c < cols:
            neighbors.append((r, c))
    return neighbors

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    while True:
        changed = False
        changed_to_7 = np.zeros_like(output_grid, dtype=bool) #track 8 -> 7 this iteration
        current_grid = np.copy(output_grid) # work on a copy each iteration

        # Rule 2: Magenta (6) adjacency
        for row in range(rows):
            for col in range(cols):
                if current_grid[row, col] == 8:
                    neighbors = get_orthogonal_neighbors(current_grid, row, col)
                    for r, c in neighbors:
                        if current_grid[r, c] == 6:
                            output_grid[row, col] = 7
                            changed_to_7[row, col] = True
                            changed = True
                            break

        # Rule 3: Blue (1) to the left of Azure (8)
        for row in range(rows):
            for col in range(cols):
                if current_grid[row, col] == 8:
                    if col > 0 and current_grid[row, col - 1] == 1:
                            output_grid[row, col] = 7
                            changed_to_7[row,col] = True
                            changed = True

        # Rule 4: Propagation.
        for row in range(rows):
            for col in range(cols):
                if current_grid[row,col] == 1:
                    neighbors = get_orthogonal_neighbors(current_grid, row, col)
                    for r,c in neighbors:
                        if current_grid[r,c] == 8 and changed_to_7[r,c]: #check output
                            output_grid[row,col] = 7
                            changed = True
        if not changed:
            break

    return output_grid
```
