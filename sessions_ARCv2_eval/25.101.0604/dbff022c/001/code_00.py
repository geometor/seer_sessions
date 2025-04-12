import copy
import collections

"""
Identifies connected components (shapes) of identical non-zero digits in the input grid.
For each shape, it determines if it encloses any regions of zeros (interior zeros).
An interior zero region is one that cannot reach the grid boundary by moving only through other zeros.
If a shape encloses interior zeros, a fill color is determined based on the shape's border color (C):
- C=3 -> Fill=3
- C=7 -> Fill=7
- C=8 -> Fill=1
- C=2 -> Fill=7
- C=4 -> Fill depends on the minimum border color (min_obd) of *other* shapes in the grid:
    - If min_obd=5, Fill=5
    - If min_obd=3, Fill=6
    - Otherwise, no fill.
- C=5 (or others) -> No fill.
The identified interior zero cells are then filled with the determined fill color in the output grid.
Cells not part of an enclosed zero region remain unchanged.
"""

def find_shapes(grid: list[list[int]]) -> list[dict]:
    """
    Finds all connected components of identical non-zero digits.

    Args:
        grid: The input grid.

    Returns:
        A list of dictionaries, where each dictionary represents a shape
        and contains 'color' (the digit) and 'cells' (a set of (row, col) tuples).
    """
    rows = len(grid)
    cols = len(grid[0])
    visited = set()
    shapes = []

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0 and (r, c) not in visited:
                color = grid[r][c]
                shape_cells = set()
                q = collections.deque([(r, c)])
                visited.add((r, c))
                shape_cells.add((r, c))

                while q:
                    row, col = q.popleft()
                    # Check orthogonal and diagonal neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               (nr, nc) not in visited and grid[nr][nc] == color:
                                visited.add((nr, nc))
                                shape_cells.add((nr, nc))
                                q.append((nr, nc))
                shapes.append({'color': color, 'cells': shape_cells})
    return shapes

def find_interior_zeros(grid: list[list[int]], shape_cells: set) -> set:
    """
    Finds zero cells that are enclosed by the given shape.

    Args:
        grid: The input grid.
        shape_cells: A set of (row, col) tuples representing the cells of a single shape.

    Returns:
        A set of (row, col) tuples representing the interior zero cells enclosed by the shape.
    """
    rows = len(grid)
    cols = len(grid[0])
    potential_interior = set()
    q = collections.deque()
    visited_zeros = set() # Zeros visited during any BFS starting from shape adjacency

    # 1. Find initial zero neighbors of the shape
    for r_s, c_s in shape_cells:
        # Only check orthogonal neighbors for starting the zero search
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r_s + dr, c_s + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                    potential_interior.add((nr, nc))

    interior_zeros = set()

    # 2. For each connected component of potential interior zeros, check if it reaches the boundary
    for r_init, c_init in potential_interior:
        if (r_init, c_init) in visited_zeros:
            continue

        component_zeros = set()
        q_zeros = collections.deque([(r_init, c_init)])
        visited_zeros.add((r_init, c_init))
        component_zeros.add((r_init, c_init))
        reaches_boundary = False

        while q_zeros:
            r, c = q_zeros.popleft()

            # Check if this zero touches the boundary
            if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                reaches_boundary = True
                # Optimization: if one cell reaches boundary, the whole component does.
                # No need to break here, let the BFS complete to mark all visited.

            # Explore neighbors (orthogonal only for zero-path finding)
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and \
                   grid[nr][nc] == 0 and (nr, nc) not in visited_zeros:
                    visited_zeros.add((nr, nc))
                    component_zeros.add((nr, nc))
                    q_zeros.append((nr, nc))

        # If the component did not reach the boundary, add its cells to interior_zeros
        if not reaches_boundary:
            interior_zeros.update(component_zeros)

    return interior_zeros


def determine_fill_color(shape_color: int, all_shapes: list[dict], current_shape_cells: set) -> int | None:
    """
    Determines the fill color based on the shape's color and other shapes present.

    Args:
        shape_color: The color (digit) of the current shape.
        all_shapes: A list of all shapes found in the grid.
        current_shape_cells: The cells of the current shape (to exclude it when finding 'other' shapes).

    Returns:
        The fill color (int) or None if no fill should occur.
    """
    if shape_color == 3:
        return 3
    if shape_color == 7:
        return 7
    if shape_color == 8:
        return 1
    if shape_color == 2:
        return 7
    if shape_color == 4:
        other_border_colors = set()
        for shape in all_shapes:
            # Check if it's a different shape instance
            if shape['cells'] != current_shape_cells:
                 other_border_colors.add(shape['color'])

        if not other_border_colors:
            return None # No other shapes

        min_obd = min(other_border_colors)
        if min_obd == 5:
            return 5
        if min_obd == 3:
            return 6
        else:
            return None # Min other border color is not 5 or 3
    # Default case (includes C=5 and any other unspecified colors)
    return None


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by identifying shapes, finding their enclosed
    interior zeros, determining the correct fill color based on specific rules,
    and filling those zeros.

    Args:
        input_grid: The 2D list representing the input grid.

    Returns:
        A new 2D list representing the transformed grid.
    """
    # initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    if not input_grid or not input_grid[0]:
        return output_grid # Handle empty grid case
    rows = len(input_grid)
    cols = len(input_grid[0])

    # 1. Identify all shapes in the grid
    all_shapes = find_shapes(input_grid)

    # 2. Process each shape
    for shape in all_shapes:
        shape_color = shape['color']
        shape_cells = shape['cells']

        # 3. Find interior zeros for the current shape
        # Need to pass the original grid state for finding zeros correctly
        interior_zeros = find_interior_zeros(input_grid, shape_cells)

        if not interior_zeros:
            continue # No interior zeros for this shape

        # 4. Determine the fill color
        fill_color = determine_fill_color(shape_color, all_shapes, shape_cells)

        # 5. Fill the interior zeros in the output grid if a fill color was determined
        if fill_color is not None:
            for r, c in interior_zeros:
                # Ensure we only fill actual zeros (safety check)
                if output_grid[r][c] == 0:
                     output_grid[r][c] = fill_color

    return output_grid