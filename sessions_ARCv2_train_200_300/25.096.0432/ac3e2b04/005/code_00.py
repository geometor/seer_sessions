import collections
import copy

"""
Transforms the input grid based on connectivity from the border.
A flood fill (BFS) starts from all background cells (0) on the grid's border.
This fill propagates through adjacent background (0) and pattern (3) cells,
but is blocked by barrier (2) cells.
Any background cell (0) that is *not* reached by this fill is considered "enclosed".
These enclosed background cells (0) are changed to 1 in the output.
Additionally, any barrier cell (2) in the input that is adjacent (up, down, left, or right) 
to at least one of these enclosed background cells (0) is also changed to 1 in the output.
All other cells (border-connected 0s, all 3s, and 2s not adjacent to enclosed 0s) 
retain their original values.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the described transformation to the input grid.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed output grid.
    """
    
    # Get grid dimensions
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)]

    # 1. Flood Fill from Border
    # Initialize a visited grid to keep track of cells reachable from the border
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    # Initialize a queue for Breadth-First Search (BFS)
    queue = collections.deque()

    # Seed the BFS with all '0' cells on the border
    for r in range(rows):
        for c in range(cols):
            is_border = (r == 0 or r == rows - 1 or c == 0 or c == cols - 1)
            if is_border and input_grid[r][c] == 0 and not visited[r][c]:
                queue.append((r, c))
                visited[r][c] = True

    # Define directions for neighbors
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Perform BFS
    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            # Check bounds, barrier condition (not 2), and visited status
            if 0 <= nr < rows and 0 <= nc < cols and \
               input_grid[nr][nc] != 2 and not visited[nr][nc]:
                visited[nr][nc] = True
                queue.append((nr, nc)) # Continue BFS from this newly visited cell

    # 2. Identify Target 0s (Enclosed 0s)
    target_zeros = set()
    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] == 0 and not visited[r][c]:
                target_zeros.add((r, c))

    # 3. Identify Target 2s (Barrier cells adjacent to enclosed 0s)
    target_twos = set()
    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] == 2:
                # Check neighbors
                is_adjacent_to_target_zero = False
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    # Check bounds and if neighbor is in target_zeros
                    if 0 <= nr < rows and 0 <= nc < cols and \
                       (nr, nc) in target_zeros:
                        is_adjacent_to_target_zero = True
                        break # Found one adjacent target zero, no need to check more neighbors
                
                if is_adjacent_to_target_zero:
                    target_twos.add((r, c))

    # 4. Create Output Grid
    output_grid = copy.deepcopy(input_grid)

    # 5. Fill Target 0s
    for r, c in target_zeros:
        output_grid[r][c] = 1
        
    # 6. Fill Target 2s
    for r, c in target_twos:
        output_grid[r][c] = 1

    # 7. Return final grid
    return output_grid