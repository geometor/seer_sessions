"""
The transformation rule implements a flood fill algorithm originating from specific "seed" pixels and spreading into adjacent white pixels, bounded by gray pixels and other colored regions.

1. An output grid is initialized as a copy of the input grid.
2. "Seed" pixels are identified in the input grid. A seed pixel is any pixel whose color is not white (0) and not gray (5).
3. A queue is initialized for a Breadth-First Search (BFS).
4. For each seed pixel found at coordinates (r, c) with color 'fill_color':
    a. Add the tuple (r, c, fill_color) to the queue.
5. A set 'visited_white_cells' is initialized to keep track of the coordinates (row, column) of white cells that have already been filled. This prevents a white cell from being filled by multiple colors if it's adjacent to different seed regions.
6. Define the 4 cardinal directions (up, down, left, right) for neighbor checking. Diagonal neighbors are not considered.
7. While the queue is not empty:
    a. Dequeue a pixel's coordinates (r, c) and its associated fill_color.
    b. Examine the 4 cardinal neighbors of the pixel at (r, c).
    c. For each neighbor (nr, nc):
        i. Check if the neighbor is within the grid bounds.
        ii. Check if the neighbor pixel in the *input* grid is white (0). This ensures the fill only expands into originally white areas.
        iii. Check if the neighbor coordinates (nr, nc) have not already been added to the 'visited_white_cells' set.
        iv. If all conditions are met:
            1. Update the neighbor pixel's color in the output grid to fill_color.
            2. Add the neighbor's coordinates (nr, nc) to the 'visited_white_cells' set.
            3. Enqueue the neighbor's coordinates (nr, nc) and the fill_color to continue the fill from this new position.
8. The process continues until the queue is empty, meaning all reachable white cells adjacent to the initial seeds (respecting boundaries) have been filled.
9. The final modified output grid is returned.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Applies a 4-directional flood fill from non-white, non-gray pixels 
    into adjacent, originally white pixels, respecting gray and other colors as boundaries.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Get grid dimensions
    rows, cols = input_grid.shape
    
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Initialize the queue for BFS
    queue = deque()
    
    # Initialize a set to keep track of white cells that have been filled
    visited_white_cells = set()
    
    # Identify initial seed pixels and add them to the queue
    # Seed pixels are not white (0) and not gray (5)
    for r in range(rows):
        for c in range(cols):
            color = input_grid[r, c]
            if color != 0 and color != 5:
                # Add (row, col, color) to the queue for BFS starting points
                queue.append((r, c, color))
                # Note: We don't add the seed pixel itself to visited_white_cells,
                # as that set tracks *white* cells that get filled.

    # Define the 4 cardinal directions for neighbors (no diagonals)
    directions = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1)    # Right
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
                # Check if the neighbor is white (0) in the *input* grid
                # and has not been visited (filled) yet
                if input_grid[nr, nc] == 0 and (nr, nc) not in visited_white_cells:
                    # Update the neighbor's color in the output grid
                    output_grid[nr, nc] = fill_color
                    # Mark the neighbor white cell as visited (filled)
                    visited_white_cells.add((nr, nc))
                    # Enqueue the neighbor for further processing with the same fill_color
                    queue.append((nr, nc, fill_color))

    # Return the final transformed grid
    return output_grid