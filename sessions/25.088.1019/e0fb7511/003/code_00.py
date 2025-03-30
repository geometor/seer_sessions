"""
Identify contiguous regions of white pixels (0). If a region does not touch any of the grid's borders, change all pixels in that region to azure (8). Otherwise, leave the white pixels as they are. Blue pixels (1) remain unchanged.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Transforms the input grid by finding enclosed white regions (not touching borders) 
    and coloring them azure (8).

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input_grid to numpy array for easier manipulation
    input_grid_np = np.array(input_grid)
    
    # Initialize output_grid as a copy of the input grid
    output_grid = input_grid_np.copy()
    
    # Get grid dimensions
    height, width = input_grid_np.shape
    
    # Create a boolean grid to keep track of visited pixels during BFS
    visited = np.zeros((height, width), dtype=bool)

    # Iterate through each pixel of the grid
    for r in range(height):
        for c in range(width):
            # Check if the pixel is white (0) and has not been visited yet
            if input_grid_np[r, c] == 0 and not visited[r, c]:
                # Start a Breadth-First Search (BFS) to find the connected white region
                queue = deque([(r, c)])
                region_pixels = []  # Store coordinates of pixels in the current region
                touches_border = False  # Flag to check if the region touches any border

                # Mark the starting pixel as visited
                visited[r, c] = True

                # --- BFS to find the connected white region ---
                while queue:
                    curr_r, curr_c = queue.popleft()
                    region_pixels.append((curr_r, curr_c))

                    # Check if the current pixel is on the border
                    if curr_r == 0 or curr_r == height - 1 or curr_c == 0 or curr_c == width - 1:
                        touches_border = True

                    # Explore cardinal neighbors (up, down, left, right)
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check if neighbor is within bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check if neighbor is white and not yet visited
                            if input_grid_np[nr, nc] == 0 and not visited[nr, nc]:
                                visited[nr, nc] = True
                                queue.append((nr, nc))
                
                # --- Color the region if it doesn't touch the border ---
                # If the entire region was explored and it never touched a border
                if not touches_border:
                    # Change all pixels in this region to azure (8) in the output grid
                    for reg_r, reg_c in region_pixels:
                        output_grid[reg_r, reg_c] = 8
                # Otherwise (if touches_border is True), the pixels remain white (0)
                # as they were initialized in the output_grid copy.

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()