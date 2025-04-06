```python
"""
Transforms an input grid by identifying all cells containing '7' as seeds.
These seed cells are marked as '7' in the output grid. A Breadth-First
Search (BFS) propagates outwards from all seeds simultaneously. Orthogonal
neighbors of '7' cells are marked '8', and neighbors of '8' cells are
marked '7'. The propagation only affects cells not yet visited, starting
from an initial grid of zeros.
"""

import collections

def find_all_seeds(grid: list[list[int]]) -> list[tuple[int, int]]:
    """Finds the coordinates (row, col) of all '7's in the grid."""
    seeds = []
    rows = len(grid)
    if rows == 0:
        return seeds
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 7:
                seeds.append((r, c))
    return seeds

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Performs the BFS propagation transformation from all seed locations.

    Args:
        input_grid: The input 2D list of integers.

    Returns:
        The transformed 2D list of integers.
    """
    # Get grid dimensions
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
         return [[] for _ in range(rows)] # Return grid of empty rows if cols is 0

    # Initialize output_grid with zeros
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Find all seed locations ('7's in the input)
    seed_locations = find_all_seeds(input_grid)

    # If no seeds are found, return the initialized grid
    if not seed_locations:
        return output_grid

    # Initialize BFS queue and visited set
    # The queue stores tuples of (row, col, value)
    queue = collections.deque()
    visited = set()

    # Initialize the BFS with all seed locations
    for r, c in seed_locations:
        start_value = 7
        if (r, c) not in visited: # Ensure seeds aren't added multiple times if input has duplicates? (Unlikely based on examples, but safe)
            output_grid[r][c] = start_value
            queue.append((r, c, start_value))
            visited.add((r, c))

    # Perform BFS propagation
    while queue:
        current_row, current_col, current_value = queue.popleft()

        # Determine the value for neighbors (alternating 7 and 8)
        next_value = 8 if current_value == 7 else 7

        # Define orthogonal neighbor directions (up, down, left, right)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # Explore neighbors
        for dr, dc in directions:
            neighbor_row, neighbor_col = current_row + dr, current_col + dc

            # Check if the neighbor is within grid bounds
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                # Check if the neighbor has not been visited
                if (neighbor_row, neighbor_col) not in visited:
                    # Update the output grid with the next value
                    output_grid[neighbor_row][neighbor_col] = next_value
                    # Mark the neighbor as visited
                    visited.add((neighbor_row, neighbor_col))
                    # Add the neighbor to the queue for further exploration
                    queue.append((neighbor_row, neighbor_col, next_value))

    return output_grid
```