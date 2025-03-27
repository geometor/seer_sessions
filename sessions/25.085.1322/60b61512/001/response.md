```python
import numpy as np
from collections import deque

def transform(input_grid):
    """
    Identifies white (0) pixels that are fully enclosed by yellow (4) pixels
    and changes them to orange (7). A white pixel is considered enclosed if it
    cannot reach the boundary of the grid by moving only through adjacent
    (up, down, left, right) white pixels. Other pixels remain unchanged.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    output_array = input_array.copy()
    rows, cols = input_array.shape

    # Create a visited grid to keep track of white pixels reachable from the boundary
    visited = np.zeros_like(input_array, dtype=bool)
    queue = deque()

    # Add all white pixels on the boundary to the queue and mark them as visited
    for r in range(rows):
        for c in range(cols):
            # Check if the cell is on the boundary
            if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                # Check if the cell is white (0) and not already visited
                if input_array[r, c] == 0 and not visited[r, c]:
                    visited[r, c] = True
                    queue.append((r, c))

    # Define the four cardinal directions for neighbors
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Perform Breadth-First Search (BFS) starting from the boundary white pixels
    while queue:
        r, c = queue.popleft()

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within the grid boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor is white (0) and not visited
                if input_array[nr, nc] == 0 and not visited[nr, nc]:
                    visited[nr, nc] = True
                    queue.append((nr, nc))

    # Iterate through the grid to find unenclosed white pixels
    for r in range(rows):
        for c in range(cols):
            # If a pixel is white (0) and was not reached by the BFS (not visited),
            # it means it's enclosed. Change its color to orange (7).
            if input_array[r, c] == 0 and not visited[r, c]:
                output_array[r, c] = 7

    # Convert the NumPy array back to a list of lists for the final output
    return output_array.tolist()

```