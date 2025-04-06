```python
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
to at least one of these enclosed background cells (originally 0, now becoming 1) is also changed to 1 in the output.
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

    # --- Step 1: Flood Fill from Border ---
    # Initialize a grid to keep track of cells reachable from the border
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    # Initialize a queue for Breadth-First Search (BFS)
    queue = collections.deque()

    # Seed the BFS queue with all '0' cells located on the grid's border
    for r in range(rows):
        for c in range(cols):
            # Check if the cell is on the border
            is_border = (r == 0 or r == rows - 1 or c == 0 or c == cols - 1)
            # If it's a border cell, is background (0), and hasn't been visited yet
            if is_border and input_grid[r][c] == 0 and not visited[r][c]:
                queue.append((r, c)) # Add to queue for BFS
                visited[r][c] = True # Mark as visited (reachable from border)

    # Define the four cardinal directions for exploring neighbors
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Perform the BFS to find all cells reachable from border '0's
    while queue:
        r, c = queue.popleft() # Get the next cell to explore from

        # Explore neighbors in the four cardinal directions
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor is NOT a barrier (value 2)
                # Check if the neighbor has NOT been visited yet
                if input_grid[nr][nc] != 2 and not visited[nr][nc]:
                    # Mark the neighbor as visited (reachable)
                    visited[nr][nc] = True
                    # Add the neighbor to the queue to continue the search from it
                    # Note: The search propagates through both 0s and 3s if they aren't barriers
                    queue.append((nr, nc))

    # --- Step 2: Identify Target 0s (Enclosed Background Cells) ---
    # Create a set to store the coordinates of enclosed '0' cells
    target_zeros = set()
    for r in range(rows):
        for c in range(cols):
            # If a cell is background (0) in the input AND was NOT visited by the BFS
            if input_grid[r][c] == 0 and not visited[r][c]:
                # It's an enclosed '0', add its coordinates to the set
                target_zeros.add((r, c))

    # --- Step 3: Identify Target 2s (Barrier cells adjacent to enclosed 0s) ---
    # Create a set to store the coordinates of barrier cells that need changing
    target_twos = set()
    for r in range(rows):
        for c in range(cols):
            # Consider only barrier cells (value 2)
            if input_grid[r][c] == 2:
                # Check its neighbors to see if any are enclosed '0's
                is_adjacent_to_target_zero = False
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    # Check if the neighbor is within bounds AND its coordinates are in the target_zeros set
                    if 0 <= nr < rows and 0 <= nc < cols and \
                       (nr, nc) in target_zeros:
                        is_adjacent_to_target_zero = True
                        break # Found an adjacent enclosed zero, no need to check other neighbors

                # If this barrier cell was adjacent to at least one enclosed '0'
                if is_adjacent_to_target_zero:
                    # Add its coordinates to the target_twos set
                    target_twos.add((r, c))

    # --- Step 4: Create and Modify Output Grid ---
    # Start with a copy of the input grid. This preserves original 3s, border-connected 0s, and non-adjacent 2s.
    output_grid = copy.deepcopy(input_grid)

    # Modify the enclosed '0's
    for r, c in target_zeros:
        output_grid[r][c] = 1 # Change value to 1
        
    # Modify the adjacent '2's
    for r, c in target_twos:
        output_grid[r][c] = 1 # Change value to 1

    # --- Step 5: Return the Result ---
    return output_grid
```