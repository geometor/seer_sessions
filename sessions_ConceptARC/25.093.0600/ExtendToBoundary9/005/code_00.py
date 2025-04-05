import numpy as np
import collections

"""
The transformation identifies a primary closed boundary shape of one color. 
Inside this boundary, there exists a 'pattern' element (potentially multi-colored and including background 0s), defined by the content within the bounding box of specific non-boundary elements found inside.
The core operation involves tiling this inner 'pattern' onto all background (color 0) cells that are strictly enclosed by the boundary shape. The original boundary and pattern elements remain unchanged.

1.  Initialize: Create a copy of the input grid.
2.  Identify Boundary Color: Find the non-zero color that partitions the grid such that the largest connected component of '0' cells is not reachable from the grid edges without crossing this color.
3.  Identify Enclosed Background Cells: Perform a flood fill (BFS) starting from all '0' cells on the grid's edges. Mark all reachable '0' cells, without crossing the boundary color. Any '0' cell *not* marked is considered enclosed.
4.  Extract Inner Pattern:
    a. Identify all non-zero cells located within the region enclosed by the boundary (i.e., not reachable from the edge without crossing the boundary).
    b. Determine the minimal bounding box containing these enclosed non-zero cells.
    c. Extract the rectangular subgrid defined by this bounding box from the *original input grid*. This is the `pattern_array`.
    d. Record the top-left coordinate (`min_row`, `min_col`) of the bounding box as the `pattern_origin`.
5.  Tile Pattern:
    a. Iterate through each enclosed background cell coordinate `(r, c)`.
    b. Calculate corresponding indices `(pattern_row, pattern_col)` within the `pattern_array` using modulo arithmetic relative to the `pattern_origin`.
    c. Retrieve the `pattern_color` from `pattern_array[pattern_row, pattern_col]`.
    d. If `pattern_color` is not '0', update the cell in the *output grid* at `(r, c)` to this `pattern_color`.
6.  Return: The modified output grid.
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
        tuple: (list_of_enclosed_zeros, reachable_mask)
               list_of_enclosed_zeros: List of (row, col) tuples for enclosed background cells.
               reachable_mask: A boolean numpy array where True indicates a cell reachable from edge without crossing boundary.
    """
    rows, cols = grid.shape
    reachable_mask = np.zeros_like(grid, dtype=bool)
    q = collections.deque()

    # Add edge '0' cells to the queue and mark as reachable
    for r in range(rows):
        for c in [0, cols - 1]:
            if grid[r, c] == 0 and not reachable_mask[r, c]:
                reachable_mask[r, c] = True
                q.append((r, c))
            # Consider non-zero cells on edge as reachable for mask purpose
            elif grid[r, c] != 0 and not reachable_mask[r, c]:
                 reachable_mask[r,c] = True # Mark edge non-zeros as technically reachable

    for c in range(cols):
        for r in [0, rows - 1]:
             if grid[r, c] == 0 and not reachable_mask[r, c]:
                reachable_mask[r, c] = True
                q.append((r, c))
             elif grid[r, c] != 0 and not reachable_mask[r, c]:
                 reachable_mask[r,c] = True

    # BFS from edge zeros, cannot cross the boundary_color
    while q:
        r, c = q.popleft()
        # Explore neighbors only if the current cell is 0
        if grid[r, c] == 0:
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                # Check validity, reachability, and if it's not the boundary color
                if _is_valid(nr, nc, rows, cols) and \
                   not reachable_mask[nr, nc] and \
                   grid[nr, nc] != boundary_color:
                    reachable_mask[nr, nc] = True
                    # Only add '0' cells to the queue to continue BFS within connected '0' regions
                    if grid[nr, nc] == 0:
                        q.append((nr, nc))

    # Identify enclosed background cells (0s not reachable by the BFS)
    enclosed_zeros = []
    for r in range(rows):
        for c in range(cols):
            # A cell is enclosed if it's 0 AND not marked as reachable
            if grid[r, c] == 0 and not reachable_mask[r, c]:
                enclosed_zeros.append((r, c))

    return enclosed_zeros, reachable_mask

def _find_boundary_color(grid, unique_colors):
    """
    Determines the boundary color based on which color encloses the most '0' cells.
    """
    rows, cols = grid.shape
    best_boundary_color = -1
    max_enclosed_count = -1
    best_enclosed_zeros_for_boundary = []
    best_reachable_mask_for_boundary = None

    if not unique_colors:
        return best_boundary_color, best_enclosed_zeros_for_boundary, best_reachable_mask_for_boundary

    for color in unique_colors:
        enclosed_coords, reachable_mask = _find_enclosed_background(grid, color)
        count = len(enclosed_coords)

        if count > max_enclosed_count:
            max_enclosed_count = count
            best_boundary_color = color
            best_enclosed_zeros_for_boundary = enclosed_coords
            best_reachable_mask_for_boundary = reachable_mask
        # Tie-breaking: if counts are equal, prefer lower color index (arbitrary but consistent)
        elif count == max_enclosed_count and best_boundary_color != -1 and color < best_boundary_color:
            best_boundary_color = color
            best_enclosed_zeros_for_boundary = enclosed_coords
            best_reachable_mask_for_boundary = reachable_mask

    # Handle cases where no color truly encloses '0's (e.g., fully filled shapes)
    if best_boundary_color == -1 and len(unique_colors) > 0:
       # Fallback heuristic: maybe the most frequent color? or the one with largest extent?
       # For now, if no clear enclosure, pick the first color. This might need refinement.
       best_boundary_color = unique_colors[0]
       enclosed_coords, reachable_mask = _find_enclosed_background(grid, best_boundary_color)
       best_enclosed_zeros_for_boundary = enclosed_coords
       best_reachable_mask_for_boundary = reachable_mask


    return best_boundary_color, best_enclosed_zeros_for_boundary, best_reachable_mask_for_boundary


def _extract_inner_pattern(grid, boundary_color, reachable_mask):
    """
    Identifies and extracts the inner pattern based on non-reachable, non-zero cells.
    Handles cases where the pattern color might be the same as the boundary color but internal.
    """
    rows, cols = grid.shape
    pattern_candidate_coords = []

    # Identify all cells not reachable from the outside
    for r in range(rows):
        for c in range(cols):
            if not reachable_mask[r, c] and grid[r, c] != 0: # Find non-zero cells inside the unreachable area
                 # Check if it's truly internal (not part of the immediate boundary wall adjacent to reachable space)
                 is_internal = True
                 if grid[r,c] == boundary_color:
                      is_internal = False # Assume boundary color is part of wall unless proven otherwise
                      for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                         nr, nc = r + dr, c + dc
                         # If any neighbor is *not* reachable (and inside grid), it suggests this boundary cell is internal
                         if _is_valid(nr, nc, rows, cols) and not reachable_mask[nr, nc]:
                             is_internal = True
                             break
                 # Add if it's not the boundary color OR if it's an internal boundary color cell
                 if grid[r,c] != boundary_color or is_internal:
                    pattern_candidate_coords.append((r,c))


    if not pattern_candidate_coords:
        return None, -1, -1 # No pattern found

    # Find bounding box of the identified pattern cells
    min_row = min(r for r, c in pattern_candidate_coords)
    max_row = max(r for r, c in pattern_candidate_coords)
    min_col = min(c for r, c in pattern_candidate_coords)
    max_col = max(c for r, c in pattern_candidate_coords)

    # Extract the pattern from the original grid within the bounding box
    pattern_array = grid[min_row : max_row + 1, min_col : max_col + 1].copy()

    return pattern_array, min_row, min_col


def transform(input_grid):
    # Initialize output grid as a copy of the input
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    rows, cols = grid.shape

    # Find unique non-zero colors
    unique_colors = sorted([c for c in np.unique(grid) if c != 0])
    if not unique_colors:
        return output_grid.tolist() # No transformation if grid is all zeros

    # Identify Boundary Color and Enclosed Cells
    boundary_color, enclosed_zeros_coords, reachable_mask = _find_boundary_color(grid, unique_colors)

    # If no boundary color found or no enclosed zeros, return original
    if boundary_color == -1 or not enclosed_zeros_coords:
        return output_grid.tolist()

    # Extract Inner Pattern
    pattern_array, min_row, min_col = _extract_inner_pattern(grid, boundary_color, reachable_mask)

    # If no pattern identified, return original grid
    if pattern_array is None:
        return output_grid.tolist()

    pattern_height, pattern_width = pattern_array.shape
    if pattern_height == 0 or pattern_width == 0:
         return output_grid.tolist() # Invalid pattern dimensions

    # Tile the Pattern onto Enclosed Background Cells
    for r, c in enclosed_zeros_coords:
        # Calculate relative position within the pattern's tiling scheme
        # Ensure non-negative relative indices before modulo
        rel_row = r - min_row
        rel_col = c - min_col

        # Find corresponding pattern cell using modulo
        # Add pattern dimension before modulo to handle negative relative indices correctly
        pattern_row = (rel_row % pattern_height + pattern_height) % pattern_height
        pattern_col = (rel_col % pattern_width + pattern_width) % pattern_width


        # Get color from pattern
        pattern_color = pattern_array[pattern_row, pattern_col]

        # Update output grid ONLY if pattern color is not background (0)
        if pattern_color != 0:
            output_grid[r, c] = pattern_color

    return output_grid.tolist()