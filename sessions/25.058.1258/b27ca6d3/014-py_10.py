"""
1.  **Identify Red Pixels:** Locate all pixels with the value '2' (red).

2.  **Horizontal/Vertical Group Check:** For each red pixel:
    *   Check for horizontally or vertically adjacent red pixels.
    *   Count the number of *connected* red pixels (including the starting pixel).  "Connected" means reachable by moving horizontally or vertically through other red pixels.
    *   If the count is 3 or more, change the color of *all* connected red pixels in that group to '3' (green).

3.  **Isolated Diagonal Pair Check:** For each red pixel:
    *   Check for diagonally adjacent red pixels.
    *   If a diagonally adjacent red pixel is found, check *both* pixels to see if they have *any* other horizontally or vertically adjacent red neighbors.
    *   If *neither* of the two diagonally adjacent red pixels has any other red neighbors (H/V), change the color of *both* pixels to '3' (green).

4.  **All Other Pixels:**  Pixels not meeting the above conditions remain unchanged.
"""

import numpy as np

def get_hv_neighbors(grid, row, col):
    """Gets the horizontal and vertical neighbors of a cell."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i == row or j == col) and (i != row or j != col): # Exclude diagonals and self
                neighbors.append((i, j))
    return neighbors

def get_diagonal_neighbors(grid, row, col):
    """Gets the diagonal neighbors of a cell."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i != row and j != col):  # Only diagonals
                neighbors.append((i, j))
    return neighbors

def get_connected_hv_pixels(grid, row, col, target_color=2):
    """Gets all connected H/V pixels of the target color using a breadth-first search."""
    rows, cols = grid.shape
    connected_pixels = set()
    queue = [(row, col)]
    visited = set()

    while queue:
        r, c = queue.pop(0)
        if (r, c) in visited:
            continue
        visited.add((r,c))

        if grid[r, c] == target_color:
          connected_pixels.add((r,c))
          neighbors = get_hv_neighbors(grid, r, c)
          for nr, nc in neighbors:
            if (nr, nc) not in visited:
                queue.append((nr,nc))

    return connected_pixels
def transform(input_grid):
    """Transforms the input grid according to the specified rules."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    red_pixels = []

    # Identify Red Pixels and store for later
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 2:
              red_pixels.append((r,c))

    # Horizontal/Vertical Group Check
    for r, c in red_pixels:
        connected_pixels = get_connected_hv_pixels(output_grid, r, c)
        if len(connected_pixels) >= 3:
            for cr, cc in connected_pixels:
                output_grid[cr, cc] = 3

    #Rebuild red pixel list, taking into consideration the changes
    red_pixels = []
    for r in range(rows):
      for c in range(cols):
        if output_grid[r,c] == 2:
          red_pixels.append((r,c))


    # Isolated Diagonal Pair Check
    for r, c in red_pixels:
      diagonal_neighbors = get_diagonal_neighbors(output_grid,r,c)
      for dr, dc, in diagonal_neighbors:
        if output_grid[dr,dc] == 2:
          neighbors1 = get_hv_neighbors(output_grid,r,c)
          neighbors2 = get_hv_neighbors(output_grid,dr,dc)
          has_other_red_neighbors1 = any(output_grid[nr, nc] == 2 for nr, nc in neighbors1)
          has_other_red_neighbors2 = any(output_grid[ndr, ndc] == 2 for ndr, ndc in neighbors2)

          if not has_other_red_neighbors1 and not has_other_red_neighbors2:
            output_grid[r,c] = 3
            output_grid[dr,dc] = 3

    return output_grid