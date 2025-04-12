```python
import copy
from collections import deque

# Color constants used in the task
ORANGE = 7
GREEN = 3
AZURE = 8

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Performs a flood fill operation on the input grid.

    The flood fill starts from all initial green (3) pixels. It spreads
    in 8 directions (horizontally, vertically, and diagonally) to adjacent
    orange (7) pixels. Azure (8) pixels act as barriers and block the spread.
    Orange pixels reachable from the initial green seeds without crossing
    an azure barrier are changed to green. Initial green pixels, azure pixels,
    and unreachable orange pixels remain unchanged.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the transformed 2D grid.
    """

    # Initialize output_grid as a deep copy of the input grid
    output_grid = copy.deepcopy(input_grid)
    height = len(input_grid)
    if height == 0:
        return output_grid
    width = len(input_grid[0])
    if width == 0:
        return output_grid

    # Initialize queue for Breadth-First Search (BFS)
    queue = deque()
    # Keep track of visited cells to avoid cycles and redundant work
    visited = set()

    # Find initial green seed pixels and add them to the queue and visited set
    for r in range(height):
        for c in range(width):
            if input_grid[r][c] == GREEN:
                seed = (r, c)
                if seed not in visited:
                    queue.append(seed)
                    visited.add(seed)

    # Define the 8 possible directions for neighbors (including diagonals)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Perform the flood fill using BFS
    while queue:
        r, c = queue.popleft()

        # Explore neighbors in all 8 directions
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                neighbor_coords = (nr, nc)

                # Check if the neighbor has already been visited
                if neighbor_coords not in visited:
                    # Check if the neighbor is an orange pixel (fillable) in the original grid
                    if input_grid[nr][nc] == ORANGE:
                        # Change the color of the neighbor to green in the output grid
                        output_grid[nr][nc] = GREEN
                        # Mark the neighbor as visited
                        visited.add(neighbor_coords)
                        # Add the neighbor to the queue to explore from it later
                        queue.append(neighbor_coords)
                    # If the neighbor is not orange (e.g., azure barrier or already green),
                    # still mark it as visited *if it's not a barrier* to potentially optimize
                    # later checks, though strictly necessary only for fillable cells.
                    # However, adding barriers (AZURE) to visited can prevent re-checking them,
                    # and initial GREEN cells are already added.
                    # Let's only add fillable cells to visited to strictly follow the spread logic.
                    # Reconsidering: add non-fillable (but not barrier) neighbours to visited
                    # to avoid checking them repeatedly from different paths?
                    # The current logic only adds *newly filled* cells to visited and queue.
                    # What if an orange cell is reachable from two different spread paths?
                    # The `visited` check prevents processing it twice.
                    # What about initial green cells? They start in visited.
                    # What about barrier cells? They are never added to visited or queue.
                    # This seems correct. Only orange cells that get filled are added.

    return output_grid
```