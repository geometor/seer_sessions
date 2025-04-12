import copy
from collections import deque

"""
Performs a constrained color spreading operation, visually similar to a flood fill.
The transformation starts from all initial green (3) pixels ('seeds').
It spreads in 8 directions (horizontally, vertically, and diagonally) into
adjacent orange (7) pixels ('fillable area'). Azure (8) pixels act as
impassable barriers, blocking the spread.

Orange pixels that are deemed 'reachable' from the initial green seeds,
following the specific rules of connectivity and barrier interaction for this task,
are changed to green (3). Initial green pixels, azure pixels, and orange pixels
that are not reachable according to the task's specific rules remain unchanged.

NOTE: Standard 8-directional flood fill algorithms (like the one implemented below)
have been observed to produce outputs that differ from the provided training examples
for this task (specifically, they tend to fill *more* orange pixels than expected).
This suggests the actual transformation rule involves additional constraints or
modifications to the standard flood fill behavior that are not yet fully captured.
This implementation represents the closest standard algorithm based on visual inspection
and the hypothesis of an 8-way flood fill, but is expected to fail on the provided
training examples. The true rule remains unidentified.
"""

# Define color constants for clarity
ORANGE = 7
GREEN = 3
AZURE = 8

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on a standard 8-directional flood fill rule,
    acknowledging its known discrepancies with the expected task behavior based on examples.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the transformed 2D grid according to the standard
        8-way flood fill algorithm.
    """

    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        # Return grid of empty rows matching input height if width is 0
        return [[] for _ in range(height)]

    # Initialize output_grid as a deep copy to modify
    output_grid = copy.deepcopy(input_grid)

    # Initialize queue for Breadth-First Search (BFS)
    queue = deque()
    # Keep track of visited cells ((row, col) tuples) to avoid cycles and redundant work
    visited = set()

    # Find initial green seed pixels.
    # Add their locations to the queue to start the BFS and mark them as visited.
    for r in range(height):
        for c in range(width):
            if input_grid[r][c] == GREEN:
                seed_location = (r, c)
                # Ensure seeds are not added multiple times if they are adjacent
                # and already processed during this initial scan.
                if seed_location not in visited:
                    queue.append(seed_location)
                    visited.add(seed_location)

    # Define the 8 possible relative offsets for neighbors (including diagonals)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # Above row (NW, N, NE)
        (0, -1),          (0, 1),   # Current row (W, E)
        (1, -1), (1, 0), (1, 1)    # Below row (SW, S, SE)
    ]

    # Perform the flood fill using BFS
    while queue:
        # Get the current location (pixel) from the front of the queue
        r, c = queue.popleft()

        # Explore neighbors in all 8 directions
        for dr, dc in directions:
            # Calculate neighbor coordinates
            nr, nc = r + dr, c + dc
            neighbor_location = (nr, nc)

            # Check 1: Is the neighbor within the grid boundaries?
            if 0 <= nr < height and 0 <= nc < width:
                # Check 2: Has the neighbor already been visited?
                if neighbor_location not in visited:
                    # Check 3: Is the neighbor an orange pixel (fillable) in the *original* input grid?
                    # Azure pixels (barriers) and already green pixels (initial or filled) will fail this check.
                    if input_grid[nr][nc] == ORANGE:
                        # If checks pass, this is a valid pixel to fill under standard flood fill:
                        # 1. Change its color to green in the output grid
                        output_grid[nr][nc] = GREEN
                        # 2. Mark it as visited to prevent reprocessing
                        visited.add(neighbor_location)
                        # 3. Add it to the queue to explore its neighbors later
                        queue.append(neighbor_location)
                    # Note: We don't explicitly need to add non-orange neighbors to visited set here.
                    # They won't be added to the queue, so the fill won't propagate through them.
                    # Adding them to visited could slightly optimize by preventing re-checks
                    # if they are neighbors of multiple filled cells, but isn't strictly necessary
                    # for correctness of this standard algorithm.

    # Return the modified grid after the fill process is complete
    return output_grid