# 44d8ac46 • 002 • example_4 • investigate_coder

---
```python
"""
The transformation rule identifies regions enclosed by grey (5) pixels and changes the color of the interior white (0) pixels to red (2).
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Returns the valid neighbors of a cell in the grid.
    """
    rows, cols = grid.shape
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbors.append((new_row, new_col))
    return neighbors

def is_enclosed(grid, start_row, start_col):
    """
    Checks if a region starting from a given cell is fully enclosed by grey (5) pixels.
    Uses a Breadth-First Search (BFS) algorithm.
    """
    rows, cols = grid.shape
    visited = set()
    queue = [(start_row, start_col)]
    visited.add((start_row, start_col))

    while queue:
        row, col = queue.pop(0)

        # Check if we reached the edge of the grid
        if row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
            if grid[row, col] != 5:
                return False

        neighbors = get_neighbors(grid, row, col)
        for n_row, n_col in neighbors:
            if (n_row, n_col) not in visited:
                if grid[n_row, n_col] == 0:
                    visited.add((n_row, n_col))
                    queue.append((n_row, n_col))
                elif grid[n_row, n_col] == 5:
                    visited.add((n_row, n_col)) # add grey pixels
                    continue
                else: #not white or grey - should never be a different color
                    return False
                    
    return True

def transform(input_grid):
    """
    Transforms the input grid by identifying enclosed white regions and changing them to red.
    """
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    
    # Create a set to store coordinates of visited white pixels
    visited_white_pixels = set()

    # Iterate through the grid to find white (0) pixels
    for row in range(rows):
        for col in range(cols):
            if output_grid[row, col] == 0 and (row, col) not in visited_white_pixels:
                # Check if the region starting from this pixel is enclosed
                if is_enclosed(output_grid, row, col):
                    # If enclosed, change all connected white pixels to red (2)
                    queue = [(row, col)]
                    visited_white_pixels.add((row, col))
                    while queue:
                        r, c = queue.pop(0)
                        output_grid[r, c] = 2  # Change to red
                        neighbors = get_neighbors(output_grid, r, c)
                        for nr, nc in neighbors:
                            if output_grid[nr, nc] == 0 and (nr, nc) not in visited_white_pixels:
                                visited_white_pixels.add((nr, nc))
                                queue.append((nr, nc))
                else:
                  # must also add the pixels to visited if not enclosed
                  queue = [(row, col)]
                  visited_white_pixels.add((row, col))
                  while queue:
                    r, c = queue.pop(0)
                    neighbors = get_neighbors(output_grid, r, c)
                    for nr, nc in neighbors:
                        if output_grid[nr, nc] == 0 and (nr, nc) not in visited_white_pixels:
                            visited_white_pixels.add((nr, nc))
                            queue.append((nr, nc))

    return output_grid
```
