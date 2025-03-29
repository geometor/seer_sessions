import numpy as np
from collections import deque

"""
Perform a flood fill operation originating conceptually from the location of the 
single gray pixel (color 5). The fill uses yellow (color 4) and only affects 
white pixels (color 0). Red pixels (color 2) act as impenetrable boundaries for 
the fill. The original gray pixel and all red pixels remain unchanged in the 
output. The fill spreads cardinally (up, down, left, right).
"""

def find_pixel(grid, color):
    """Finds the first occurrence of a pixel with the given color."""
    coords = np.argwhere(grid == color)
    if len(coords) > 0:
        return tuple(coords[0])
    return None

def transform(input_grid):
    """
    Applies a flood fill starting from the gray pixel, bounded by red pixels.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A numpy array representing the transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    height, width = grid.shape

    # Define colors
    background_color = 0 # white
    boundary_color = 2   # red
    start_pixel_color = 5 # gray
    fill_color = 4       # yellow

    # Find the starting pixel location
    start_coord = find_pixel(grid, start_pixel_color)
    if start_coord is None:
        # Should not happen based on examples, but good practice
        return output_grid 

    # Initialize queue for Breadth-First Search (BFS) flood fill
    # and a set to keep track of visited coordinates
    queue = deque()
    visited = set()

    # Add initial neighbours of the start coordinate to the queue if they are white
    start_row, start_col = start_coord
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = start_row + dr, start_col + dc

        # Check bounds
        if 0 <= nr < height and 0 <= nc < width:
            # Check if the neighbor is the target color (white)
            if grid[nr, nc] == background_color:
                if (nr, nc) not in visited:
                    output_grid[nr, nc] = fill_color
                    visited.add((nr, nc))
                    queue.append((nr, nc))

    # Perform flood fill using BFS
    while queue:
        r, c = queue.popleft()

        # Explore neighbors (cardinal directions)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor hasn't been visited
                if (nr, nc) not in visited:
                    # Check if the neighbor is the background color (fillable)
                    if grid[nr, nc] == background_color:
                        # Change color in the output grid
                        output_grid[nr, nc] = fill_color
                        # Mark as visited
                        visited.add((nr, nc))
                        # Add to queue for further exploration
                        queue.append((nr, nc))
                    # Also mark boundary cells as visited conceptually to prevent re-checking neighbours from them
                    elif grid[nr, nc] == boundary_color:
                         visited.add((nr, nc)) # Mark boundary as visited to avoid checking its neighbours again from other paths

    # Ensure the original start pixel remains unchanged (already handled by copy and fill logic only targeting background)
    # output_grid[start_row, start_col] = start_pixel_color 
    
    return output_grid.tolist() # Return as list of lists if required by framework