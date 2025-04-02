import numpy as np
from collections import deque

"""
Identifies the background color (0), the container color (most frequent non-background color), and the target color (other non-background color).
Performs a Breadth-First Search (BFS) starting only from background-colored cells on the grid boundary, exploring only through adjacent background cells, to identify the 'outside' background region.
Creates an output grid initialized with the background color.
Copies the target color to the output grid only for cells that originally contained the target color AND are adjacent (8-way) to at least one cell marked as belonging to the 'outside' background region.
"""

def _identify_colors(grid):
    """
    Identifies background, container, and target colors based on frequency.
    Assumes background is 0.
    Container is the most frequent non-background color.
    Target is the other non-background color.
    Handles cases with 0, 1, or 2 non-background colors.
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
        target_color = sorted_colors[1][0] # The next most frequent is assumed target
        # If there are more than 2 non-bg colors, this heuristic might fail.
        # For this specific task, it seems there are only ever 2 non-bg colors.
    elif len(sorted_colors) == 1:
         # If only one non-background color, it acts as the target, no container blocking
         target_color = sorted_colors[0][0]
         container_color = -1 # Use -1 to signify no effective container barrier

    return background_color, container_color, target_color


def transform(input_grid):
    """
    Filters the input grid based on reachability from the outer background.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # 1. Identify the key colors
    background_color, container_color, target_color = _identify_colors(input_np)

    # 2. Initialize output grid with background color
    output_grid = np.full_like(input_np, background_color)

    # 3. Handle edge cases: no target color
    if target_color is None:
        return output_grid.tolist()

    # 4. Handle edge case: no container color (only background and target)
    # In this case, all target pixels are effectively 'outside'.
    if container_color == -1:
        output_grid[input_np == target_color] = target_color
        return output_grid.tolist()

    # 5. Perform flood fill (BFS) from boundary *background* cells
    # This identifies the 'outside' background region.
    q = deque()
    visited_background = np.zeros_like(input_np, dtype=bool)

    # Add boundary background cells to queue and mark as visited
    for r in range(rows):
        for c in [0, cols - 1]:
            if input_np[r, c] == background_color and not visited_background[r, c]:
                q.append((r, c))
                visited_background[r, c] = True
    for c in range(cols): # Cover top/bottom rows, including corners again (fine)
        for r in [0, rows - 1]:
            if input_np[r, c] == background_color and not visited_background[r, c]:
                q.append((r, c))
                visited_background[r, c] = True

    # Define 8 directions for neighbors (including diagonals)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    # Start BFS, exploring only through background cells
    while q:
        r, c = q.popleft()

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check bounds and if the neighbor is background and not visited
            if (0 <= nr < rows and 0 <= nc < cols and
                    input_np[nr, nc] == background_color and
                    not visited_background[nr, nc]):
                visited_background[nr, nc] = True
                q.append((nr, nc))

    # 6. Populate the output grid
    # Iterate through all input cells
    for r in range(rows):
        for c in range(cols):
            # If the cell contains the target color
            if input_np[r, c] == target_color:
                # Check its 8 neighbors
                keep_target = False
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    # Check bounds
                    if 0 <= nr < rows and 0 <= nc < cols:
                        # Check if the neighbor is background AND part of the 'outside' region
                        if input_np[nr, nc] == background_color and visited_background[nr, nc]:
                            keep_target = True
                            break # Found a connection to the outside, no need to check further neighbors

                # If connected to the outside background, copy target color to output
                if keep_target:
                    output_grid[r, c] = target_color

    # 7. Return the modified output grid as a list of lists
    return output_grid.tolist()