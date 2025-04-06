```python
import collections

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms an input grid of 0s and 3s based on connectivity.
    - Zeros remain unchanged.
    - Threes that are part of a connected component (horizontally or vertically)
      of size 2 or more are changed to 8s.
    - Threes that are isolated (not connected to any other 3s) remain 3s.
    """

    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Initialize output_grid as a deep copy of the input grid
    # This handles the default cases: 0s stay 0, isolated 3s initially stay 3
    output_grid = [row[:] for row in input_grid]

    # Keep track of visited cells to avoid processing components multiple times
    visited = set()

    # Iterate through each cell in the grid
    for r in range(height):
        for c in range(width):
            # If the cell is a 3 and hasn't been visited yet, start exploring its component
            if input_grid[r][c] == 3 and (r, c) not in visited:
                
                # Initialize data structures for BFS
                component_cells = [] # Stores coordinates of cells in the current component
                queue = collections.deque([(r, c)]) # Queue for BFS
                
                # Mark the starting cell as visited and add to the component
                visited.add((r, c))
                component_cells.append((r, c))

                # Perform Breadth-First Search (BFS) to find the connected component
                while queue:
                    curr_r, curr_c = queue.popleft()

                    # Define potential neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check if the neighbor is within grid bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check if the neighbor is a 3 and hasn't been visited
                            if input_grid[nr][nc] == 3 and (nr, nc) not in visited:
                                # Mark neighbor as visited
                                visited.add((nr, nc))
                                # Add neighbor to the queue for further exploration
                                queue.append((nr, nc))
                                # Add neighbor to the current component list
                                component_cells.append((nr, nc))

                # After exploring the entire component, check its size
                if len(component_cells) >= 2:
                    # If the component size is 2 or more, change all its cells to 8 in the output grid
                    for cell_r, cell_c in component_cells:
                        output_grid[cell_r][cell_c] = 8
                # If the component size is 1, the cell value remains 3 (as initialized in the copy)

    # Return the final transformed grid
    return output_grid
```