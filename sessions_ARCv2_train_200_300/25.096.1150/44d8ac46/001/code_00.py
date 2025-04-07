import copy
import collections

"""
Identifies connected regions of '0' cells within a 2D grid. 
If a region of '0's is not connected to the grid boundary (i.e., it's fully enclosed by '5's or other grid contents), 
all '0's within that specific region are changed to '2's. 
Cells with value '5' remain unchanged. '0' regions that touch the boundary remain '0'.
"""

def find_region_and_check_boundary(start_r: int, start_c: int, grid: list[list[int]], visited: list[list[bool]]) -> tuple[set[tuple[int, int]], bool]:
    """
    Performs a Breadth-First Search (BFS) starting from (start_r, start_c) 
    to find a connected region of 0s.

    Args:
        start_r: The starting row index.
        start_c: The starting column index.
        grid: The input grid.
        visited: A grid of booleans to track visited cells.

    Returns:
        A tuple containing:
        - region_cells: A set of (row, col) tuples belonging to the found region.
        - touches_boundary: A boolean indicating if any cell in the region touches the grid boundary.
    """
    rows = len(grid)
    cols = len(grid[0])
    region_cells = set()
    touches_boundary = False
    q = collections.deque([(start_r, start_c)])

    # Mark the starting cell as visited and add it to the region
    visited[start_r][start_c] = True
    region_cells.add((start_r, start_c))

    # Define possible moves (up, down, left, right)
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while q:
        r, c = q.popleft()

        # Check if the current cell is on the boundary
        if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
            touches_boundary = True  # Mark if the region reaches the edge

        # Explore neighbors
        for dr, dc in moves:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor is a '0' and hasn't been visited yet
                if grid[nr][nc] == 0 and not visited[nr][nc]:
                    visited[nr][nc] = True
                    region_cells.add((nr, nc))
                    q.append((nr, nc))

    return region_cells, touches_boundary


def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Transforms the input grid by filling enclosed regions of '0's with '2's.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed grid.
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
    
    # Initialize visited grid to keep track of explored cells
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # If we find an unvisited '0', start exploring its region
            if input_grid[r][c] == 0 and not visited[r][c]:
                # Find the connected region of 0s and check if it touches the boundary
                region_cells, touches_boundary = find_region_and_check_boundary(r, c, input_grid, visited)
                
                # If the region does NOT touch the boundary, it's enclosed
                if not touches_boundary:
                    # Fill the enclosed region with '2's in the output grid
                    for rr, cc in region_cells:
                        output_grid[rr][cc] = 2
                        
    # Return the modified grid
    return output_grid