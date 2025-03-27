"""
The transformation rule implements a flood fill algorithm originating from specific "seed" pixels. 
1. An output grid is initialized as a copy of the input grid.
2. "Seed" pixels are identified in the input grid. A seed pixel is any pixel whose color is not white (0) and not gray (5).
3. A queue is initialized with the coordinates (row, column) and color of each seed pixel.
4. A set is initialized to keep track of visited coordinates (initially containing seed pixel coordinates) to prevent reprocessing.
5. While the queue is not empty:
    a. Dequeue a pixel's coordinates (r, c) and its associated fill_color.
    b. Examine all 8 neighbors (including diagonals) of the pixel at (r, c).
    c. For each neighbor (nr, nc):
        i. Check if the neighbor is within the grid bounds.
        ii. Check if the neighbor pixel in the output grid is currently white (0).
        iii. Check if the neighbor coordinates (nr, nc) have not already been visited.
        iv. If all conditions are met:
            1. Update the neighbor pixel's color in the output grid to fill_color.
            2. Add the neighbor's coordinates (nr, nc) to the visited set.
            3. Enqueue the neighbor's coordinates (nr, nc) and the fill_color.
6. The process continues until the queue is empty, at which point the modified output grid is returned.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Applies a flood fill from non-white, non-gray pixels into adjacent white pixels.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Get grid dimensions
    rows, cols = input_grid.shape
    
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Initialize the queue for BFS and the visited set
    queue = deque()
    visited = set()
    
    # Identify initial seed pixels and add them to the queue and visited set
    for r in range(rows):
        for c in range(cols):
            color = input_grid[r, c]
            # Seed pixels are not white (0) and not gray (5)
            if color != 0 and color != 5:
                # Add (row, col, color) to the queue
                queue.append((r, c, color))
                # Add (row, col) to the visited set
                visited.add((r, c))

    # Define the 8 directions for neighbors (including diagonals)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Perform the flood fill using BFS
    while queue:
        # Dequeue the current pixel's info
        r, c, fill_color = queue.popleft()

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor is white (0) in the output grid
                # and has not been visited yet
                if output_grid[nr, nc] == 0 and (nr, nc) not in visited:
                    # Update the neighbor's color in the output grid
                    output_grid[nr, nc] = fill_color
                    # Mark the neighbor as visited
                    visited.add((nr, nc))
                    # Enqueue the neighbor for further processing
                    queue.append((nr, nc, fill_color))

    # Return the final transformed grid
    return output_grid