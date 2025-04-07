```python
import copy
from collections import deque

"""
Transforms an input grid by performing a flood fill operation.
The fill originates from the background cells (value 0) that are adjacent 
(up, down, left, right) to marker cells (value 6).
The fill color is 3.
The fill propagates only through background cells (value 0) and stops 
when it encounters grid boundaries or cells that are not background cells 
(e.g., original boundary cells with value 3, marker cells with value 6, or 
cells already filled during the process).
The original marker cells (6) and boundary cells (3) are preserved.
"""

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
    if rows == 0:
        return
    cols = len(grid[0])
    if cols == 0:
        return

    # Check if the starting point is valid and is the target color
    if not (0 <= start_row < rows and 0 <= start_col < cols and grid[start_row][start_col] == target_color):
        return

    q = deque([(start_row, start_col)])
    # Mark the starting cell immediately only if it's the target color
    # This check is already done above, but included for clarity in the queue setup
    grid[start_row][start_col] = fill_color 

    while q:
        r, c = q.popleft()

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor is the target color 
                if grid[nr][nc] == target_color:
                    # Change color to fill_color
                    grid[nr][nc] = fill_color
                    # Add neighbor to the queue to process its neighbors
                    q.append((nr, nc))
                # The fill naturally stops if grid[nr][nc] is not target_color (e.g., it's a boundary, a marker, or already filled)


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a flood fill originating from neighbors of marker cells (value 6)
    to fill background cells (value 0) with color 3, stopping at non-background cells.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed grid.
    """
    # Initialize output_grid as a deep copy of the input to avoid modifying the original
    output_grid = copy.deepcopy(input_grid)
    
    rows = len(output_grid)
    if rows == 0:
        return output_grid
    cols = len(output_grid[0])
    if cols == 0:
        return output_grid

    # Define colors
    marker_color = 6
    fill_color = 3
    target_color = 0
    # boundary_color = 3 is implicitly handled as it's not the target_color

    # 1. Find all marker cell locations
    marker_locations = []
    for r in range(rows):
        for c in range(cols):
            if output_grid[r][c] == marker_color:
                marker_locations.append((r, c))

    # 2. For each marker, identify adjacent target cells and initiate flood fill from them
    # Store potential start points to avoid starting multiple fills in the same connected component from the same marker
    potential_starts = set()
    for r_marker, c_marker in marker_locations:
        # Check neighbors of the marker
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r_marker + dr, c_marker + dc
            # Check if neighbor is within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                 # If the neighbor is a target cell (0), add it as a potential start point
                 if output_grid[nr][nc] == target_color:
                     potential_starts.add((nr, nc))

    # 3. Perform flood fill from each unique potential start point identified
    # This loop iterates over the set, so even if multiple markers point to the same 
    # starting '0' cell, the fill from that cell only happens once.
    for r_start, c_start in potential_starts:
         # Important: Check if the start cell hasn't already been filled by a previous fill operation
         # originating from a different marker's neighbor but within the same connected component.
         if output_grid[r_start][c_start] == target_color:
             _flood_fill(output_grid, r_start, c_start, fill_color, target_color)

    # 4. Return the modified grid
    return output_grid
```