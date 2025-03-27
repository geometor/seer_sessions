import numpy as np
from collections import deque

"""
Identifies white (0) pixels enclosed by blue (1) or red (2) pixels (or grid boundaries) and changes them to yellow (4).
White pixels connected to the grid edge (without crossing blue or red pixels) remain white.

1. Initialize the output grid as a copy of the input grid.
2. Define boundary colors: blue (1) and red (2).
3. Find all white (0) pixels connected to the grid edges using a flood fill (BFS) algorithm, considering diagonal adjacency. These are the 'outside' or 'reachable' white pixels. Store their coordinates.
4. Iterate through the grid. If a pixel is white (0) and its coordinates were *not* found in the 'reachable' set from step 3, change its color to yellow (4) in the output grid.
5. Keep all blue (1), red (2), and 'reachable' white (0) pixels unchanged.
6. Return the modified output grid.
"""

def transform(input_grid):
    """
    Transforms the input grid by filling enclosed white areas with yellow.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    # Define boundary colors
    boundary_colors = {1, 2} # blue, red
    fill_color = 4 # yellow
    background_color = 0 # white

    # Initialize structures for BFS
    reachable_white_pixels = set()
    queue = deque()

    # Add initial white pixels from the edges to the queue and reachable set
    for r in range(height):
        for c in [0, width - 1]: # Left and right edges
            if input_grid[r, c] == background_color:
                if (r, c) not in reachable_white_pixels:
                    reachable_white_pixels.add((r, c))
                    queue.append((r, c))
    for c in range(width): 
        for r in [0, height - 1]: # Top and bottom edges (avoid double-adding corners)
             if input_grid[r, c] == background_color:
                if (r, c) not in reachable_white_pixels:
                    reachable_white_pixels.add((r, c))
                    queue.append((r, c))

    # Perform Breadth-First Search (BFS) to find all reachable white pixels
    while queue:
        r, c = queue.popleft()

        # Check all 8 neighbors (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue # Skip the pixel itself

                nr, nc = r + dr, c + dc

                # Check if the neighbor is within bounds
                if 0 <= nr < height and 0 <= nc < width:
                    # Check if the neighbor is white and not already visited/queued
                    # Also ensure it's not a boundary color (though the primary check is for background_color)
                    if input_grid[nr, nc] == background_color and (nr, nc) not in reachable_white_pixels:
                        reachable_white_pixels.add((nr, nc))
                        queue.append((nr, nc))

    # Iterate through the grid and fill the enclosed white pixels
    for r in range(height):
        for c in range(width):
            # If a pixel is white but not reachable from the edge, fill it
            if input_grid[r, c] == background_color and (r, c) not in reachable_white_pixels:
                output_grid[r, c] = fill_color

    return output_grid