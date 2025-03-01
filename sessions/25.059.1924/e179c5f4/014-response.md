# e179c5f4 • 014 • refine_coder

---
```python
"""
1.  **Identify Seed Pixels:** Locate all blue (1) and azure (8) pixels in the input grid. These constitute the initial seed pixels.
2.  **Preserve Seed State:** Copy the initial seed pixels (both blue and azure) from the input grid to the output grid, maintaining their original positions and colors.
3.  **Alternating Expansion:**
    *   Initialize an empty queue. Add all seed pixel positions to the queue.
    *   While the queue is not empty:
        *   Dequeue a pixel position (row, column).
        *   Get the color of the current pixel in the *output* grid.
        *   Check its four immediate neighbors (up, down, left, right).
        *   For each neighbor:
            *   If the neighbor is within the grid boundaries and is white (0) in the *output* grid:
                *   If the current pixel is blue (1), change the neighbor to azure (8) in the output grid.
                *   If the current pixel is azure (8), change the neighbor to blue (1) in the output grid.
                *   Enqueue the neighbor's position.
"""

import numpy as np

def get_seed_positions(grid):
    # Find the coordinates of all blue (1) and azure (8) cells.
    blue_coords = np.where(grid == 1)
    azure_coords = np.where(grid == 8)
    blue_seeds = list(zip(blue_coords[0], blue_coords[1]))
    azure_seeds = list(zip(azure_coords[0], azure_coords[1]))
    return blue_seeds + azure_seeds

def is_valid(r, c, grid):
    # Check if row, col are within the grid boundaries
    rows, cols = grid.shape
    return 0 <= r < rows and 0 <= c < cols

def transform(input_grid):
    # initialize output_grid with zeros and the same dimensions
    output_grid = np.zeros_like(input_grid)

    # get seed positions
    seed_positions = get_seed_positions(input_grid)

    # Preserve Seed state: Copy seed pixels to output_grid
    for r, c in seed_positions:
        output_grid[r, c] = input_grid[r, c]

    # Create a queue for cells to be processed, initialized with seed positions
    queue = seed_positions.copy()

    # Loop to change output pixels
    while queue:
        r, c = queue.pop(0)  # Dequeue a cell
        current_color = output_grid[r,c]

        # Define neighbors (up, down, left, right)
        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

        for nr, nc in neighbors:
            if is_valid(nr, nc, output_grid):
                if output_grid[nr, nc] == 0: #if white
                    if current_color == 1:
                        output_grid[nr, nc] = 8  # white adjacent to 1 becomes 8
                        queue.append((nr, nc))
                    elif current_color == 8:
                        output_grid[nr, nc] = 1 # white adjacent to 8 becomes 1
                        queue.append((nr, nc))

    return output_grid
```

