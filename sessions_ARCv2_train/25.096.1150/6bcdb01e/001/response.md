```python
import copy
from collections import deque

"""
Apply a flood fill transformation starting from cells with value 3. 
The fill propagates horizontally and vertically to adjacent cells containing the value 7, changing them to 3. 
Cells with value 8 act as barriers and stop the fill. 
Cells initially containing 3 or 8, and 7s not reached by the fill, remain unchanged.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on a flood fill rule originating from '3' cells.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed output grid.
    """

    # Get grid dimensions
    if not input_grid or not input_grid[0]:
        return []
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input grid
    # This ensures that 8s, initial 3s, and unreachable 7s are preserved
    # unless explicitly changed by the flood fill.
    output_grid = [row[:] for row in input_grid] # Sufficient for lists of ints

    # Initialize a queue for the flood fill (BFS)
    queue = deque()

    # Find initial seed cells (value 3) and add them to the queue
    # Note: Cells initially 3 don't need to be explicitly processed by the fill
    # logic itself, but their neighbors do. We add neighbors of 3s that are 7s
    # or we can just add the 3s and let the main loop handle neighbors.
    # Adding the 3s themselves is simpler and covers all cases.
    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] == 3:
                 # Although the 3 itself doesn't change, it acts as a source.
                 # We add its coords to potentially start filling adjacent 7s.
                 # No need to explicitly mark visited, as we only change 7s to 3s
                 # in the output_grid, and the check output_grid[nr][nc] == 7 handles this.
                 queue.append((r, c))


    # Perform the flood fill using Breadth-First Search (BFS)
    while queue:
        r, c = queue.popleft()

        # Define potential neighbors (up, down, left, right)
        neighbors = [
            (r - 1, c),
            (r + 1, c),
            (r, c - 1),
            (r, c + 1),
        ]

        for nr, nc in neighbors:
            # Check if the neighbor is within the grid boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor cell in the *input* grid contains 7
                # AND if its corresponding cell in the *output* grid is still 7
                # (meaning it hasn't been reached/processed by the fill yet).
                # The condition input_grid[nr][nc] == 7 is technically redundant if
                # we start correctly, as only 7s can become 3s, but it's safer
                # to include, matching the natural language description precisely.
                if input_grid[nr][nc] == 7 and output_grid[nr][nc] == 7:
                    # Change the value in the output grid to 3
                    output_grid[nr][nc] = 3
                    # Add this newly changed cell to the queue to process its neighbors
                    queue.append((nr, nc))

    # The output_grid now contains the final state after the flood fill
    return output_grid
```