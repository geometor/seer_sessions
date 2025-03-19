# d06dbe63 • 012 • refine_coder

---
```python
"""
1.  **Locate the Seed:** Find the azure (8) cell within the input grid. This cell is the "seed" for the transformation.
2.  **Preserve the Seed:**  The seed cell's position and color (azure) are unchanged in the output grid.
3.  **Expand Grey Fill:** From the seed cell's location, fill all adjacent cells with grey (5).
4.  **Iterate Expansion:** Continue expanding the grey fill outwards in all directions (horizontally, vertically, and diagonally) from every grey cell.
5.  **Boundary Condition:** Stop the expansion of grey at the edges of the grid.  The expansion does *not* wrap around.
6.  **Replacement Rule:** Change all cells to grey except the original azure seed.
"""

import numpy as np

def find_seed(grid):
    # Find the coordinates of the azure (8) cell.
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 8:
                return (i, j)
    return None

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    output_grid = np.copy(input_grid)
    seed_row, seed_col = find_seed(input_grid)

    if seed_row is None: # handle edge case where there is no seed
        return output_grid

    # Preserve seed cell
    # output_grid[seed_row, seed_col] = 8  # Already copied

    # Use a queue for breadth-first expansion
    queue = [(seed_row, seed_col)]

    while queue:
        row, col = queue.pop(0)

        # Iterate through all 8 neighbors (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  # Skip the current cell

                new_row, new_col = row + dr, col + dc

                # Check bounds and if the cell should be filled
                if 0 <= new_row < output_grid.shape[0] and 0 <= new_col < output_grid.shape[1]:
                    if output_grid[new_row, new_col] != 8:  # change all colors except the azure seed
                        output_grid[new_row, new_col] = 5
                        queue.append((new_row, new_col))  # Add the new grey cell to the queue
    return output_grid
```
