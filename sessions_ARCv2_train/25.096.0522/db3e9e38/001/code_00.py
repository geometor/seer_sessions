"""
Transforms an input grid by finding the topmost '7', treating it as a seed,
and performing a Breadth-First Search (BFS) propagation. During the BFS,
the values 7 and 8 alternate layer by layer, starting with 7 at the seed.
The propagation overwrites the grid cells with these alternating values.
"""

import collections

def find_seed(grid: list[list[int]]) -> tuple[int, int] | None:
    """Finds the coordinates (row, col) of the topmost '7' in the grid."""
    rows = len(grid)
    if rows == 0:
        return None
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 7:
                return (r, c)
    return None # No seed found

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Performs the BFS propagation transformation.

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

    # Find the seed location (topmost '7')
    seed_coords = find_seed(input_grid)

    # If no seed is found, return the initialized grid
    if seed_coords is None:
        return output_grid

    seed_row, seed_col = seed_coords

    # Initialize BFS queue and visited set
    # The queue stores tuples of (row, col, value)
    queue = collections.deque()
    visited = set()

    # Start BFS from the seed cell
    start_value = 7
    output_grid[seed_row][seed_col] = start_value
    queue.append((seed_row, seed_col, start_value))
    visited.add((seed_row, seed_col))

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