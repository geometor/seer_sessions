import numpy as np
import collections

"""
The transformation identifies a primary closed boundary shape of one color. 
Inside this boundary, there exists a 'pattern' element (potentially multi-colored and including background 0s), defined by the content within the bounding box of specific non-boundary and 'internal' boundary elements found inside.
The core operation involves tiling this inner 'pattern' onto all background (color 0) cells that are strictly enclosed by the boundary shape. The original boundary and pattern elements remain unchanged in the output.

Workflow:
1.  Initialize: Create a copy of the input grid for the output.
2.  Identify Unique Colors: Find all non-zero colors present.
3.  Identify Boundary Color: For each unique non-zero color, tentatively assume it's the boundary. Calculate which color encloses the largest area of background ('0') cells using a reachability analysis (BFS from edges). The color maximizing this enclosed area is chosen as the `boundary_color`. Also obtain the coordinates of the `enclosed_zeros_coords` and the `reachable_mask` for this boundary color.
4.  Extract Inner Pattern:
    a. Identify candidate cells for the pattern: These are non-zero cells that are *not* reachable from the grid edge without crossing the `boundary_color`. This includes:
        i. Cells with a color different from the `boundary_color`.
        ii. Cells with the `boundary_color` that are determined to be 'internal' (i.e., not adjacent to any cell marked as reachable).
    b. Find the minimal bounding box containing all candidate pattern cells.
    c. Extract the rectangular subgrid defined by this bounding box from the *original input grid*. This is the `pattern_array`.
    d. Record the top-left coordinate (`min_row`, `min_col`) of the bounding box.
5.  Tile Pattern:
    a. Iterate through each coordinate `(r, c)` in `enclosed_zeros_coords`.
    b. Calculate corresponding indices `(pattern_row, pattern_col)` within the `pattern_array` using modulo arithmetic relative to the pattern's top-left corner (`min_row`, `min_col`).
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
    Uses BFS starting from edge '0' cells. Also computes a mask indicating
    all cells reachable from the edge without crossing the boundary color.

    Args:
        grid (np.array): The input grid.
        boundary_color (int): The color acting as the boundary.

    Returns:
        tuple: (list_of_enclosed_zeros, reachable_mask)
               list_of_enclosed_zeros: List of (row, col) tuples for enclosed background cells.
               reachable_mask: A boolean numpy array where True indicates a cell reachable
                               from edge without crossing boundary.
    """
    rows, cols = grid.shape
    # reachable_mask tracks cells reachable from the edge *without* crossing boundary_color
    reachable_mask = np.zeros_like(grid, dtype=bool)
    q = collections.deque()

    # Initialize queue ONLY with '0' cells on the edge
    for r in range(rows):
        for c in [0, cols - 1]:
            if grid[r, c] == 0 and not reachable_mask[r, c]:
                reachable_mask[r, c] = True
                q.append((r, c))
    for c in range(cols): # Check top/bottom edges (excluding corners already checked)
        for r in [0, rows - 1]:
             if grid[r, c] == 0 and not reachable_mask[r, c]:
                reachable_mask[r, c] = True
                q.append((r, c))

    # BFS exploring reachable areas (non-boundary cells)
    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check validity, reachability, and if it's not the boundary color
            if _is_valid(nr, nc, rows, cols) and \
               not reachable_mask[nr, nc] and \
               grid[nr, nc] != boundary_color:
                reachable_mask[nr, nc] = True
                q.append((nr, nc)) # Add all non-boundary reachable neighbors

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
    Returns the chosen color, the list of enclosed '0' coords, and the reachability mask.
    """
    best_boundary_color = -1
    max_enclosed_count = -1
    best_enclosed_zeros_for_boundary = []
    best_reachable_mask_for_boundary = None

    if not unique_colors:
        return best_boundary_color, best_enclosed_zeros_for_boundary, best_reachable_mask_for_boundary

    for color in unique_colors:
        enclosed_coords, reachable_mask = _find_enclosed_background(grid, color)
        count = len(enclosed_coords)

        # Primary criteria: maximize enclosed zeros
        if count > max_enclosed_count:
            max_enclosed_count = count
            best_boundary_color = color
            best_enclosed_zeros_for_boundary = enclosed_coords
            best_reachable_mask_for_boundary = reachable_mask
        # Tie-breaking: if counts are equal, prefer lower color index (consistent heuristic)
        elif count == max_enclosed_count and best_boundary_color != -1 and color < best_boundary_color:
            best_boundary_color = color
            best_enclosed_zeros_for_boundary = enclosed_coords
            best_reachable_mask_for_boundary = reachable_mask

    # Handle case where no color encloses any '0's, but colors exist
    # (e.g., solid shapes with no internal background)
    if best_boundary_color == -1 and unique_colors:
       # Fallback: Pick the lowest color index as boundary? Or most frequent?
       # Let's stick to lowest index for simplicity if no enclosure found.
       best_boundary_color = unique_colors[0]
       enclosed_coords, reachable_mask = _find_enclosed_background(grid, best_boundary_color)
       best_enclosed_zeros_for_boundary = enclosed_coords # Likely empty
       best_reachable_mask_for_boundary = reachable_mask

    return best_boundary_color, best_enclosed_zeros_for_boundary, best_reachable_mask_for_boundary


def _extract_inner_pattern(grid, boundary_color, reachable_mask):
    """
    Identifies and extracts the inner pattern based on non-reachable, non-zero cells.
    Includes non-boundary colors and 'internal' boundary-colored cells.
    """
    rows, cols = grid.shape
    pattern_candidate_coords = []

    # Iterate through all grid cells to find candidates for the pattern
    for r in range(rows):
        for c in range(cols):
            # Rule 1: Must be inside the unreachable area defined by the boundary
            if not reachable_mask[r, c]:
                # Rule 2: Must not be a background '0' cell (those are filled later)
                if grid[r, c] != 0:
                    # Rule 3: Identify if it's a potential pattern element
                    is_pattern_element = False
                    if grid[r, c] != boundary_color:
                        # It's a non-boundary color inside the unreachable area -> part of pattern
                        is_pattern_element = True
                    else: # It's a boundary-colored cell inside the unreachable area
                        # Check if it's truly 'internal' (not adjacent to any reachable cell)
                        is_internal_boundary = True
                        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            nr, nc = r + dr, c + dc
                            # If neighbor is valid AND reachable, this boundary cell is part of the 'wall'
                            if _is_valid(nr, nc, rows, cols) and reachable_mask[nr, nc]:
                                is_internal_boundary = False
                                break
                        if is_internal_boundary:
                            # Boundary-colored cell surrounded by non-reachable area -> part of pattern
                            is_pattern_element = True

                    if is_pattern_element:
                        pattern_candidate_coords.append((r,c))


    # If no pattern cells found (e.g., empty interior), return None
    if not pattern_candidate_coords:
        return None, -1, -1

    # Find the bounding box of the identified pattern candidate cells
    min_row = min(r for r, c in pattern_candidate_coords)
    max_row = max(r for r, c in pattern_candidate_coords)
    min_col = min(c for r, c in pattern_candidate_coords)
    max_col = max(c for r, c in pattern_candidate_coords)

    # Extract the pattern subgrid from the original input grid using the bounding box
    pattern_array = grid[min_row : max_row + 1, min_col : max_col + 1].copy()

    # Return the extracted pattern array and its top-left corner coordinates
    return pattern_array, min_row, min_col


def transform(input_grid):
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_grid = grid.copy()
    rows, cols = grid.shape

    # Find unique non-zero colors present in the grid
    unique_colors = sorted([c for c in np.unique(grid) if c != 0])

    # If no non-zero colors, return the original grid
    if not unique_colors:
        return output_grid.tolist()

    # Step 3: Identify Boundary Color and Enclosed Background Cells
    boundary_color, enclosed_zeros_coords, reachable_mask = _find_boundary_color(grid, unique_colors)

    # If no valid boundary color identified or no background cells are enclosed, return original
    if boundary_color == -1 or not enclosed_zeros_coords:
        return output_grid.tolist()

    # Step 4: Extract Inner Pattern
    pattern_array, min_row, min_col = _extract_inner_pattern(grid, boundary_color, reachable_mask)

    # If no pattern could be extracted (e.g., empty interior), return original grid
    if pattern_array is None:
        return output_grid.tolist()

    pattern_height, pattern_width = pattern_array.shape

    # Check for invalid pattern dimensions (should not happen if candidates were found)
    if pattern_height == 0 or pattern_width == 0:
         return output_grid.tolist()

    # Step 5: Tile the Pattern onto Enclosed Background Cells in the output grid
    for r, c in enclosed_zeros_coords:
        # Calculate the relative position of the cell (r, c) with respect to the pattern's origin
        rel_row = r - min_row
        rel_col = c - min_col

        # Determine the corresponding row and column within the pattern_array using modulo arithmetic
        # The addition of pattern dimension before modulo handles potential negative relative indices correctly
        pattern_row = (rel_row % pattern_height + pattern_height) % pattern_height
        pattern_col = (rel_col % pattern_width + pattern_width) % pattern_width

        # Get the color from the determined position in the pattern array
        pattern_color = pattern_array[pattern_row, pattern_col]

        # Update the output grid at (r, c) ONLY if the pattern color is not background (0)
        # This prevents overwriting existing non-zero elements with pattern's background
        if pattern_color != 0:
            output_grid[r, c] = pattern_color

    # Step 6: Return the modified grid as a list of lists
    return output_grid.tolist()