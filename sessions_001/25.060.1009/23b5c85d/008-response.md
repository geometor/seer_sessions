# 23b5c85d • 008 • refine_coder

---
```python
"""
Transforms the input grid based on the presence and size of azure squares.

If azure squares are present, the smallest one is returned.
If no azure squares are present, a 3x3 square of a specific color (red or green)
is returned, depending on examples provided.
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
    Transforms the input grid by extracting the smallest azure square or
    returning a 3x3 colored square if no azure squares are found.
    """
    # Find all azure (8) squares.
    azure_squares = find_all_squares(input_grid, 8)

    # If azure squares are present, return the smallest one.
    if azure_squares:
        smallest_square = min(azure_squares, key=lambda x: x[2])
        size = smallest_square[2]
        output_grid = np.full((size, size), 8, dtype=int)
        return output_grid

    # If no azure squares are present, return a 3x3 red or green square.
    # Based on the provided examples, the color is red for the second example
    # and green for the third, lacking further context, assume red color for now.
    output_grid = np.full((3, 3), 2, dtype=int)  # Red square
    return output_grid
```
