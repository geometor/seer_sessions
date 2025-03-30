```python
import numpy as np
from collections import deque

def transform(input_grid):
    """
    Fills empty space (color 0) in the grid based on proximity to 'seed' pixels 
    (color > 1) using Manhattan distance, treating 'wall' pixels (color 1) as 
    impassable barriers. This simulates a Voronoi diagram constrained by walls, 
    where regions are defined by the closest seed. Ties in distance are broken 
    by choosing the seed with the numerically lower color value.

    1. Identify Objects & Initialize: Copy the input grid to the output grid. 
       Locate all 'seed' pixels (colors 2-9). Create a distance grid 
       initialized with infinity and a queue for Breadth-First Search (BFS).
    2. Place Seeds: For each seed pixel at location (r, c) with color 
       `seed_color`, set its distance to 0 in the distance grid and add its 
       location to the BFS queue. The output grid already contains the seed color
       from the initial copy.
    3. Expand Colors (BFS): Perform a multi-source BFS. While the queue is not 
       empty, dequeue a location (r, c). For each valid neighbor (nr, nc):
        a. Validity Check: A neighbor is valid if it's within grid bounds AND 
           if the corresponding cell in the *input* grid is empty space (color 0).
        b. Calculate Distance: Calculate the new distance from the originating 
           seed via the current path (distance at (r, c) + 1).
        c. Update on Shorter Path: If the new distance is shorter than the 
           recorded distance for the neighbor (nr, nc), update the neighbor's 
           distance, set its color in the *output* grid to the color being 
           propagated (the color of the cell (r, c) in the output grid), and 
           enqueue the neighbor.
        d. Tie-Breaking: If the new distance is equal to the recorded distance 
           for the neighbor, compare the currently propagated color with the 
           neighbor's existing color in the output grid. If the current 
           propagated color is numerically smaller, update the neighbor's color 
           in the output grid.
    4. Return Output: Once the BFS is complete, the output grid contains the 
       filled regions constrained by the walls. Return this grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # 1. Initialize output grid as a copy of input, distance grid, and queue
    output_grid = input_grid_np.copy()
    distance_grid = np.full((height, width), float('inf'))
    queue = deque()

    # 2. Identify seeds and initialize BFS structures
    for r in range(height):
        for c in range(width):
            color = input_grid_np[r, c]
            # Seed pixels are those with color > 1
            if color > 1:
                distance_grid[r, c] = 0
                # Output grid already has the seed color due to copy
                queue.append((r, c))

    # Define neighbors (4-directional adjacency)
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    # 3. Perform BFS Expansion
    while queue:
        r, c = queue.popleft()
        current_dist = distance_grid[r, c]
        # The color being propagated is the one assigned to the current cell (r,c)
        # in the output grid (originating from its closest seed)
        propagated_color = output_grid[r, c] 

        # Explore neighbors
        for i in range(4):
            nr, nc = r + dr[i], c + dc[i]

            # 3a. Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                
                # 3a. Crucially, check if the neighbor cell in the *original* input 
                # was an empty space (0). Expansion only happens into empty cells.
                if input_grid_np[nr, nc] == 0:
                    
                    # 3b. Calculate distance from the originating seed via current path
                    new_dist = current_dist + 1

                    # 3c. Check if this path is shorter than any previous path to (nr, nc)
                    if new_dist < distance_grid[nr, nc]:
                        distance_grid[nr, nc] = new_dist
                        output_grid[nr, nc] = propagated_color # Assign color
                        queue.append((nr, nc))
                    # 3d. Check for tie-breaking condition: same distance
                    elif new_dist == distance_grid[nr, nc]:
                        # Update color only if the current propagated color is smaller
                        # than the color currently assigned to the neighbor
                        if propagated_color < output_grid[nr, nc]:
                            output_grid[nr, nc] = propagated_color
                            # No need to re-add to queue if only tie-breaking color update occurred

    # 4. Return Output
    # The output grid was initialized with walls (1) and seeds (>1). 
    # BFS only overwrites empty cells (0). Unreachable empty cells remain 0.
    return output_grid.tolist()
```