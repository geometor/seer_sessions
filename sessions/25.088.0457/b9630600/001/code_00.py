import numpy as np
from collections import deque

"""
Identify all distinct, contiguous green shapes (color 3) in the input grid.
For each green shape, determine if it forms a closed boundary enclosing a region of white pixels (color 0).
Locate all white pixels that are inside the enclosed region of each identified closed boundary shape. 
A pixel is considered "inside" if it is white and cannot reach the edge of the grid by moving horizontally or vertically through only white pixels without crossing the green boundary of the shape.
Create the output grid by copying the input grid.
Modify the output grid by changing the color of all identified interior white pixels to green (color 3).
"""

def find_exterior_white_pixels(grid, background_color=0):
    """
    Finds all background_color pixels connected to the grid boundary using BFS.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color representing the background/exterior.

    Returns:
        set: A set of (row, col) tuples representing exterior background pixels.
    """
    rows, cols = grid.shape
    exterior_pixels = set()
    queue = deque()
    
    # Add all background pixels on the border to the queue and visited set
    for r in range(rows):
        if grid[r, 0] == background_color and (r, 0) not in exterior_pixels:
            queue.append((r, 0))
            exterior_pixels.add((r, 0))
        if grid[r, cols - 1] == background_color and (r, cols - 1) not in exterior_pixels:
            queue.append((r, cols - 1))
            exterior_pixels.add((r, cols - 1))
            
    for c in range(cols):
        if grid[0, c] == background_color and (0, c) not in exterior_pixels:
            queue.append((0, c))
            exterior_pixels.add((0, c))
        if grid[rows - 1, c] == background_color and (rows - 1, c) not in exterior_pixels:
             queue.append((rows - 1, c))
             exterior_pixels.add((rows - 1, c))

    # Perform BFS from the border background pixels
    while queue:
        r, c = queue.popleft()
        
        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check if neighbor is within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is background color and not already visited
                if grid[nr, nc] == background_color and (nr, nc) not in exterior_pixels:
                    exterior_pixels.add((nr, nc))
                    queue.append((nr, nc))
                    
    return exterior_pixels

def transform(input_grid):
    """
    Fills the interior of closed shapes made of green (3) pixels with green (3).
    The interior is defined as white (0) pixels not connected to the grid boundary
    without crossing a green pixel.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = input_grid_np.copy()
    rows, cols = input_grid_np.shape
    
    boundary_color = 3 # green
    background_color = 0 # white
    fill_color = 3 # green
    
    # Find all white pixels connected to the boundary (exterior white pixels)
    exterior_white = find_exterior_white_pixels(input_grid_np, background_color)
    
    # Iterate through the grid
    for r in range(rows):
        for c in range(cols):
            # If a pixel is white (background_color) and is NOT in the exterior set
            # it must be an interior white pixel.
            if input_grid_np[r, c] == background_color and (r, c) not in exterior_white:
                # Fill this interior pixel with the fill_color (green)
                output_grid[r, c] = fill_color
                
    # Convert back to list of lists for the required output format
    return output_grid.tolist()