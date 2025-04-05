import numpy as np
import collections

"""
The transformation identifies a primary closed boundary shape of one color. 
Inside this boundary, there exists at least one 'pattern' element, potentially consisting of multiple cells of a different color (or sometimes the same color as the boundary).
The core operation involves tiling this inner 'pattern' onto all background (color 0) cells that are strictly enclosed by the boundary shape.

1.  **Initialize:** Create a copy of the input grid.
2.  **Identify Boundary Color:** Find the color forming the outermost closed loop. This is typically the color surrounding the largest contiguous area of '0's that cannot reach the grid edge.
3.  **Identify Enclosed Background Cells:** Perform a flood fill (BFS) starting from all '0' cells on the grid's edges. Mark all reachable '0' cells. Any '0' cell *not* marked is considered enclosed by the boundary.
4.  **Identify Inner Pattern:**
    *   Find all non-zero cells adjacent to the enclosed background cells identified in step 3. These form the potential inner pattern elements. Filter out cells that have the boundary color if they are part of the main boundary structure itself (e.g., check if they are adjacent to outside '0's).
    *   Determine the bounding box (min/max row/col) of these inner pattern cells.
    *   Extract the pattern: create a small 2D array representing the content within the bounding box, relative to the top-left corner (min_row, min_col) of the box. This pattern includes the identified inner pattern cells and any original '0's within that bounding box.
5.  **Tile Pattern:**
    *   Iterate through each enclosed background cell (from step 3) in the `output_grid`.
    *   Calculate the cell's position relative to the top-left corner of the pattern's bounding box: `rel_row = row - min_row`, `rel_col = col - min_col`.
    *   Determine the corresponding cell in the pattern using the modulo operator: `pattern_row = rel_row % pattern_height`, `pattern_col = rel_col % pattern_width`.
    *   Get the color from the `pattern[pattern_row, pattern_col]`.
    *   If the pattern color is not the background color (0), update the `output_grid` at `(row, col)` with this pattern color.
6.  **Return:** The modified `output_grid`.
"""

def _is_valid(r, c, rows, cols):
  """Checks if coordinates are within grid bounds."""
  return 0 <= r < rows and 0 <= c < cols

def _find_enclosed_background(grid, boundary_color):
    """
    Finds coordinates of background (0) cells enclosed by the boundary_color.
    Uses BFS starting from edge '0' cells. Cells not reached are enclosed.

    Args:
        grid (np.array): The input grid.
        boundary_color (int): The color acting as the boundary.

    Returns:
        list: A list of (row, col) tuples for enclosed background cells.
        np.array: A boolean mask where True indicates a cell reachable from edge.
    """
    rows, cols = grid.shape
    reachable_from_edge = np.zeros_like(grid, dtype=bool)
    q = collections.deque()

    # Add edge '0' cells to the queue
    for r in range(rows):
        for c in [0, cols - 1]:
            if grid[r, c] == 0 and not reachable_from_edge[r, c]:
                reachable_from_edge[r, c] = True
                q.append((r, c))
            # Also consider boundary cells on the edge as potentially allowing escape for adjacent 0s
            elif grid[r,c] == boundary_color:
                 reachable_from_edge[r,c] = True # Mark boundary on edge as 'visited' in context of reachability
    for c in range(cols):
        for r in [0, rows - 1]:
            if grid[r, c] == 0 and not reachable_from_edge[r, c]:
                reachable_from_edge[r, c] = True
                q.append((r, c))
            elif grid[r,c] == boundary_color:
                 reachable_from_edge[r,c] = True

    # BFS from edge zeros, cannot cross the boundary_color
    while q:
        r, c = q.popleft()
        # Check neighbors only if current cell is 0 (or was an edge boundary cell added initially)
        # This prevents exploring from inside the boundary if the initial queue contained edge boundary cells
        if grid[r,c] == 0:
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if _is_valid(nr, nc, rows, cols) and \
                   not reachable_from_edge[nr, nc] and \
                   grid[nr, nc] != boundary_color: # Cannot cross the boundary
                    reachable_from_edge[nr, nc] = True
                    q.append((nr, nc))

    # Identify enclosed background cells (0s not reachable)
    enclosed_zeros = []
    for r in range(rows):
        for c in range(cols):
            # A cell is enclosed if it's 0 AND not reachable
            if grid[r, c] == 0 and not reachable_from_edge[r, c]:
                enclosed_zeros.append((r, c))

    return enclosed_zeros, reachable_from_edge


def _get_inner_pattern_and_bbox(grid, enclosed_zeros_coords, boundary_color, reachable_mask):
    """
    Identifies the pattern elements inside the boundary and determines its bounding box.

    Args:
        grid (np.array): The input grid.
        enclosed_zeros_coords (list): Coords of enclosed '0' cells.
        boundary_color (int): The boundary color.
        reachable_mask (np.array): Boolean mask of cells reachable from the edge.

    Returns:
        tuple: (pattern_array, min_row, min_col) or (None, -1, -1) if no pattern found.
               pattern_array is a numpy array.
    """
    rows, cols = grid.shape
    inner_pattern_cells = []

    # Find non-zero, non-boundary cells adjacent to enclosed zeros
    # These form the 'seed' of the inner pattern
    potential_pattern_coords = set()
    enclosed_zeros_set = set(enclosed_zeros_coords)

    for r_zero, c_zero in enclosed_zeros_coords:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r_zero + dr, c_zero + dc
            if _is_valid(nr, nc, rows, cols) and grid[nr, nc] != 0 and grid[nr, nc] != boundary_color:
                 potential_pattern_coords.add((nr, nc))
            # Also consider boundary-colored cells if they are NOT part of the outer boundary
            elif _is_valid(nr, nc, rows, cols) and grid[nr, nc] == boundary_color:
                 # Check if this boundary cell is truly 'inside' - i.e., not adjacent to an outside '0'
                 is_outer_boundary = False
                 for dr2, dc2 in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                     nnr, nnc = nr + dr2, nc + dc2
                     # If adjacent to a reachable 0 or outside grid, it's part of outer boundary
                     if not _is_valid(nnr, nnc, rows, cols) or (grid[nnr,nnc] == 0 and reachable_mask[nnr,nnc]):
                          is_outer_boundary = True
                          break
                 if not is_outer_boundary:
                     potential_pattern_coords.add((nr, nc))


    if not potential_pattern_coords:
        # Check if there are *any* non-zero, non-boundary cells within the enclosed area at all
        # This handles cases where the pattern might be disconnected from the enclosed 0s initially
        for r in range(rows):
             for c in range(cols):
                 is_enclosed_non_boundary_non_zero = (
                     grid[r, c] != 0 and
                     grid[r, c] != boundary_color and
                     not reachable_mask[r, c] and # Must not be reachable from outside
                     (r,c) not in enclosed_zeros_set # Must not be a background cell
                 )
                 # Check also for potentially enclosed boundary-colored cells
                 is_enclosed_boundary = (
                     grid[r, c] == boundary_color and
                     not reachable_mask[r,c] # Initially assume boundary cells aren't reachable unless proven otherwise by BFS
                 )
                 if is_enclosed_boundary:
                      # Double check it's not adjacent to an outside area
                      is_outer_boundary = False
                      for dr2, dc2 in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                           nnr, nnc = r + dr2, c + dc2
                           if not _is_valid(nnr, nnc, rows, cols) or (grid[nnr,nnc] == 0 and reachable_mask[nnr,nnc]):
                                is_outer_boundary = True
                                break
                      if not is_outer_boundary:
                           potential_pattern_coords.add((r,c))

                 elif is_enclosed_non_boundary_non_zero:
                     potential_pattern_coords.add((r, c))

    if not potential_pattern_coords:
         # Special case check for test 3: inner pattern is same color as boundary
         # Look for boundary-colored cells surrounded only by other boundary cells or enclosed zeros
         for r_zero, c_zero in enclosed_zeros_coords:
             for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                 nr, nc = r_zero + dr, c_zero + dc
                 if _is_valid(nr, nc, rows, cols) and grid[nr, nc] == boundary_color:
                     # Check if this boundary cell is truly 'inside'
                     is_outer_boundary = False
                     for dr2, dc2 in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                         nnr, nnc = nr + dr2, nc + dc2
                         if not _is_valid(nnr, nnc, rows, cols) or (grid[nnr, nnc] == 0 and reachable_mask[nnr, nnc]):
                             is_outer_boundary = True
                             break
                     if not is_outer_boundary:
                         potential_pattern_coords.add((nr, nc))

    if not potential_pattern_coords:
        return None, -1, -1 # No pattern found

    # Find bounding box of the identified pattern cells
    min_row = min(r for r, c in potential_pattern_coords)
    max_row = max(r for r, c in potential_pattern_coords)
    min_col = min(c for r, c in potential_pattern_coords)
    max_col = max(c for r, c in potential_pattern_coords)

    pattern_height = max_row - min_row + 1
    pattern_width = max_col - min_col + 1

    # Extract the pattern from the original grid within the bounding box
    pattern_array = grid[min_row : max_row + 1, min_col : max_col + 1].copy()

    # Important: Ensure that only originally non-zero cells or *internal* zeros
    # within the pattern's bounding box contribute. Zeros that were part of the
    # main "enclosed background" area should remain 0 in the pattern template
    # unless they were explicitly part of the pattern structure.
    # Let's refine the pattern: only keep original non-zero values from potential_pattern_coords
    # or original zero values if they fall within the bbox.
    # This seems complex, let's rethink. Simpler: just extract the bbox area.
    # The tiling logic will handle replacing background 0s.
    # Let's try the simple extraction first.

    # Correction: The pattern should be defined by the non-boundary colors *within* the bbox.
    # If a cell inside the bbox in the original grid was 0 AND was identified
    # as an 'enclosed_zero', it should be treated as 0 in the pattern for tiling.
    # If it was a non-zero color (pattern color or boundary color that's internal), keep it.
    pattern_array = np.zeros((pattern_height, pattern_width), dtype=int)
    for r in range(pattern_height):
        for c in range(pattern_width):
            orig_r, orig_c = min_row + r, min_col + c
            # Check if this original coordinate was one of the identified pattern cells
            if (orig_r, orig_c) in potential_pattern_coords:
                 pattern_array[r, c] = grid[orig_r, orig_c]
            # Check if it's a zero *inside* the pattern bbox but *not* part of the main fill area
            elif grid[orig_r, orig_c] == 0 and (orig_r, orig_c) not in enclosed_zeros_set:
                 pattern_array[r, c] = 0 # Keep internal zeros if they exist
            elif grid[orig_r, orig_c] != 0 and grid[orig_r, orig_c] != boundary_color : # Keep other non-boundary colors if any exist
                pattern_array[r, c] = grid[orig_r, orig_c]


    # If the constructed pattern is all zeros (edge case?), return None
    if np.all(pattern_array == 0):
        return None, -1, -1


    return pattern_array, min_row, min_col


def transform(input_grid):
    """
    Transforms the grid by tiling an inner pattern onto the background
    area enclosed by a boundary shape.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    rows, cols = grid.shape

    # Find unique non-zero colors
    colors = [c for c in np.unique(grid) if c != 0]
    if not colors:
        return output_grid.tolist() # No non-zero colors

    # --- Determine Boundary Color ---
    # Heuristic: Boundary color is often the most frequent non-zero color,
    # or the one enclosing the largest '0' area.
    # Let's try each non-zero color as a potential boundary.
    best_boundary_color = -1
    max_enclosed_count = -1
    enclosed_zeros_map = {}
    reachable_mask_map = {}

    # Find enclosed zeros for each potential boundary color
    for color in colors:
        enclosed_coords, reachable_mask = _find_enclosed_background(grid, color)
        enclosed_zeros_map[color] = enclosed_coords
        reachable_mask_map[color] = reachable_mask
        if len(enclosed_coords) > max_enclosed_count:
            max_enclosed_count = len(enclosed_coords)
            best_boundary_color = color
        # Tie-breaking: if counts are equal, maybe prefer lower color index? (simple heuristic)
        elif len(enclosed_coords) == max_enclosed_count and best_boundary_color != -1 and color < best_boundary_color:
             best_boundary_color = color


    # If no enclosed zeros found for any color, return original grid
    if best_boundary_color == -1 or max_enclosed_count == 0:
        # One last check: maybe the boundary *is* the edge of the grid, and the pattern fills everything?
        # This seems unlikely based on examples. Let's assume a boundary color is needed.
        return output_grid.tolist()

    boundary_color = best_boundary_color
    enclosed_zeros_coords = enclosed_zeros_map[boundary_color]
    reachable_mask = reachable_mask_map[boundary_color]


    # --- Identify Inner Pattern ---
    pattern_array, min_row, min_col = _get_inner_pattern_and_bbox(grid, enclosed_zeros_coords, boundary_color, reachable_mask)

    # If no pattern identified, return original grid
    if pattern_array is None:
        return output_grid.tolist()

    pattern_height, pattern_width = pattern_array.shape
    if pattern_height == 0 or pattern_width == 0:
         return output_grid.tolist() # Invalid pattern dimensions


    # --- Tile the Pattern onto Enclosed Background Cells ---
    for r, c in enclosed_zeros_coords:
        # Calculate relative position within the pattern's tiling scheme
        rel_row = r - min_row
        rel_col = c - min_col

        # Find corresponding pattern cell using modulo
        pattern_row = rel_row % pattern_height
        pattern_col = rel_col % pattern_width

        # Get color from pattern
        pattern_color = pattern_array[pattern_row, pattern_col]

        # Update output grid ONLY if pattern color is not background
        if pattern_color != 0:
            output_grid[r, c] = pattern_color

    return output_grid.tolist()