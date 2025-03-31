import numpy as np
from collections import deque

"""
Transformation Rule:

1. Identify 'seed' pixels in the input grid. A seed pixel is any pixel that is neither blue (1) nor white (0).
2. For each seed pixel found at location (r, c) with color C:
3. Perform a flood fill operation starting from the blue (1) neighbors of the seed pixel.
4. The flood fill uses the seed's color C.
5. The fill spreads to adjacent (up, down, left, right) blue (1) pixels within the same contiguous blue region as the initial blue neighbors.
6. The fill stops at boundaries defined by non-blue pixels in the original input grid.
7. The original seed pixel retains its color. Pixels outside the filled blue regions remain unchanged.
8. The process is repeated for all seed pixels found in the input grid. The output grid reflects all completed fill operations.
"""

def transform(input_grid):
    """
    Applies a flood fill transformation to the input grid based on seed pixels.

    Args:
        input_grid (np.ndarray): A 2D NumPy array representing the input grid.

    Returns:
        np.ndarray: A 2D NumPy array representing the transformed output grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Keep track of visited cells across different fill operations to avoid refilling
    # This prevents a later fill from overriding an earlier one if seeds are adjacent
    # Note: We only mark cells *after* they are filled with a *new* color.
    # Blue cells that are checked but not filled are not marked here.
    globally_filled = np.zeros_like(input_grid, dtype=bool)

    # Find all potential seed pixels first
    seeds = []
    for r in range(rows):
        for c in range(cols):
            color = input_grid[r, c]
            if color != 0 and color != 1:
                seeds.append(((r, c), color))

    # Process each seed
    for seed_coord, seed_color in seeds:
        r_seed, c_seed = seed_coord
        
        # Initialize queue and visited set for this specific flood fill
        q = deque()
        visited_this_fill = set()

        # Find initial blue neighbors of the seed to start the fill
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r_seed + dr, c_seed + dc

            # Check boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor is blue in the original grid
                # and hasn't been filled by a *previous* seed's operation
                if input_grid[nr, nc] == 1 and not globally_filled[nr, nc]:
                    # Check if not already visited *in this specific fill*
                    if (nr, nc) not in visited_this_fill:
                        output_grid[nr, nc] = seed_color # Fill the neighbor
                        globally_filled[nr, nc] = True   # Mark as globally filled
                        q.append((nr, nc))               # Add to queue for expansion
                        visited_this_fill.add((nr, nc))  # Mark as visited for this fill

        # Perform the flood fill (BFS) starting from the initial neighbors
        while q:
            curr_r, curr_c = q.popleft()

            # Explore neighbors of the current blue cell
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_r, next_c = curr_r + dr, curr_c + dc

                # Check boundaries
                if 0 <= next_r < rows and 0 <= next_c < cols:
                    # Check if the neighbor is blue in the original grid
                    # and hasn't been filled by a *previous* seed's operation
                    if input_grid[next_r, next_c] == 1 and not globally_filled[next_r, next_c]:
                         # Check if not already visited *in this specific fill*
                        if (next_r, next_c) not in visited_this_fill:
                             output_grid[next_r, next_c] = seed_color # Fill the neighbor
                             globally_filled[next_r, next_c] = True   # Mark as globally filled
                             q.append((next_r, next_c))               # Add to queue
                             visited_this_fill.add((next_r, next_c))  # Mark as visited for this fill

    return output_grid