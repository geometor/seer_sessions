import numpy as np
from collections import deque

"""
Identifies contiguous regions of blue pixels (1) in the input grid.
For each blue region, it checks if the region completely encloses any maroon pixels (9).
A maroon pixel is considered enclosed if any path from it to the grid boundary must cross a pixel belonging to the blue region being evaluated.
If a blue region encloses maroon pixels, all pixels belonging to that region are changed to azure (8) in the output grid.
Otherwise, the blue region remains unchanged.
The background maroon pixels (9) are never modified.
Connectivity for regions is defined orthogonally (up, down, left, right).
"""

def find_connected_regions(grid, target_color):
    """
    Finds all contiguous regions of a specific color in the grid using BFS.
    Connectivity is orthogonal.

    Args:
        grid (np.array): The input grid.
        target_color (int): The color of the pixels to form regions from.

    Returns:
        list[set]: A list where each element is a set of (row, col) tuples
                   representing a single connected region.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == target_color and not visited[r, c]:
                # Start BFS for a new region
                region_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                region_coords.add((r, c))

                while q:
                    row, col = q.popleft()
                    # Check orthogonal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if neighbor is the target color and not visited
                            if grid[nr, nc] == target_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                region_coords.add((nr, nc))
                regions.append(region_coords)
    return regions

def check_enclosure(grid, region_coords_set):
    """
    Checks if a given region encloses any background (maroon, 9) pixels.
    Uses a flood fill (BFS) starting from boundary pixels that are NOT part of the region.
    Any maroon pixel not reached by the flood fill is considered enclosed.

    Args:
        grid (np.array): The input grid.
        region_coords_set (set): A set of (row, col) tuples for the region to check.

    Returns:
        bool: True if the region encloses maroon pixels, False otherwise.
    """
    rows, cols = grid.shape
    visited_by_flood = np.zeros_like(grid, dtype=bool)
    q = deque()

    # Initialize queue with boundary pixels NOT in the region being tested
    for r in range(rows):
        for c in [0, cols - 1]: # Left and right boundaries
             if (r, c) not in region_coords_set and not visited_by_flood[r, c]:
                 q.append((r, c))
                 visited_by_flood[r, c] = True
    for c in range(cols): # Top and bottom boundaries (avoid double-adding corners)
         for r in [0, rows - 1]:
             if (r, c) not in region_coords_set and not visited_by_flood[r, c]:
                 q.append((r, c))
                 visited_by_flood[r, c] = True


    # Perform BFS flood fill from the outside
    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # If neighbor is reachable (not part of the region barrier) and not visited
                if (nr, nc) not in region_coords_set and not visited_by_flood[nr, nc]:
                    visited_by_flood[nr, nc] = True
                    q.append((nr, nc))

    # Check for any maroon pixels that were NOT visited by the flood fill
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 9 and not visited_by_flood[r, c]:
                 # Found an enclosed maroon pixel
                 # We must ensure this maroon pixel wasn't enclosed by *another* barrier
                 # However, the logic correctly identifies if *any* maroon pixel is unreachable
                 # from the boundary without crossing the *current* region's pixels.
                 # If a maroon pixel is unreachable, it must be enclosed by *some* barrier.
                 # The flood fill explores everything reachable *without* crossing the specific region barrier.
                 # So if a maroon pixel is not visited, the *current* region must be (part of) its enclosure.
                 return True

    # No enclosed maroon pixels found
    return False


def transform(input_grid):
    """
    Transforms the input grid by changing blue (1) pixels to azure (8)
    if they form a contiguous region that encloses maroon (9) pixels.

    Args:
        input_grid (np.array): The 2D input grid.

    Returns:
        np.array: The transformed 2D output grid.
    """
    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # Find all connected regions of blue pixels (color 1)
    blue_regions = find_connected_regions(input_grid, 1)

    # Iterate through each identified blue region
    for region_coords_set in blue_regions:
        # Check if this region encloses any maroon (9) pixels
        if check_enclosure(input_grid, region_coords_set):
            # If it encloses, change the color of pixels in this region to azure (8)
            for r, c in region_coords_set:
                output_grid[r, c] = 8
                
    # change output pixels 

    return output_grid