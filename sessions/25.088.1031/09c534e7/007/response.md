```python
import numpy as np
from collections import deque

"""
Transformation Rule Description:

The transformation identifies "seed" pixels, which are any pixels that are not the background color (white, 0) and not the primary shape color (blue, 1). For each seed pixel found:
1. It checks its 4-way adjacent neighbors in the input grid.
2. If an adjacent neighbor is blue (1), this neighbor serves as the starting point for a flood fill operation.
3. The flood fill operation identifies the entire connected component of blue (1) pixels reachable from that starting neighbor using 4-way adjacency.
4. All pixels within this identified blue component are then colored in the output grid with the color of the original seed pixel.
5. This process repeats for all seed pixels. If a blue component is adjacent to multiple seeds, the component takes the color of the seed processed last during iteration. Pixels that are not part of a blue component adjacent to a seed retain their original color from the input grid.
"""

def get_neighbors(coord, shape):
    """Gets 4-way adjacent neighbor coordinates within grid bounds."""
    r, c = coord
    height, width = shape
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbors.append((nr, nc))
    return neighbors

def flood_fill(grid, start_coord, fill_color, target_color, output_grid, visited):
    """Performs flood fill on the grid starting from start_coord."""
    height, width = grid.shape
    
    # Check if the starting coordinate is valid for flood fill
    # It must be the target color and not visited yet.
    start_r, start_c = start_coord
    if grid[start_r, start_c] != target_color or visited[start_r, start_c]:
        return # Already visited or not the target color

    q = deque([start_coord])
    
    while q:
        r, c = q.popleft()

        # Check bounds and if already visited or not the target color
        # This check is important as the queue might contain coords already processed by another branch
        if not (0 <= r < height and 0 <= c < width) or visited[r, c] or grid[r, c] != target_color:
            continue

        # Mark as visited and set the color in the output grid
        visited[r, c] = True
        output_grid[r, c] = fill_color

        # Add valid neighbors to the queue
        for nr, nc in get_neighbors((r, c), (height, width)):
             if 0 <= nr < height and 0 <= nc < width and not visited[nr, nc] and grid[nr, nc] == target_color:
                q.append((nr, nc))


def transform(input_grid):
    """
    Transforms the input grid by flood-filling connected blue regions 
    adjacent to seed pixels with the seed's color.
    """
    height, width = input_grid.shape
    output_grid = np.copy(input_grid)
    visited_blue = np.zeros_like(input_grid, dtype=bool) # Keep track of blue pixels already filled

    # Iterate through each pixel to find seeds
    for r in range(height):
        for c in range(width):
            seed_color = input_grid[r, c]
            
            # Check if the current pixel is a seed (not background 0, not primary 1)
            if seed_color != 0 and seed_color != 1:
                seed_coord = (r, c)
                
                # Find 4-way neighbors of the seed
                seed_neighbors = get_neighbors(seed_coord, (height, width))
                
                # Check each neighbor to see if it's a blue pixel that can start a flood fill
                for neighbor_r, neighbor_c in seed_neighbors:
                    # If the neighbor in the original input grid is blue (1) 
                    # and hasn't been filled yet
                    if input_grid[neighbor_r, neighbor_c] == 1 and not visited_blue[neighbor_r, neighbor_c]:
                        # Start flood fill from this blue neighbor
                        # The fill color is the seed's color
                        # The target color for filling is blue (1)
                        flood_fill(input_grid, 
                                   (neighbor_r, neighbor_c), 
                                   seed_color, 
                                   1, # target color is blue
                                   output_grid, 
                                   visited_blue) 
                        # Note: The flood_fill function modifies output_grid and visited_blue directly

    return output_grid
```