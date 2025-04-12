"""
Transformation Rule:

1.  Create the output grid as an exact copy of the input grid.
2.  Identify all white (0) pixels located on the grid boundary (edges).
3.  Perform a flood fill (BFS) operation starting from these boundary white pixels.
4.  The fill color is yellow (4).
5.  The fill spreads only to adjacent (up, down, left, right) white (0) pixels within the grid bounds.
6.  Non-white pixels act as barriers, stopping the fill propagation.
7.  All white pixels reachable from the boundary via this flood fill are changed to yellow (4) in the output grid.
8.  Original non-white shapes and unreachable white pixels remain unchanged.

Note: This implementation reflects the standard flood fill approach described. As noted in the analysis phase, this specific logic did not perfectly match all training example outputs, suggesting a more nuanced rule might be required. However, this code represents the current best interpretation based on the NLP.
"""

import copy
from collections import deque

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Fills the white areas (0) connected to the boundary with yellow (4),
    stopping at non-white pixels.
    """
    
    # Initialize output_grid as a deep copy of the input grid
    output_grid = copy.deepcopy(input_grid)
    
    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Define fill color and background color
    fill_color = 4
    background_color = 0

    # Initialize a queue for the flood fill (BFS)
    queue = deque()

    # Identify boundary white pixels and add them to the queue
    # Also, immediately color them in the output grid to mark as visited/source
    # This prevents adding the same starting pixel multiple times if it's a corner
    for r in range(height):
        for c in range(width):
            # Check if the pixel is on the boundary
            is_boundary = (r == 0 or r == height - 1 or c == 0 or c == width - 1)
            
            # If it's a white pixel on the boundary AND hasn't been processed yet
            if is_boundary and output_grid[r][c] == background_color:
                 # Change color to fill color (mark as visited and source)
                 output_grid[r][c] = fill_color
                 # Add to the queue for processing neighbors
                 queue.append((r, c))

    # Define 4-way adjacent neighbors (dr, dc) for movement
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up

    # Perform the flood fill using BFS
    while queue:
        r, c = queue.popleft() # Get the next pixel to process

        # Explore its neighbors
        for dr, dc in neighbors:
            nr, nc = r + dr, c + dc # Calculate neighbor coordinates

            # Check if the neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is a background pixel (unvisited)
                # We check output_grid because visited pixels are already colored yellow
                if output_grid[nr][nc] == background_color:
                    # Change color to fill color (mark as visited)
                    output_grid[nr][nc] = fill_color
                    # Add neighbor to the queue to process its neighbors later
                    queue.append((nr, nc))

    # Return the modified grid
    return output_grid