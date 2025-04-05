```python
import numpy as np
from collections import deque

# Helper function to find connected components using Breadth-First Search (BFS)
def _find_connected_island(grid, start_row, start_col, visited):
    """
    Performs BFS starting from (start_row, start_col) to find a connected island of 5s.
    Marks visited cells within the island.

    Args:
        grid (np.array): The input grid.
        start_row (int): The starting row index.
        start_col (int): The starting column index.
        visited (np.array): A boolean array tracking visited cells.

    Returns:
        tuple: A tuple containing:
            - list: A list of (row, col) tuples representing the cells in the found island.
            - int: The number of cells in the island (island size).
    """
    rows, cols = grid.shape
    # Check if starting point is valid for starting a search
    if not (0 <= start_row < rows and 0 <= start_col < cols) or \
       visited[start_row, start_col] or \
       grid[start_row, start_col] != 5:
        return [], 0 # Return empty if start is invalid, visited, or not a 5

    q = deque([(start_row, start_col)]) # Initialize queue with the starting cell
    island_cells = [] # To store coordinates of cells in this island
    visited[start_row, start_col] = True # Mark the starting cell as visited

    # Standard BFS loop
    while q:
        r, c = q.popleft() # Get the next cell to process
        island_cells.append((r, c)) # Add it to the current island

        # Explore 4-directional neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor is a '5' and has not been visited yet
                if not visited[nr, nc] and grid[nr, nc] == 5:
                    visited[nr, nc] = True # Mark neighbor as visited
                    q.append((nr, nc)) # Add neighbor to the queue

    return island_cells, len(island_cells)


def transform(input_grid_list):
    """
    Transforms the input grid based on connected components of '5's.
    Finds all connected components (islands) of cells containing '5', using 4-way adjacency.
    If a connected component contains 2 or more cells, all '5's within that component are changed to '2's.
    Components with only one '5' remain unchanged. Cells containing '0' remain unchanged.

    Args:
        input_grid_list (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_grid = np.array(input_grid_list, dtype=int)
    rows, cols = input_grid.shape

    # Create a copy of the input grid to modify as the output grid
    output_grid = np.copy(input_grid)

    # Create a boolean grid to keep track of visited cells during island finding
    visited = np.zeros_like(input_grid, dtype=bool)

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell contains a '5' and has not been visited yet
            if input_grid[r, c] == 5 and not visited[r, c]:
                # If an unvisited '5' is found, start BFS to find the island it belongs to
                island_cells, island_size = _find_connected_island(input_grid, r, c, visited)

                # Check if the found island has a size of 2 or more
                if island_size >= 2:
                    # If the island size is >= 2, change all '5's in this island to '2's in the output grid
                    for ir, ic in island_cells:
                        output_grid[ir, ic] = 2
            # If cell is 0 or already visited, continue to the next cell

    # Convert the final NumPy array back to a list of lists for the required output format
    return output_grid.tolist()
```