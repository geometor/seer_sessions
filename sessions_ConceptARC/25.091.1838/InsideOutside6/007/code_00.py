"""
Identifies the background color (0), the container color (most frequent non-background color), and the target color (other non-background color). 
Determines an 'outside' region consisting of background cells reachable from the grid boundary by traversing only adjacent background cells. 
Creates an output grid initialized with the background color. 
Copies the target color to the output grid only for those target cells in the input that are adjacent (8-way) to at least one cell belonging to the identified 'outside' background region. All other cells, including the container color and 'inside' target cells, are replaced with the background color.
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
             target_color is None if only background exists or if only background and container exist (though this case seems unlikely based on examples).
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

    # If container_color was identified but target_color remains None (only 2 colors total: bg and container)
    # Re-evaluate based on the task logic: the single non-bg color should be the target if no container logic applies.
    # However, the problem implies the most frequent non-bg IS the container. If target_color is None
    # after the sort, it means there isn't a second non-bg color to be the target.
    # The logic seems robust for the cases seen (bg+container+target or bg+target).

    return background_color, container_color, target_color


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
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

    # 5. Perform BFS to find the 'outside' background region
    # This region includes background cells reachable from the boundary
    # by moving only through other background cells.
    q = deque()
    visited_background = np.zeros_like(input_np, dtype=bool)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)] # 8-way

    # Add boundary background cells to queue and mark as visited
    for r in range(rows):
        for c in [0, cols - 1]: # Left and right edges
            if input_np[r, c] == background_color and not visited_background[r, c]:
                q.append((r, c))
                visited_background[r, c] = True
    for c in range(1, cols - 1): # Top and bottom edges (excluding corners)
         for r in [0, rows - 1]:
             if input_np[r, c] == background_color and not visited_background[r, c]:
                q.append((r, c))
                visited_background[r, c] = True

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
                # Check if any 8-way neighbor is part of the 'outside' background region
                keep_target = False
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    # Check bounds and if the neighbor is an 'outside' background cell
                    if (0 <= nr < rows and 0 <= nc < cols and
                            input_np[nr, nc] == background_color and
                            visited_background[nr, nc]):
                        keep_target = True
                        break # Found a connection to the outside background

                # If connected to the outside background, copy target color to output
                if keep_target:
                    output_grid[r, c] = target_color

    # 7. Return the modified output grid as a list of lists
    return output_grid.tolist()