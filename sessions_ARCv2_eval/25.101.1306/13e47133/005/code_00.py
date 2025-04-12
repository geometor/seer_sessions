"""
Transforms the input grid by performing a simultaneous competitive flood fill
originating from 'seed' pixels.

1.  Identify the boundary color (red, 2) and the background color (most frequent color
    excluding boundaries).
2.  Identify all 'seed' pixels (neither background nor boundary).
3.  Initialize data structures:
    - `output_grid`: A copy of the input grid.
    - `distance_grid`: Stores the minimum BFS distance from any seed to each cell
                      (initialized to infinity).
    - `origin_seed_grid`: Stores the tuple `(color, row, col)` of the seed that
                         claimed each cell (initialized with a placeholder).
    - `queue`: A queue for the multi-source BFS.
4.  Seed the BFS: For each seed pixel, set its distance to 0 in `distance_grid`,
    record its info in `origin_seed_grid`, and add its location to the `queue`.
5.  Run the multi-source BFS:
    - While the queue is not empty, dequeue a cell `(r, c)`.
    - For each valid neighbor `(nr, nc)`:
        - If the neighbor is a background pixel in the input grid:
            - Calculate the distance from the current cell's originating seed.
            - Compare this new path (distance and seed priority) with any existing
              path recorded for the neighbor.
            - Tie-breaking: If distances are equal, the seed with the lower color index wins.
              If colors are also equal, the seed with the lower row index wins. If rows
              are also equal, the seed with the lower column index wins. (This is
              handled implicitly by tuple comparison).
            - If the new path is better (shorter distance or wins tie-break):
                - Update the neighbor's distance, originating seed, and color in the
                  output grid.
                - Enqueue the neighbor *only if* the distance was improved (not just
                  if a tie was broken).
6.  Return the modified `output_grid`.
"""

import numpy as np
from collections import deque, Counter
import heapq # Could potentially use heapq for priority queue if needed, but simple deque works for BFS

def find_background_color(grid: np.ndarray, boundary_color: int) -> int:
    """Finds the most frequent color in the grid, ignoring the boundary color."""
    counts = Counter(grid.flatten())
    if boundary_color in counts:
        del counts[boundary_color] # Don't consider boundary color as background
    if not counts: # Handle edge case of grid with only boundary color or empty
        overall_counts = Counter(grid.flatten())
        if overall_counts:
            return overall_counts.most_common(1)[0][0]
        else:
            return 0 # Default background
    # Tie-breaking for background color (if needed, though unlikely in ARC):
    # Could sort by count descending, then color ascending if Counter keeps insertion order or sort items.
    # For now, most_common(1) is sufficient based on examples.
    return counts.most_common(1)[0][0]

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the simultaneous competitive flood fill transformation.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_grid = np.copy(input_np) # Initialize output grid

    # --- Define constants and identify colors ---
    boundary_color = 2
    background_color = find_background_color(input_np, boundary_color)

    # --- Initialize BFS data structures ---
    distance_grid = np.full((height, width), np.inf, dtype=float)
    # Placeholder seed tuple that will lose any tie-break comparison
    placeholder_seed = (np.inf, np.inf, np.inf)
    origin_seed_grid = np.full((height, width), placeholder_seed, dtype=object)
    queue = deque()

    # --- Seed the BFS queue with initial seed pixels ---
    for r in range(height):
        for c in range(width):
            color = input_np[r, c]
            if color != background_color and color != boundary_color: # It's a seed
                seed_info = (color, r, c) # Tie-breaking priority: color, row, col
                distance_grid[r, c] = 0
                origin_seed_grid[r, c] = seed_info
                queue.append((r, c))
            # Optional: Mark boundaries in distance grid if needed for logic, but checking input_np is sufficient
            # if color == boundary_color:
            #     distance_grid[r, c] = -1 # Mark as unwalkable/non-target

    # --- Run the multi-source BFS ---
    while queue:
        r, c = queue.popleft()
        current_dist = distance_grid[r, c]
        origin_seed = origin_seed_grid[r, c] # The (color, r, c) tuple of the seed that claimed cell (r,c)

        # Explore neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is a background pixel (target for filling)
                if input_np[nr, nc] == background_color:
                    new_dist = current_dist + 1
                    existing_dist = distance_grid[nr, nc]
                    existing_origin_seed = origin_seed_grid[nr, nc]

                    # --- Claiming Logic ---
                    update_owner = False
                    enqueue_neighbor = False

                    if new_dist < existing_dist:
                        # Found a shorter path
                        update_owner = True
                        enqueue_neighbor = True # Must explore further from this cell
                    elif new_dist == existing_dist:
                        # Equidistant path - apply tie-breaking
                        # Lower tuple value means higher priority (lower color, then row, then col)
                        if origin_seed < existing_origin_seed:
                             update_owner = True
                             # Do NOT enqueue - distance didn't decrease, avoids cycles/redundancy

                    if update_owner:
                        distance_grid[nr, nc] = new_dist
                        origin_seed_grid[nr, nc] = origin_seed
                        output_grid[nr, nc] = origin_seed[0] # Assign color of the winning seed

                    if enqueue_neighbor:
                        queue.append((nr, nc))

                # Implicitly handles boundaries and other seeds:
                # If input_np[nr, nc] is not background_color, the 'if' condition fails.

    # --- Return the result ---
    return output_grid.tolist()