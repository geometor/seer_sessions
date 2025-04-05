import numpy as np
import collections

"""
Identifies a closed boundary shape of one color and an 'inner' element of another color within the input grid.
It then performs a flood fill operation, changing the color of all background (0) cells enclosed by the boundary shape to the color of the inner element.
The boundary shape and the original inner element(s) retain their colors.

1. Identify the two distinct non-zero colors present in the grid.
2. Determine which color forms the boundary and which color is the 'fill' color (the one initially inside). This is done by tentatively assuming one color is the boundary, finding the enclosed '0' cells, and checking if the other color is adjacent to any of these enclosed cells.
3. Identify all '0' cells reachable from the grid edges without crossing the determined boundary color. These are 'outside' cells.
4. All '0' cells not reachable from the edges are considered 'inside'.
5. Change the color of all 'inside' '0' cells to the determined fill color in the output grid.
"""

def _is_valid(r, c, rows, cols):
  """Checks if coordinates are within grid bounds."""
  return 0 <= r < rows and 0 <= c < cols

def _find_inside_zeros(grid, boundary_color):
    """
    Finds the coordinates of all background (0) cells that are enclosed
    by the boundary_color, meaning they cannot reach the edge of the grid
    by moving only through 0-cells.

    Args:
        grid (np.array): The input grid.
        boundary_color (int): The color value acting as the boundary.

    Returns:
        list: A list of (row, col) tuples for inside zero cells.
    """
    rows, cols = grid.shape
    reachable_from_edge = np.zeros_like(grid, dtype=bool)
    q = collections.deque()

    # Add all edge '0' cells to the queue and mark as reachable
    for r in range(rows):
        for c in [0, cols - 1]:
            if grid[r, c] == 0 and not reachable_from_edge[r, c]:
                reachable_from_edge[r, c] = True
                q.append((r, c))
    for c in range(cols):
        for r in [0, rows - 1]:
             if grid[r, c] == 0 and not reachable_from_edge[r, c]:
                reachable_from_edge[r, c] = True
                q.append((r, c))

    # Perform BFS from edge zeros
    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if _is_valid(nr, nc, rows, cols) and \
               not reachable_from_edge[nr, nc] and \
               grid[nr, nc] == 0:
                reachable_from_edge[nr, nc] = True
                q.append((nr, nc))

    # Identify inside zeros (those not reachable from the edge)
    inside_zeros = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 0 and not reachable_from_edge[r, c]:
                inside_zeros.append((r, c))

    return inside_zeros

def transform(input_grid):
    """
    Transforms the input grid by flood-filling the area enclosed by a
    boundary color with the color of an element found inside that boundary.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    rows, cols = grid.shape

    # Find the unique non-zero colors
    colors = [c for c in np.unique(grid) if c != 0]

    # Handle cases with less than 2 distinct non-zero colors (no fill possible)
    if len(colors) < 2:
        return output_grid.tolist()

    c1, c2 = colors[0], colors[1]
    boundary_color = -1
    fill_color = -1
    found_config = False

    # --- Determine Boundary and Fill Color ---
    # Try c1 as boundary
    inside_zeros_c1 = _find_inside_zeros(grid, c1)
    for r, c in inside_zeros_c1:
         for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if _is_valid(nr, nc, rows, cols) and grid[nr, nc] == c2:
                boundary_color = c1
                fill_color = c2
                found_config = True
                break
         if found_config:
             break

    # If not found, try c2 as boundary
    if not found_config:
        inside_zeros_c2 = _find_inside_zeros(grid, c2)
        for r, c in inside_zeros_c2:
             for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if _is_valid(nr, nc, rows, cols) and grid[nr, nc] == c1:
                    boundary_color = c2
                    fill_color = c1
                    found_config = True
                    break
             if found_config:
                 break

    # If configuration still not determined (e.g., nested shapes or errors)
    # or if no fill is needed (no inside zeros found for the correct boundary), return original
    if not found_config:
         return output_grid.tolist() # Or handle potential edge cases differently

    # --- Perform the Fill ---
    # Find the inside zeros using the confirmed boundary color
    # We might already have this list from the check above
    if boundary_color == c1:
        inside_zeros_coords = inside_zeros_c1
    else: # boundary_color == c2
        inside_zeros_coords = inside_zeros_c2

    # Change the color of inside zeros in the output grid
    for r, c in inside_zeros_coords:
        output_grid[r, c] = fill_color

    return output_grid.tolist()