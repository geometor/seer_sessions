"""
Identifies enclosed white regions within an azure boundary in the input grid and fills them with azure. The transformation rule involves:
1. Finding all white pixels reachable from the grid borders without crossing azure pixels (exterior white pixels) using a flood fill (BFS) algorithm starting from border white pixels. 8-directional connectivity (including diagonals) is used.
2. Creating an output grid where:
   - Original azure pixels (8) from the input become white (0) in the output.
   - Exterior white pixels (0) from the input (those reachable from the border) remain white (0) in the output.
   - Interior white pixels (0) from the input (those *not* reachable from the border) become azure (8) in the output.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Transforms the input grid by filling enclosed white regions with azure.

    Args:
        input_grid (list[list[int]]): A 2D list of integers representing the input grid.

    Returns:
        list[list[int]]: A 2D list of integers representing the transformed output grid.
    """
    # Convert input to NumPy array for efficient operations
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    
    # Initialize a boolean grid to track visited white cells reachable from the border
    visited = np.zeros_like(input_grid_np, dtype=bool)
    
    # Initialize a queue for Breadth-First Search (BFS)
    queue = deque()

    # Define 8-directional neighbors (relative coordinates)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # 1. Seed the queue with white border pixels
    # Iterate through all border cells
    for r in range(height):
        for c in range(width):
            # Check if the cell is on the border
            if r == 0 or r == height - 1 or c == 0 or c == width - 1:
                # Check if the border cell is white (0) and hasn't been visited yet
                if input_grid_np[r, c] == 0 and not visited[r, c]:
                    visited[r, c] = True  # Mark as visited
                    queue.append((r, c)) # Add to the queue for BFS

    # 2. Perform Flood Fill (BFS) from the border white pixels
    while queue:
        r, c = queue.popleft() # Get the next cell to process

        # Explore its 8 neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within the grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is white (0) and hasn't been visited yet
                if input_grid_np[nr, nc] == 0 and not visited[nr, nc]:
                    visited[nr, nc] = True # Mark neighbor as visited
                    queue.append((nr, nc)) # Add neighbor to the queue

    # 3. Construct the output grid based on the flood fill results
    # Initialize output grid with the same dimensions, default value can be 0
    output_grid = np.zeros_like(input_grid_np, dtype=int)
    
    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Rule 1: If input is azure (8), output is white (0)
            if input_grid_np[r, c] == 8:
                output_grid[r, c] = 0
            # Rule 2: If input is white (0)
            elif input_grid_np[r, c] == 0:
                # Check if it was visited (reachable from border - exterior)
                if visited[r, c]:
                    output_grid[r, c] = 0 # Exterior white remains white
                # If not visited (not reachable from border - interior)
                else:
                    output_grid[r, c] = 8 # Interior white becomes azure
            # Optional: handle other unexpected colors if necessary, though examples only show 0 and 8.
            # else: output_grid[r, c] = input_grid_np[r, c] # Keep original color? Defaulting to 0 is safer.

    # Convert the final NumPy array back to a list of lists for the expected output format
    return output_grid.tolist()