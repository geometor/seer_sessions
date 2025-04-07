import copy
from collections import deque

"""
Transforms an input grid based on the following rules:
1. Identify marker cells (value 6).
2. Filter these markers to find "active" markers, which are those adjacent (up, down, left, right) to at least one boundary cell (value 3).
3. Identify potential fill start cells: these are background cells (value 0) that are adjacent to any active marker cell.
4. For each unique potential fill start cell, if it hasn't already been filled, initiate a flood fill operation.
5. The flood fill uses color 3, starts from the identified background cell, and propagates through adjacent background cells (value 0).
6. The fill stops at grid boundaries or any cell that is not a background cell (value 0).
7. The original marker cells (6) and boundary cells (3) retain their values.
"""

def _is_valid(r, c, rows, cols):
    """Check if coordinates are within grid bounds."""
    return 0 <= r < rows and 0 <= c < cols

def _find_cells(grid, color):
    """Find all cells with a specific color."""
    locations = []
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == color:
                locations.append((r, c))
    return locations

def _is_adjacent_to(grid, r, c, target_color):
    """Check if the cell at (r, c) is adjacent to any cell with target_color."""
    rows = len(grid)
    cols = len(grid[0])
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if _is_valid(nr, nc, rows, cols) and grid[nr][nc] == target_color:
            return True
    return False

def _flood_fill(grid: list[list[int]], start_row: int, start_col: int, fill_color: int, target_color: int):
    """
    Performs a flood fill on the grid starting from (start_row, start_col).
    Modifies the grid in place.

    Args:
        grid: The grid to modify (list of lists of ints).
        start_row: The starting row index for the fill.
        start_col: The starting column index for the fill.
        fill_color: The color to fill with.
        target_color: The color of cells to be filled.
    """
    rows = len(grid)
    cols = len(grid[0])

    # Check if the starting point itself is the target color. 
    # This should always be true based on how it's called in transform, but good practice.
    if not _is_valid(start_row, start_col, rows, cols) or grid[start_row][start_col] != target_color:
        return

    q = deque([(start_row, start_col)])
    grid[start_row][start_col] = fill_color # Fill the starting cell

    while q:
        r, c = q.popleft()

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds and if the neighbor is the target color
            if _is_valid(nr, nc, rows, cols) and grid[nr][nc] == target_color:
                # Change color to fill_color
                grid[nr][nc] = fill_color
                # Add neighbor to the queue
                q.append((nr, nc))

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Handle empty grid case
    if not input_grid or not input_grid[0]:
        return []

    # Initialize output_grid as a deep copy
    output_grid = copy.deepcopy(input_grid)
    rows = len(output_grid)
    cols = len(output_grid[0])

    # Define colors
    marker_color = 6
    boundary_color = 3
    background_color = 0
    fill_color = 3 # Fill uses the boundary color

    # 1. Find all marker cells
    all_marker_locations = _find_cells(output_grid, marker_color)

    # 2. Filter for active markers (adjacent to a boundary cell)
    active_marker_locations = []
    for r_marker, c_marker in all_marker_locations:
        if _is_adjacent_to(output_grid, r_marker, c_marker, boundary_color):
            active_marker_locations.append((r_marker, c_marker))

    # 3. Identify potential fill start cells (background cells adjacent to active markers)
    potential_starts = set()
    for r_marker, c_marker in active_marker_locations:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r_marker + dr, c_marker + dc
            # Check if neighbor is valid and is a background cell
            if _is_valid(nr, nc, rows, cols) and output_grid[nr][nc] == background_color:
                potential_starts.add((nr, nc))

    # 4. Perform flood fill from each unique potential start point
    for r_start, c_start in potential_starts:
        # Check if the cell hasn't already been filled by another fill process
        if output_grid[r_start][c_start] == background_color:
            _flood_fill(output_grid, r_start, c_start, fill_color, background_color)

    # 5. Return the modified grid
    return output_grid