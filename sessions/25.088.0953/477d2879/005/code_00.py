import numpy as np
from collections import deque

def transform(input_grid):
    """
    Fills the entire grid based on proximity to 'seed' pixels (color > 1) using 
    Manhattan distance. This simulates a Voronoi diagram where regions are defined 
    by the closest seed. Ties in distance are broken by choosing the seed with the 
    numerically lower color value. Input pixels with color 0 (white) or 1 (blue) 
    act as empty space and do not block the expansion.

    1. Identify Seed Pixels: Locate all pixels in the input grid that have a 
       color value greater than 1 (colors 2 through 9). These are the seeds.
    2. Initialize Grids and Queue: Create a distance grid initialized with 
       infinity, an output grid initialized with a placeholder (e.g., -1), 
       and a queue for Breadth-First Search (BFS).
    3. Place Seeds: For each seed pixel at location (r, c) with color 
       `seed_color`, set its distance to 0, its color in the output grid to 
       `seed_color`, and add its location to the BFS queue.
    4. Expand Colors (BFS): Perform a multi-source BFS. While the queue is not 
       empty, dequeue a location. For each valid neighbor:
        a. Calculate the new distance (current distance + 1).
        b. If the new distance is shorter than the recorded distance for the 
           neighbor, update the neighbor's distance and color (to the current 
           propagated color) and enqueue the neighbor.
        c. If the new distance is equal to the recorded distance (a tie), compare 
           the currently propagated color with the neighbor's existing color. 
           If the current color is numerically smaller, update the neighbor's color.
    5. Return Output: Once the BFS is complete, the output grid contains the 
       final colored regions. Return this grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # Initialize distance grid with infinity and output grid with a placeholder (-1)
    distance_grid = np.full((height, width), float('inf'))
    output_grid = np.full((height, width), -1, dtype=int)

    # Use a deque for BFS queue
    queue = deque()

    # 1. & 3. Identify seeds and initialize BFS structures
    for r in range(height):
        for c in range(width):
            color = input_grid_np[r, c]
            # Seed pixels are those with color > 1
            if color > 1:
                distance_grid[r, c] = 0
                output_grid[r, c] = color
                queue.append((r, c))

    # Define neighbors (4-directional adjacency)
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    # 4. Perform BFS Expansion
    while queue:
        r, c = queue.popleft()
        current_dist = distance_grid[r, c]
        # The color being propagated originates from the seed that claimed (r,c)
        current_color = output_grid[r, c] 

        # Explore neighbors
        for i in range(4):
            nr, nc = r + dr[i], c + dc[i]

            # Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                
                # Calculate distance from the originating seed via current path
                new_dist = current_dist + 1

                # 4.b Check if this path is shorter than any previous path to (nr, nc)
                if new_dist < distance_grid[nr, nc]:
                    distance_grid[nr, nc] = new_dist
                    output_grid[nr, nc] = current_color
                    queue.append((nr, nc))
                # 4.c Check for tie-breaking condition: same distance
                elif new_dist == distance_grid[nr, nc]:
                    # Update color only if the current seed's color is smaller
                    # than the color currently assigned to the neighbor
                    if current_color < output_grid[nr, nc]:
                        output_grid[nr, nc] = current_color
                        # No need to re-add to queue if only tie-breaking color update

    # 5. Return Output
    # Assuming the grid is always fully connected or seeds exist, 
    # all -1 placeholders should be overwritten. If not, defaulting to 0 might
    # be needed, but based on examples, the grid gets fully colored.
    # output_grid[output_grid == -1] = 0 # Optional: Default unreachable to white

    return output_grid.tolist()