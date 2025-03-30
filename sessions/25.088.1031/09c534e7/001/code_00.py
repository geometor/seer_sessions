import numpy as np
from collections import deque

"""
Transformation Rule Description:

The transformation identifies non-background (white, 0) and non-primary shape (blue, 1) pixels, referred to as "seed" pixels. For each seed pixel, it performs a flood fill operation starting from the adjacent blue pixels. The flood fill propagates only through contiguous blue pixels (using 4-way adjacency) in the original input grid. All blue pixels reached by the flood fill originating from a specific seed are changed to the color of that seed in the output grid. If multiple seeds could potentially fill the same blue pixel, the first fill operation reaching that pixel determines its final color (implicit BFS order, though examples don't show conflicts). The original seed pixels and background pixels remain unchanged.
"""

def find_seeds(grid):
    """Finds seed pixels (non-white, non-blue) in the grid."""
    seeds = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != 0 and color != 1:
                seeds.append(((r, c), color))
    return seeds

def transform(input_grid):
    """
    Transforms the input grid by flood-filling blue regions adjacent to 
    seed pixels with the seed's color.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    seeds = find_seeds(input_grid)
    
    # Keep track of pixels already colored by a fill operation
    visited_by_fill = set() 

    for seed_coord, seed_color in seeds:
        sr, sc = seed_coord
        q = deque()
        
        # Start the fill from the blue neighbors of the seed
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = sr + dr, sc + dc
            
            # Check bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if neighbor is blue in the *original* grid
                # and hasn't been visited by *any* fill operation yet
                if input_grid[nr, nc] == 1 and (nr, nc) not in visited_by_fill:
                    # Add to queue for BFS
                    q.append((nr, nc))
                    # Mark as visited by a fill
                    visited_by_fill.add((nr, nc))
                    # Change color in the output grid
                    output_grid[nr, nc] = seed_color
                    
        # Perform BFS
        while q:
            curr_r, curr_c = q.popleft()
            
            # Explore neighbors
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = curr_r + dr, curr_c + dc
                
                # Check bounds
                if 0 <= nr < height and 0 <= nc < width:
                     # Check if neighbor is blue in the *original* grid
                     # and hasn't been visited by *any* fill operation yet
                    if input_grid[nr, nc] == 1 and (nr, nc) not in visited_by_fill:
                        # Add to queue for BFS
                        q.append((nr, nc))
                         # Mark as visited by a fill
                        visited_by_fill.add((nr, nc))
                        # Change color in the output grid
                        output_grid[nr, nc] = seed_color

    return output_grid