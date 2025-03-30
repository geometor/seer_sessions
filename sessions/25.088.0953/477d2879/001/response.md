```python
import numpy as np
from collections import deque

def transform(input_grid):
    """
    Transforms the input grid based on a flood-fill or expansion rule originating from 'seed' pixels.

    1.  Identifies 'seed pixels' (any color other than white (0) or blue (1)) in the input grid.
    2.  Initializes an output grid, a distance grid (initialized to infinity), and a color grid (initialized to -1).
    3.  Sets the distance to 0 and the color to the seed's color for all seed pixel locations in the respective grids.
    4.  Uses a Breadth-First Search (BFS) starting simultaneously from all seed pixels.
    5.  The BFS expands outwards layer by layer into adjacent cells.
    6.  For each cell being considered for expansion:
        - If the expansion reaches the cell with a shorter distance than previously recorded, update the cell's distance and color (from the originating seed) in the distance and color grids, and add the cell to the BFS queue.
        - If the expansion reaches the cell with the *same* distance as previously recorded, compare the current expanding seed's color with the already recorded color. If the current seed's color has a lower numerical value, update the cell's color in the color grid (tie-breaking rule: lower color index wins). Add the cell to the BFS queue only if the distance was updated, not just the color for a tie-break at the same distance. *Correction*: Just update the color; no need to re-add to queue if only tie-breaking.
    7.  The expansion continues until the queue is empty.
    8.  The final `color_grid` represents the output, where each cell contains the color of the closest seed pixel according to the BFS expansion and tie-breaking rule.
    """
    
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    
    # Initialize distance grid with infinity and color grid with -1 (or another placeholder)
    distance_grid = np.full((height, width), float('inf'))
    # The output grid will store the final colors
    output_grid = np.full((height, width), -1, dtype=int) 
    
    # Use a deque for BFS queue
    queue = deque()
    
    # Identify seed pixels and initialize the BFS
    for r in range(height):
        for c in range(width):
            color = input_grid_np[r, c]
            # Seed pixels are those not 0 (white) and not 1 (blue)
            if color != 0 and color != 1:
                distance_grid[r, c] = 0
                output_grid[r, c] = color
                queue.append((r, c))

    # Define neighbors (4-directional adjacency)
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    # Perform BFS
    while queue:
        r, c = queue.popleft()
        current_dist = distance_grid[r, c]
        current_color = output_grid[r, c]
        
        # Explore neighbors
        for i in range(4):
            nr, nc = r + dr[i], c + dc[i]
            
            # Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                new_dist = current_dist + 1
                
                # Check if this path is shorter than any previous path
                if new_dist < distance_grid[nr, nc]:
                    distance_grid[nr, nc] = new_dist
                    output_grid[nr, nc] = current_color
                    queue.append((nr, nc))
                # Check for tie-breaking condition: same distance, but lower color index
                elif new_dist == distance_grid[nr, nc]:
                    if current_color < output_grid[nr, nc]:
                        output_grid[nr, nc] = current_color
                        # Optimization: No need to re-add to queue if only tie-breaking, 
                        # as its neighbors have already been explored or will be explored 
                        # via other paths of the same minimum distance. If a shorter path
                        # was found later, it would handle propagation.
                        # queue.append((nr, nc)) # Re-adding might lead to cycles or redundant work

    # The output_grid now holds the final colored grid based on the expansion
    # Ensure any cell that wasn't reached (shouldn't happen if grid is connected or seeds exist) 
    # has a default value, though the logic should cover all cells reachable from seeds.
    # If the input grid could be entirely 0s and 1s, the output would remain -1. 
    # Based on examples, there are always seeds.
    # Let's handle the edge case where some original 0/1 cells might remain -1 if unreachable (though unlikely given examples)
    # A safe default might be 0, but the problem implies full coverage.
    # Check if any -1 remains and replace (e.g., with 0), although it shouldn't based on task structure
    output_grid[output_grid == -1] = 0 # Default to white if unreachable, though likely unnecessary

    return output_grid.tolist()
```