import numpy as np
from collections import deque

"""
Fill enclosed white regions (color 0) with a special color (4 or 7) found elsewhere in the grid.
An enclosed region is a contiguous area of white pixels that does not touch the grid border and is entirely surrounded by non-white pixels.
The special color (fill_color) is determined by finding the single pixel in the input grid with color 4 (yellow) or 7 (orange).
"""

def find_special_color(grid):
    """Finds the unique pixel with color 4 or 7."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 4 or grid[r, c] == 7:
                return grid[r, c]
    # Should not happen based on problem description, but return a default if needed
    return 0 

def find_enclosed_white_pixels(grid):
    """
    Identifies coordinates of white pixels belonging to enclosed regions.
    Uses a flood fill (BFS) starting from border white pixels. 
    Any white pixel NOT visited by this fill is considered enclosed.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    q = deque()

    # Add all border white pixels to the queue and mark as visited
    for r in range(rows):
        if grid[r, 0] == 0 and not visited[r, 0]:
            q.append((r, 0))
            visited[r, 0] = True
        if grid[r, cols - 1] == 0 and not visited[r, cols - 1]:
            q.append((r, cols - 1))
            visited[r, cols - 1] = True
    for c in range(cols):
        if grid[0, c] == 0 and not visited[0, c]:
            q.append((0, c))
            visited[0, c] = True
        if grid[rows - 1, c] == 0 and not visited[rows - 1, c]:
            q.append((rows - 1, c))
            visited[rows - 1, c] = True

    # Perform BFS (flood fill) from border white pixels
    while q:
        r, c = q.popleft()
        
        # Check 4 neighbours (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check bounds and if neighbour is white and not visited
            if 0 <= nr < rows and 0 <= nc < cols and \
               grid[nr, nc] == 0 and not visited[nr, nc]:
                visited[nr, nc] = True
                q.append((nr, nc))

    # Collect coordinates of white pixels NOT visited
    enclosed_pixels = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 0 and not visited[r, c]:
                enclosed_pixels.append((r, c))
                
    return enclosed_pixels

def transform(input_grid):
    """
    Transforms the input grid by finding enclosed white regions and filling them
    with a special color (4 or 7) present elsewhere in the grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    
    # 1. Find the special fill color (4 or 7)
    fill_color = find_special_color(input_np)
    
    # If no special color is found, return the original grid (shouldn't happen based on examples)
    if fill_color == 0: 
         return output_grid.tolist() # Convert back to list of lists

    # 2. Identify all white pixels belonging to enclosed regions
    enclosed_pixels = find_enclosed_white_pixels(input_np)
    
    # 3. Fill the identified enclosed pixels with the fill_color
    for r, c in enclosed_pixels:
        output_grid[r, c] = fill_color
        
    # Convert the result back to a list of lists for the required output format
    return output_grid.tolist()