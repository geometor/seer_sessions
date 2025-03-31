import numpy as np
from collections import deque

"""
Transforms the input grid by finding all non-green pixels enclosed by green (3) 
walls and changing their color to azure (8). Enclosure is determined by 
reachability from the grid border: pixels are reachable if a path of non-green 
pixels connects them to the border. Unreachable, non-green pixels are filled. 
Green pixels and reachable non-green pixels remain unchanged.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Fills enclosed non-green regions with azure (8).

    Args:
        input_grid: A 2D list of integers representing the input grid colors.

    Returns:
        A 2D list of integers representing the transformed output grid.
    """
    # Convert input to numpy array for efficient operations
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    
    # Create the output grid as a copy of the input grid initially
    output_grid = grid.copy()
    
    # Create a boolean grid to track reachable cells, initialized to False
    reachable = np.zeros((height, width), dtype=bool)
    
    # Define wall color (boundary) and fill color
    wall_color = 3 # green
    fill_color = 8 # azure

    # Initialize a queue for Breadth-First Search (BFS)
    queue = deque()

    # --- Step 1: Seed the BFS from border cells ---
    # Iterate through all border cells
    for r in range(height):
        for c in range(width):
            is_border = r == 0 or r == height - 1 or c == 0 or c == width - 1
            if is_border:
                # If a border cell is not a wall, mark it reachable and add to queue
                if grid[r, c] != wall_color:
                    if not reachable[r, c]: # Avoid adding duplicates if corners are processed twice
                        reachable[r, c] = True
                        queue.append((r, c))

    # --- Step 2: Perform BFS to find all reachable non-wall cells ---
    while queue:
        r, c = queue.popleft()

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is not a wall and not already marked reachable
                if grid[nr, nc] != wall_color and not reachable[nr, nc]:
                    reachable[nr, nc] = True
                    queue.append((nr, nc))

    # --- Step 3: Fill unreachable non-wall cells in the output grid ---
    # Iterate through every cell in the grid
    for r in range(height):
        for c in range(width):
            # Check if the cell was NOT reached by BFS
            if not reachable[r, c]:
                # Check if the original cell color was NOT the wall color
                if grid[r, c] != wall_color:
                    # Fill this enclosed, non-wall cell with the fill color
                    output_grid[r, c] = fill_color
                    
    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()