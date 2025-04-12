```python
import numpy as np
from collections import deque, Counter

"""
Transforms the input grid by performing a competitive flood fill based on seed pixels.

1.  Identify the boundary color (red, color 2).
2.  Identify the background color (most frequent color excluding boundary).
3.  Identify 'seed' pixels (neither background nor boundary).
4.  Create an output grid, initially a copy of the input.
5.  Create a mask to track filled pixels (boundaries, seeds, and filled areas).
6.  Sort seeds by priority: highest color index first, then lowest row, then lowest column.
7.  Iterate through sorted seeds:
    - Perform a Breadth-First Search (BFS) starting from the neighbors of the current seed.
    - The BFS fills adjacent background pixels with the seed's color.
    - The fill stops at boundaries, already filled pixels (by higher priority seeds or original elements), or grid edges.
    - Update the output grid and the filled mask during the BFS.
8.  Return the final output grid.
"""

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
    return counts.most_common(1)[0][0]

def bfs_fill(input_grid: np.ndarray,
             output_grid: np.ndarray,
             filled_mask: np.ndarray,
             start_loc: tuple[int, int],
             seed_color: int,
             background_color: int):
    """
    Performs BFS fill originating from valid background neighbors of start_loc.
    Updates output_grid and filled_mask in place.
    """
    q = deque()
    height, width = input_grid.shape
    r_start, c_start = start_loc

    # --- Initial Step: Seed the queue with valid neighbors ---
    # Check the 4 direct neighbors of the actual seed location
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r_start + dr, c_start + dc

        # Check bounds
        if 0 <= nr < height and 0 <= nc < width:
            neighbor_loc = (nr, nc)
            # Check if neighbor is background AND not already filled/blocked
            if input_grid[neighbor_loc] == background_color and not filled_mask[neighbor_loc]:
                # Fill this neighbor immediately
                output_grid[neighbor_loc] = seed_color
                filled_mask[neighbor_loc] = True
                q.append(neighbor_loc) # Add to queue for further expansion

    # --- BFS Expansion ---
    while q:
        r, c = q.popleft()

        # Explore neighbors of the current cell (r, c) from the queue
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds
            if 0 <= nr < height and 0 <= nc < width:
                neighbor_loc = (nr, nc)
                # Check if neighbor is background AND not already filled/blocked
                if input_grid[neighbor_loc] == background_color and not filled_mask[neighbor_loc]:
                    # Fill the neighbor
                    output_grid[neighbor_loc] = seed_color
                    filled_mask[neighbor_loc] = True
                    q.append(neighbor_loc) # Add to queue

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the competitive flood fill transformation.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_grid = np.copy(input_np) # Initialize output grid

    # --- Define constants ---
    boundary_color = 2

    # --- Identify background color ---
    background_color = find_background_color(input_np, boundary_color)

    # --- Identify seeds and initialize filled_mask ---
    seeds = []
    filled_mask = np.zeros_like(input_np, dtype=bool)
    for r in range(height):
        for c in range(width):
            color = input_np[r, c]
            if color == boundary_color:
                filled_mask[r, c] = True # Mark boundaries as filled
            elif color != background_color:
                # This is a seed pixel
                seeds.append({'color': color, 'row': r, 'col': c})
                filled_mask[r, c] = True # Mark seed locations as filled

    # --- Sort seeds by priority: highest color, lowest row, lowest col ---
    # Sort key uses negative color for descending order
    seeds.sort(key=lambda s: (-s['color'], s['row'], s['col']))

    # --- Perform competitive BFS fill for each seed in priority order ---
    for seed in seeds:
        seed_loc = (seed['row'], seed['col'])
        seed_color = seed['color']
        # The BFS function handles filling adjacent background areas
        # It modifies output_grid and filled_mask directly
        bfs_fill(input_np, output_grid, filled_mask, seed_loc, seed_color, background_color)

    # --- Return the result ---
    return output_grid.tolist()
```