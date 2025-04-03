```python
import collections
import numpy as np

"""
Identify non-zero 'target' cells within an input grid that are not part of the 
'boundary' layer directly adjacent to the outermost background (0-valued cells 
connected to the grid edge). Count these target cells. Generate an output list 
containing the digit '4' for each target cell found. Pad this list with '0's 
at the end until it reaches a fixed length of 7.
"""

def find_outer_background_and_boundary(grid):
    """
    Identifies the outermost background cells (0s connected to the edge)
    and the value of the boundary cells adjacent to them.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A tuple: (set of outer background coordinates, boundary_value).
        boundary_value is None if no boundary is found.
    """
    rows, cols = grid.shape
    outer_background = set()
    q = collections.deque()
    visited = set()

    # Add all border cells with value 0 to the queue and visited set
    for r in range(rows):
        for c in [0, cols - 1]:
            if grid[r, c] == 0 and (r, c) not in visited:
                q.append((r, c))
                visited.add((r, c))
                outer_background.add((r, c))
    for c in range(cols):
        for r in [0, rows - 1]:
             if grid[r, c] == 0 and (r, c) not in visited:
                q.append((r, c))
                visited.add((r, c))
                outer_background.add((r, c))

    # BFS to find all connected 0s from the border
    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and \
               grid[nr, nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                outer_background.add((nr, nc))
                q.append((nr, nc))

    # Find the boundary value by checking neighbors of the outer background
    boundary_value = None
    for r_bg, c_bg in outer_background:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r_bg + dr, c_bg + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] != 0:
                boundary_value = grid[nr, nc] # Assume first found is the boundary value
                return outer_background, boundary_value # Found boundary value, return early

    # If no non-zero neighbors found for any outer background cell
    return outer_background, None


def transform(input_grid):
    """
    Transforms the input grid into a fixed-length list based on counting target cells.

    Args:
        input_grid: A list of lists or numpy array representing the grid.

    Returns:
        A list of integers representing the output.
    """
    # Convert input to numpy array for easier processing
    grid = np.array(input_grid)
    rows, cols = grid.shape
    output_list = []
    fixed_length = 7
    target_count = 0

    # Identify outer background and the boundary value
    outer_background_coords, boundary_val = find_outer_background_and_boundary(grid)

    # If no boundary value is found (e.g., grid is all zeros or non-zeros aren't adjacent to outer background),
    # then treat all non-zeros as potential targets (though unlikely given problem structure)
    # or return all zeros if no boundary exists. Based on test case 2, if only one non-zero type exists
    # and it forms the boundary, there are no targets.
    if boundary_val is None:
         # Count all non-zeros if no clear boundary connected to outer background?
         # Or interpret as no targets possible if no boundary? Let's stick to the definition:
         # target is non-zero AND not boundary. If no boundary defined by adjacency,
         # check if only one non-zero number exists overall. If so, it MUST be boundary.
         unique_non_zeros = np.unique(grid[grid != 0])
         if len(unique_non_zeros) <= 1:
             # Grid is all zeros or only has one type of non-zero value (which must be the boundary)
             target_count = 0
         else:
              # This case is ambiguous based on examples. Let's assume targets exist only
              # if a boundary adjacent to outer background is identified.
              # Or, maybe count all non-zeros not equal to the *most frequent* non-zero?
              # Sticking to the spatial definition: If boundary_val is None, implies no boundary
              # adjacent to outer 0s, so definitionally no 'target' cells inside a boundary.
              target_count = 0

    else:
        # Count target cells: non-zero cells that are NOT the boundary value
        for r in range(rows):
            for c in range(cols):
                cell_value = grid[r, c]
                # Target is non-zero and not the boundary value
                if cell_value != 0 and cell_value != boundary_val:
                    target_count += 1

    # Build the initial part of the output list with '4's
    for _ in range(target_count):
        output_list.append(4)

    # Pad the output list with '0's to reach the fixed length
    while len(output_list) < fixed_length:
        output_list.append(0)

    # Ensure the list doesn't exceed the fixed length (truncate if necessary)
    output_list = output_list[:fixed_length]

    return output_list
```