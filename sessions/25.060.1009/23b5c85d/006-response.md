# 23b5c85d • 006 • refine_coder

---
```python
"""
Identifies the smallest azure square within the input grid and returns it as a new grid.
"""

import numpy as np

def find_all_squares(grid, color):
    """
    Finds all squares of a specified color in the grid.
    Returns a list of tuples: (top_left_row, top_left_col, size)
    """
    squares = []
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)

    def is_square(r, c, size):
        """
        Checks if a square of given size exists at (r, c).
        """
        if r + size > rows or c + size > cols:
            return False
        for i in range(r, r + size):
            for j in range(c, c + size):
                if grid[i, j] != color:
                    return False
        return True

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                # Find the maximum possible size of the square
                max_size = 1
                while is_square(r, c, max_size + 1):
                    max_size += 1

                #check if it a valid square and add to squares if so
                if max_size > 0:
                  squares.append( (r,c,max_size) )

                # Mark the region as visited
                for i in range(r, r + max_size):
                    for j in range(c, c + max_size):
                        visited[i, j] = True
    return squares

def transform(input_grid):
    """
    Transforms the input grid by extracting the smallest azure square.
    """
    # Find all azure (8) squares.
    azure_squares = find_all_squares(input_grid, 8)

    # Check if any azure squares were found
    if not azure_squares:
      return np.array([[]])

    # Find the smallest square.
    smallest_square = min(azure_squares, key=lambda x: x[2])

    # Extract the size of the smallest square.
    size = smallest_square[2]

    # Create an output grid of the correct dimensions filled with azure.
    output_grid = np.full((size, size), 8, dtype=int)

    return output_grid
```
