import numpy as np
from collections import deque

"""
1. Create a copy of the input grid.
2. Find the single magenta pixel (6) which serves as the starting point.
3. Perform a flood fill starting from the magenta pixel:
    - Change reachable gray pixels (8) to orange (7).
    - The fill expands horizontally and vertically.
    - Blue pixels (1) act as boundaries and stop the fill.
    - Magenta (6) and blue (1) pixels remain unchanged.
    - The fill originates *from* the magenta pixel, but the magenta pixel itself is not changed.
"""

def find_start_point(grid):
    """Finds the coordinates of the first pixel with value 6."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 6:
                return (r, c)
    return None # Should not happen based on task description

def transform(input_grid):
    """
    Transforms the input grid by performing a flood fill starting from the
    magenta pixel (6), changing reachable gray pixels (8) to orange (7),
    bounded by blue pixels (1).
    """
    # Convert input_grid to a numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    rows, cols = output_grid.shape

    # 1. Find the starting point (magenta pixel)
    start_pos = find_start_point(input_grid_np)
    if start_pos is None:
        # If no start point is found (shouldn't happen in this task), return the original grid
        return output_grid.tolist()

    # 2. Initialize Flood Fill structures
    queue = deque([start_pos]) # Queue for Breadth-First Search (BFS)
    visited = set() # Keep track of visited cells to avoid cycles

    # 3. Perform Flood Fill
    while queue:
        r, c = queue.popleft()

        # Check if current position is already visited
        if (r, c) in visited:
            continue
        visited.add((r, c))

        # Get the color of the current pixel in the original input grid
        current_color = input_grid_np[r, c]

        # If the current pixel is gray (8), change it to orange (7) in the output grid
        if current_color == 8:
            output_grid[r, c] = 7

        # Explore neighbors only if the current cell is gray (8) or the start point (magenta, 6)
        # This allows the fill to originate *from* magenta but only colors gray cells
        if current_color == 8 or current_color == 6:
            # Iterate through neighbors (up, down, left, right)
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc

                # Check if neighbor is within grid bounds
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Check if the neighbor is not already visited
                    if (nr, nc) not in visited:
                        neighbor_color = input_grid_np[nr, nc]
                        # Check if the neighbor is not a boundary (blue, 1)
                        if neighbor_color != 1:
                            # Add valid neighbor to the queue
                            queue.append((nr, nc))

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()