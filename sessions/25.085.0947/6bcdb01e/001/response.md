```python
"""
Performs a flood fill operation on a 2D grid. 
Starting from all initial Green (3) pixels, it changes adjacent Orange (7) pixels to Green (3).
The fill spreads orthogonally (up, down, left, right).
Azure (8) pixels act as barriers, blocking the spread.
Grid boundaries also block the spread.
Pixels that are initially Green (3) or Azure (8) remain unchanged.
Orange (7) pixels not reachable from the initial Green (3) pixels without crossing an Azure (8) barrier remain Orange (7).
"""

import collections
import copy

def transform(input_grid):
    """
    Applies a flood fill starting from Green (3) pixels, filling Orange (7) areas,
    blocked by Azure (8) pixels and grid boundaries.

    Args:
        input_grid (list of list of int): The input 2D grid.

    Returns:
        list of list of int: The transformed 2D grid.
    """
    
    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Constants for colors
    GREEN = 3
    ORANGE = 7
    AZURE = 8

    # Initialize output_grid as a deep copy of the input_grid
    output_grid = copy.deepcopy(input_grid)

    # Initialize a queue for Breadth-First Search (BFS)
    queue = collections.deque()
    
    # Initialize a set to keep track of visited coordinates
    visited = set()

    # Find initial Green (seed) pixels and add them to the queue and visited set
    for r in range(height):
        for c in range(width):
            if input_grid[r][c] == GREEN:
                if (r, c) not in visited:
                    queue.append((r, c))
                    visited.add((r, c))

    # Define orthogonal directions (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Perform BFS flood fill
    while queue:
        # Get the current pixel coordinates from the queue
        r, c = queue.popleft()

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor has already been visited
                if (nr, nc) not in visited:
                    # Check if the neighbor in the *original* input grid is Orange (fillable)
                    if input_grid[nr][nc] == ORANGE:
                        # Change the neighbor's color to Green in the output grid
                        output_grid[nr][nc] = GREEN
                        # Mark the neighbor as visited
                        visited.add((nr, nc))
                        # Add the neighbor to the queue for further exploration
                        queue.append((nr, nc))
                    # If the neighbor is not Orange but also not visited yet (e.g., an Azure barrier), 
                    # mark it as visited so we don't check its color condition again.
                    # This is important if a barrier could be adjacent to multiple fill paths.
                    elif input_grid[nr][nc] != GREEN: # Don't re-add existing green seeds
                         visited.add((nr, nc))


    # Return the modified grid
    return output_grid

```