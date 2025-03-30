import numpy as np
from collections import deque

"""
Performs a flood fill operation on the input grid.
The fill originates from all blue (1) pixels simultaneously.
It spreads into orthogonally adjacent white (0) pixels.
The fill is blocked by gray (5) pixels, azure (8) pixels, and the grid boundaries.
Blue (1), gray (5), and azure (8) pixels in the input remain unchanged in the output.
Only white (0) pixels reachable from a blue (1) pixel without crossing a boundary are changed to blue (1).
"""

def transform(input_grid):
    """
    Transforms the input grid by performing a flood fill operation starting from
    blue (1) pixels. The fill spreads through adjacent white (0) pixels and is
    blocked by gray (5) and azure (8) pixels, as well as the grid boundaries.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """

    # Convert input list of lists to a NumPy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    # Initialize the output grid as a copy of the input grid
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # Define fill color, target color, and boundary colors
    fill_color = 1          # Blue
    target_color = 0        # White
    boundary_colors = {5, 8} # Gray and Azure

    # Initialize a queue for Breadth-First Search (BFS)
    queue = deque()
    # Initialize a set to keep track of visited locations to prevent cycles and re-processing
    visited = set()

    # Find initial seed locations (pixels with value 1) and add them to the queue and visited set
    for r in range(height):
        for c in range(width):
            if input_np[r, c] == fill_color:
                seed_location = (r, c)
                if seed_location not in visited:
                    queue.append(seed_location)
                    visited.add(seed_location)

    # Perform the flood fill using BFS
    while queue:
        r, c = queue.popleft()

        # Explore orthogonal neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            neighbor_location = (nr, nc)

            # Check if the neighbor is within the grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor location has already been visited
                if neighbor_location not in visited:
                    # Mark the neighbor as visited regardless of its color to avoid re-checking
                    visited.add(neighbor_location)

                    # Check the color of the neighbor pixel in the *input* grid
                    neighbor_color = input_np[nr, nc]

                    # If the neighbor is the target color (white), fill it and add to queue
                    if neighbor_color == target_color:
                        output_np[nr, nc] = fill_color
                        queue.append(neighbor_location)
                    # If the neighbor is a boundary color, it stops the fill in this direction
                    # but is marked visited. No action needed here as it's already added to visited.
                    # elif neighbor_color in boundary_colors:
                    #     pass # Boundary blocks fill, already marked visited
                    # If the neighbor is already the fill color, it means it's part of another
                    # seed or already filled region. Already marked visited.
                    # elif neighbor_color == fill_color:
                    #     pass # Already fill color, already marked visited

    # Convert the resulting NumPy array back to a list of lists
    output_grid = output_np.tolist()
    return output_grid
