"""
1.  **Identify the Object:** Locate the vertical line of orange (7) pixels in the input grid.
2.  **Surround with Azure:** For each orange (7) pixel:
     a. Change any directly adjacent pixels, that are up, down, left, right, or diagonal, to azure (8).
3. **Wrap around:** If the original object touches the edge of the grid, extend the surrounding color to the opposite side.
"""

import numpy as np

def find_vertical_line(grid, color):
    """Finds the start and end coordinates of a vertical line of the specified color."""
    rows, cols = grid.shape
    for j in range(cols):
        for i in range(rows):
            if grid[i, j] == color:
                start = (i, j)
                while i < rows and grid[i, j] == color:
                    i += 1
                end = (i - 1, j)
                return start, end
    return None, None

def transform(input_grid):
    # initialize output_grid
    output_grid = input_grid.copy()
    rows, cols = output_grid.shape

    # Find the vertical line of orange pixels.
    start, end = find_vertical_line(input_grid, 7)

    if start is None:  # Handle cases where there's no orange line
      return output_grid

    # Iterate through the line and surround with azure.
    for r in range(start[0], end[0] + 1):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue

                nr, nc = r + dr, start[1] + dc
                
                # Wrap around logic
                if nr < 0:
                    nr = rows -1
                elif nr >= rows:
                    nr = 0

                if nc < 0:
                    nc = cols - 1
                elif nc >= cols:
                    nc = 0
                
                output_grid[nr, nc] = 8

    return output_grid