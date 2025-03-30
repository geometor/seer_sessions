"""
Flood fill a connected area of white (0) pixels starting from a single red (2) pixel, treating azure (8) pixels as barriers. The fill propagates horizontally and vertically to adjacent white pixels. The original red pixel and all azure pixels remain unchanged. The filled area in the output grid becomes red (2).
"""

import collections
import copy

def transform(input_grid):
    """
    Applies a flood fill starting from a red pixel (2), filling adjacent white 
    pixels (0) with red (2), bounded by azure pixels (8).

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Create a deep copy of the input grid to modify
    output_grid = [row[:] for row in input_grid] 
    
    height = len(input_grid)
    width = len(input_grid[0])
    
    # Find the starting red pixel coordinates
    start_coord = None
    for r in range(height):
        for c in range(width):
            if input_grid[r][c] == 2:
                start_coord = (r, c)
                break
        if start_coord:
            break
            
    if not start_coord:
        # Should not happen based on task description, but handle defensively
        return output_grid 

    # Initialize the queue for Breadth-First Search (BFS) flood fill
    queue = collections.deque([start_coord])
    # Keep track of visited coordinates to avoid cycles and redundant checks
    # Initialize with the start coordinate as it's already processed (or the origin)
    visited = {start_coord} 

    # Define the four cardinal directions for neighbors
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # right, left, down, up

    # Perform the flood fill
    while queue:
        r, c = queue.popleft()

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor has not been visited
                if (nr, nc) not in visited:
                    # Check if the neighbor is a white pixel (fillable) in the original grid
                    if input_grid[nr][nc] == 0:
                        # Mark as visited
                        visited.add((nr, nc))
                        # Change the color in the output grid to red
                        output_grid[nr][nc] = 2
                        # Add the neighbor to the queue to explore from it
                        queue.append((nr, nc))
                    # Also mark barriers as visited so we don't reconsider them
                    elif input_grid[nr][nc] == 8:
                         visited.add((nr, nc))
                         
    return output_grid