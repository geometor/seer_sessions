```python
import numpy as np
from collections import deque

"""
Identifies source pixels (blue=1, red=2) and wall pixels (gray=5).
Fills background pixels (white=0) with the color of the nearest source pixel.
Distance is calculated using Manhattan distance, considering walls as impassable barriers.
A multi-source Breadth-First Search (BFS) is performed starting simultaneously from all source pixels.
Each white pixel adopts the color of the first source pixel to reach it via the shortest path.
Pixels that are not white (0), blue (1), red (2), or gray (5) remain unchanged (though none are present in the examples).
Blue, red, and gray pixels from the input remain unchanged in the output.
"""

def transform(input_grid):
    """
    Fills white areas based on the nearest blue or red source, blocked by gray walls.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_grid = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # Get grid dimensions
    height, width = input_grid.shape

    # Define colors
    WHITE = 0
    BLUE = 1
    RED = 2
    GRAY = 5

    # Initialize distance grid with infinity
    distance_grid = np.full((height, width), float('inf'), dtype=float)
    # Initialize color grid to store the color of the nearest source
    # Use -1 to indicate no source has reached this cell yet
    color_grid = np.full((height, width), -1, dtype=int)

    # Initialize a queue for BFS
    q = deque()

    # Find all source pixels (blue and red) and add them to the queue
    for r in range(height):
        for c in range(width):
            if input_grid[r, c] == BLUE or input_grid[r, c] == RED:
                distance_grid[r, c] = 0
                color_grid[r, c] = input_grid[r, c]
                q.append((r, c))

    # Define possible moves (Manhattan distance neighbors: up, down, left, right)
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Perform multi-source BFS
    while q:
        r, c = q.popleft()
        current_dist = distance_grid[r, c]
        source_color = color_grid[r, c] # Color propagated from the original source

        # Explore neighbors
        for dr, dc in moves:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if neighbor is not a wall
                if input_grid[nr, nc] != GRAY:
                    # Check if this path is shorter than any previously found path
                    # We only update if the new distance is strictly smaller.
                    # This implicitly handles ties: the first source to reach a cell claims it.
                    if current_dist + 1 < distance_grid[nr, nc]:
                        distance_grid[nr, nc] = current_dist + 1
                        # Important: Propagate the color of the *original* source that initiated this path.
                        # Since color_grid[r,c] already holds the correct originating source color, we use that.
                        color_grid[nr, nc] = source_color 
                        q.append((nr, nc))

    # Fill the white cells in the output grid based on the BFS results
    for r in range(height):
        for c in range(width):
            # If the original cell was white and a source was reachable
            if input_grid[r, c] == WHITE and color_grid[r, c] != -1:
                output_grid[r, c] = color_grid[r, c]

    return output_grid.tolist() # Return as list of lists, matching input format if needed

```