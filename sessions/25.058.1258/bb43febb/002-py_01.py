"""
The transformation identifies gray rectangles in the input grid and replaces a portion of the inner rectangle with red pixels, creating a red rectangle inside each gray rectangle with a one-pixel gray border.
"""

import numpy as np

def find_rectangles(grid, color):
    # Find all rectangles of a specific color in the grid.
    rectangles = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                # Start a new rectangle
                x1, y1 = c, r
                x2, y2 = c, r

                # Expand right
                while x2 + 1 < cols and grid[y1, x2 + 1] == color and not visited[y1, x2+1]:
                    x2 += 1

                # Expand down
                while y2 + 1 < rows and all(grid[y2 + 1, x1:x2 + 1] == color) and not any(visited[y2+1, x1:x2+1]):
                    y2 += 1

                # Mark as visited
                visited[y1:y2 + 1, x1:x2 + 1] = True
                rectangles.append((x1, y1, x2, y2))
    return rectangles

def transform(input_grid):
    """
    Transforms the input grid by finding gray rectangles and replacing the
    innermost part with red pixels.
    """
    output_grid = np.copy(input_grid)
    gray_rectangles = find_rectangles(input_grid, 5)

    for x1, y1, x2, y2 in gray_rectangles:
        # Define and color inner rectangle red, with the edge touching the sides but inset on top and bottom
        if x2 > x1 and y2 > y1: # Make sure it is at least 3x3
            output_grid[y1+1:y2, x1:x2+1] = 2

    return output_grid