```python
"""
Transforms the grid by performing a flood fill starting from cells with value 3.
The fill spreads to adjacent cells (up, down, left, right) with value 7.
The spread is blocked by cells with value 8 (as they are not value 7) and by the grid boundaries.
Cells initially containing 3 remain 3. Cells initially containing 8 remain 8.
Cells initially containing 7 are changed to 3 if they are reachable from an initial 3 cell
through a path of adjacent 7s. Otherwise, they remain 7.
"""

import copy
from collections import deque

def find_source_cells(grid: list[list[int]], source_value: int) -> list[tuple[int, int]]:
    """Finds all cells with the specified source value."""
    sources = []
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == source_value:
                sources.append((r, c))
    return sources

def is_valid(r: int, c: int, rows: int, cols: int) -> bool:
    """Checks if coordinates are within grid boundaries."""
    return 0 <= r < rows and 0 <= c < cols

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a flood fill transformation to the input grid.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed grid.
    """
    # Handle empty input grid case gracefully
    if not input_grid or not input_grid[0]:
        return []

    rows = len(input_grid)
    cols = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input grid.
    # We modify this grid while checking conditions against the original input_grid.
    output_grid = copy.deepcopy(input_grid)

    # Define the key values involved in the transformation
    source_value = 3
    fillable_value = 7
    # barrier_value = 8 is implicitly handled because the fill only targets fillable_value (7)

    # Find the coordinates of all initial source cells (value 3)
    source_cells = find_source_cells(input_grid, source_value)

    # Initialize a queue for Breadth-First Search (BFS) starting from source cells
    queue = deque(source_cells)

    # Initialize a set to keep track of visited cells (cells added to the queue or already processed).
    # Start with the source cells as visited.
    visited = set(source_cells)

    # Define the four possible moves to adjacent cells (up, down, left, right)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Perform the flood fill using BFS
    while queue:
        # Get the next cell coordinates from the front of the queue
        r, c = queue.popleft()

        # Explore the four adjacent neighbors
        for dr, dc in moves:
            nr, nc = r + dr, c + dc # Calculate neighbor coordinates

            # Check if the neighbor is a valid target for filling:
            # 1. Must be within the grid boundaries.
            # 2. Must not have been visited/queued before.
            # 3. Must have the 'fillable_value' (7) in the *original* input grid.
            if is_valid(nr, nc, rows, cols) and \
               (nr, nc) not in visited and \
               input_grid[nr][nc] == fillable_value:

                # If conditions are met:
                # 1. Mark the neighbor cell as visited.
                visited.add((nr, nc))
                # 2. Change the neighbor's value to the 'source_value' (3) in the output grid.
                output_grid[nr][nc] = source_value
                # 3. Add the neighbor's coordinates to the queue to continue the spread from this cell.
                queue.append((nr, nc))

    # Return the modified grid after the flood fill is complete
    return output_grid
```