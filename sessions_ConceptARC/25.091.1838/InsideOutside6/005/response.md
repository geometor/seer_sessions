```python
"""
Identifies the background color (0), the container color (most frequent non-background color), and the target color (other non-background color). 
Performs a Breadth-First Search (BFS) starting from all grid boundary cells that do not contain the container color. 
The BFS explores adjacent cells (8-way connectivity), but cannot pass through cells containing the container color. 
This BFS identifies all cells reachable from the outside ('outside_region').
Creates an output grid initialized with the background color. 
Copies the target color to the output grid only for cells that originally contained the target color AND were marked as reachable ('outside_region') during the BFS.
"""

import numpy as np
from collections import deque

def _identify_colors(grid):
    """
    Identifies background, container, and target colors based on frequency.
    Assumes background is 0.
    Container is the most frequent non-background color.
    Target is the other non-background color.
    Handles cases with 0, 1, or 2 non-background colors.
    Returns: background_color, container_color, target_color
             container_color is None if only background exists.
             container_color is -1 if only background and one other color exist (no effective container).
             target_color is None if only background exists.
    """
    unique_colors, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))

    # Assume background is 0
    background_color = 0
    if background_color in color_counts:
        del color_counts[background_color]

    if not color_counts: # Only background color present
        return background_color, None, None

    # Sort by count descending, then by color value ascending as tie-breaker
    sorted_colors = sorted(color_counts.items(), key=lambda item: (-item[1], item[0]))

    container_color = None
    target_color = None

    if len(sorted_colors) >= 2:
        container_color = sorted_colors[0][0]
        # Assume the second most frequent (or first if counts are equal but color is higher)
        # is the target. This simple heuristic works for the examples.
        target_color = sorted_colors[1][0]
    elif len(sorted_colors) == 1:
         # If only one non-background color, it acts as the target, no container blocking
         target_color = sorted_colors[0][0]
         container_color = -1 # Use -1 to signify no effective container barrier

    return background_color, container_color, target_color


def transform(input_grid):
    """
    Filters the input grid keeping only target pixels reachable from the boundary
    without crossing the container color.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # 1. Identify the key colors
    background_color, container_color, target_color = _identify_colors(input_np)

    # 2. Initialize output grid with background color
    output_grid = np.full_like(input_np, background_color)

    # 3. Handle edge case: no target color
    if target_color is None:
        return output_grid.tolist()

    # 4. Handle edge case: no container color (or only background and target)
    # In this case, all target pixels are effectively 'outside'.
    if container_color is None or container_color == -1:
        output_grid[input_np == target_color] = target_color
        return output_grid.tolist()

    # 5. Perform BFS from boundaries to find 'outside' cells
    q = deque()
    visited = np.zeros_like(input_np, dtype=bool)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)] # 8-way

    # Add boundary cells to queue if they are not the container color and not visited
    for r in range(rows):
        for c in [0, cols - 1]: # Left and right edges
            if input_np[r, c] != container_color and not visited[r, c]:
                q.append((r, c))
                visited[r, c] = True
    for c in range(1, cols - 1): # Top and bottom edges (excluding corners already added)
         for r in [0, rows - 1]:
             if input_np[r, c] != container_color and not visited[r, c]:
                q.append((r, c))
                visited[r, c] = True

    # Start BFS to mark all reachable 'outside' cells
    while q:
        r, c = q.popleft()

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is not visited AND not the container color
                if not visited[nr, nc] and input_np[nr, nc] != container_color:
                    visited[nr, nc] = True
                    q.append((nr, nc))

    # 6. Populate the output grid
    # Iterate through all input cells
    for r in range(rows):
        for c in range(cols):
            # If the input cell contains the target color AND it was visited (is outside)
            if input_np[r, c] == target_color and visited[r, c]:
                # Set the corresponding cell in the output grid to the target color
                output_grid[r, c] = target_color

    # 7. Return the modified output grid as a list of lists
    return output_grid.tolist()
```