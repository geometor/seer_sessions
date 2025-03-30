"""
Identify regions of white (0) pixels completely enclosed by blue (1) pixels. 
Fill these enclosed regions with azure (8).
Then, find all white (0) pixels in the original input that are directly adjacent (up, down, left, right) to any part of the filled enclosed regions. 
Change these adjacent white pixels to azure (8) as well. 
Keep the original blue (1) frame pixels unchanged.
"""

import numpy as np
from collections import deque

def find_enclosed_regions(grid):
    """
    Finds all white (0) pixels enclosed by non-white pixels using flood fill.
    Starts flood fill from border white pixels. Any white pixel not visited
    by these fills is considered enclosed.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    q = deque()

    # Add all border white pixels to the queue and mark as visited
    for r in range(rows):
        for c in [0, cols - 1]:
            if grid[r, c] == 0 and not visited[r, c]:
                q.append((r, c))
                visited[r, c] = True
    for c in range(cols):
        for r in [0, rows - 1]:
             if grid[r, c] == 0 and not visited[r, c]:
                # Check again in case corner was already added
                if not visited[r,c]: 
                    q.append((r, c))
                    visited[r, c] = True

    # Perform BFS (flood fill) from border white pixels
    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and \
               grid[nr, nc] == 0 and not visited[nr, nc]:
                visited[nr, nc] = True
                q.append((nr, nc))

    # Identify enclosed pixels (white pixels not visited by the flood fill)
    interior_set = set()
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 0 and not visited[r, c]:
                interior_set.add((r, c))
                
    return interior_set

def find_adjacent_to_set(grid, target_set):
    """
    Finds white (0) pixels in the grid that are adjacent (non-diagonally)
    to any pixel coordinate in the target_set.
    """
    rows, cols = grid.shape
    adjacent_set = set()
    
    for r, c in target_set:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds and if the neighbor is white(0) in the original grid
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 0:
                 # Crucially, ensure the adjacent pixel is NOT part of the interior itself
                 if (nr, nc) not in target_set:
                    adjacent_set.add((nr, nc))
                    
    return adjacent_set


def transform(input_grid):
    """
    Applies the transformation: fills enclosed white areas and adjacent white
    pixels with azure (8).
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    
    # Initialize output_grid as a copy of the input
    output_grid = input_array.copy()
    
    # 1. Find all groups of connected white (0) pixels completely enclosed by blue (1) pixels
    interior_set = find_enclosed_regions(input_array)

    # 2. Find all white pixels adjacent to the interior set
    adjacent_set = find_adjacent_to_set(input_array, interior_set)

    # 3. Modify the output grid: Fill interior regions with azure (8)
    for r, c in interior_set:
        output_grid[r, c] = 8

    # 4. Modify the output grid: Fill adjacent white pixels with azure (8)
    for r, c in adjacent_set:
         output_grid[r, c] = 8
         
    # Convert back to list of lists for the required output format
    return output_grid.tolist()