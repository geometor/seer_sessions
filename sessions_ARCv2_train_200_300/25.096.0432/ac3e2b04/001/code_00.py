"""
Transforms the input grid by identifying background cells (0) that are not connected 
to the grid's border via a path of other background cells. These unconnected 
background cells are then changed to 1. Cells with value 2 act as barriers, 
blocking the path connection. Cells with values 2 and 3 remain unchanged.
"""

import collections
import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the flood fill transformation rule.

    Args:
        input_grid: A 2D list representing the input grid.

    Returns:
        A 2D list representing the transformed output grid.
    """
    
    # Get grid dimensions
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)]

    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    
    # Create a visited grid to keep track of cells reachable from the border
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    
    # Initialize a queue for Breadth-First Search (BFS)
    queue = collections.deque()

    # Seed the BFS with all '0' cells on the border
    for r in range(rows):
        for c in range(cols):
            # Check if the cell is on the border
            if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                # Check if the cell is background (0) and not already visited
                if input_grid[r][c] == 0 and not visited[r][c]:
                    queue.append((r, c))
                    visited[r][c] = True

    # Define the four cardinal directions for neighbors
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Perform BFS to find all '0' cells connected to the border
    while queue:
        r, c = queue.popleft()

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor is background (0), not a barrier (2), and not visited
                if input_grid[nr][nc] != 2 and not visited[nr][nc]:
                    visited[nr][nc] = True
                    # Only continue the search from background cells
                    if input_grid[nr][nc] == 0:
                        queue.append((nr, nc))


    # Iterate through the grid and change unconnected '0's to '1's
    for r in range(rows):
        for c in range(cols):
            # If a cell is background (0) in the input but was not visited by the BFS
            if input_grid[r][c] == 0 and not visited[r][c]:
                # Change its value to 1 in the output grid
                output_grid[r][c] = 1

    return output_grid