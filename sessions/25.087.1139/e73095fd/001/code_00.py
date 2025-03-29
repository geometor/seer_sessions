import numpy as np
from collections import deque

"""
Identify all contiguous regions of white (0) pixels in the input grid.
For each white region, determine if it is fully enclosed by gray (5) pixels. 
A region is considered enclosed if none of its pixels can reach any edge of the grid 
by moving only through adjacent (up, down, left, right) white pixels without crossing a gray pixel.
Create the output grid by copying the input grid.
For every identified enclosed white region, change the color of all pixels within that region 
from white (0) to yellow (4) in the output grid.
Leave all other pixels (gray pixels and non-enclosed white pixels) unchanged.
"""

def transform(input_grid):
    """
    Fills white (0) regions enclosed by gray (5) pixels with yellow (4).

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy() # Start with a copy of the input
    rows, cols = grid.shape

    # Create a boolean grid to keep track of visited white pixels connected to the outside
    visited = np.zeros((rows, cols), dtype=bool)
    
    # Use a queue for Breadth-First Search (BFS)
    q = deque()

    # Find all white (0) pixels on the border and start BFS from them
    for r in range(rows):
        for c in range(cols):
            # Check if it's a border pixel
            is_border = (r == 0 or r == rows - 1 or c == 0 or c == cols - 1)
            # If it's a white pixel on the border and not visited yet
            if is_border and grid[r, c] == 0 and not visited[r, c]:
                q.append((r, c))
                visited[r, c] = True

    # Define the four cardinal directions for neighbors
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Perform BFS to find all white pixels connected to the border
    while q:
        r, c = q.popleft()

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # If the neighbor is white (0) and hasn't been visited
                if grid[nr, nc] == 0 and not visited[nr, nc]:
                    visited[nr, nc] = True
                    q.append((nr, nc))

    # Iterate through the grid and fill enclosed white regions
    for r in range(rows):
        for c in range(cols):
            # If a pixel is white (0) but was not visited by the BFS (meaning it's not connected to the border)
            if grid[r, c] == 0 and not visited[r, c]:
                # Change its color to yellow (4) in the output grid
                output_grid[r, c] = 4

    # Convert back to list of lists for the required output format
    return output_grid.tolist()