import copy
from collections import deque

"""
Transforms a 2D grid of integers based on connected components of non-7 values.

The transformation identifies connected components (4-directional adjacency) of identical 
numbers (excluding 7). The transformation applied to each component depends on its 
original value, size (number of cells), and the count of its unique neighboring cells 
(adjacent cells not part of the component).

Rules:
1. Cells with value 7 remain 7.
2. Components of non-6 values:
   - If size is 1, change value to 7.
   - If size > 1, keep the original value.
3. Components of value 6:
   - Size 2: Change value to 3.
   - Size 4 & Neighbor Count 5: Keep value 6.
   - Size 4 & Neighbor Count 6: Change value to 1.
   - Size 5: Change value to 4.
   - All other sizes (1, 3) or other Size 4 neighbor counts: Keep value 6.
"""

def _find_component_and_neighbors(start_r: int, start_c: int, grid: list[list[int]], visited: list[list[bool]]) -> tuple[list[tuple[int, int]], int, set[tuple[int, int]]]:
    """
    Finds a connected component and its unique neighbors using BFS.

    Args:
        start_r: Starting row index.
        start_c: Starting column index.
        grid: The input grid.
        visited: A grid tracking visited cells.

    Returns:
        A tuple containing:
        - list[(int, int)]: Coordinates of cells in the component.
        - int: The common value of the component's cells.
        - set[(int, int)]: Coordinates of unique neighbor cells.
    """
    rows = len(grid)
    cols = len(grid[0])
    component_value = grid[start_r][start_c]
    component_cells = []
    neighbor_cells = set()
    q = deque([(start_r, start_c)])
    visited[start_r][start_c] = True

    while q:
        r, c = q.popleft()
        component_cells.append((r, c))

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # If neighbor is part of the component and not visited
                if not visited[nr][nc] and grid[nr][nc] == component_value:
                    visited[nr][nc] = True
                    q.append((nr, nc))
                # If neighbor has a different value, it's a neighbor cell
                elif grid[nr][nc] != component_value:
                    neighbor_cells.add((nr, nc))
            # Neighbors outside bounds are not counted

    return component_cells, component_value, neighbor_cells


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # Handle empty grid case
    if not input_grid or not input_grid[0]:
        return []

    rows = len(input_grid)
    cols = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    # Initialize visited grid to keep track of processed cells
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Skip if cell is background (7) or already part of a processed component
            if input_grid[r][c] == 7 or visited[r][c]:
                continue

            # Found an unvisited, non-7 cell: find its component and neighbors
            component_cells, component_value, neighbor_cells = _find_component_and_neighbors(r, c, input_grid, visited)
            
            # Calculate component size and neighbor count
            component_size = len(component_cells)
            neighbor_count = len(neighbor_cells)

            # Determine the new value based on component properties
            new_value = component_value # Default to original value

            if component_value != 6:
                if component_size == 1:
                    new_value = 7 # Isolated non-6 becomes 7
                # else: keep original value (implicit default for size > 1)
            elif component_value == 6:
                # Apply size/neighbor-based rules for value 6
                if component_size == 2:
                    new_value = 3
                elif component_size == 4:
                    if neighbor_count == 5:
                        new_value = 6 # Size 4, 5 neighbors -> 6
                    elif neighbor_count == 6:
                        new_value = 1 # Size 4, 6 neighbors -> 1
                    else: # Other neighbor counts for size 4
                        new_value = 6 # Default for size 4
                elif component_size == 5:
                    new_value = 4
                else: # Covers sizes 1, 3, and > 5 for value 6
                    new_value = 6 # Default to 6 for other sizes

            # Update the output grid for all cells in the current component
            for cell_r, cell_c in component_cells:
                output_grid[cell_r][cell_c] = new_value

    # Return the fully transformed grid
    return output_grid